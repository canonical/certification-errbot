import logging
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import (
    sync_detailed as get_artefacts,
)
from test_observer.api.artefacts.patch_artefact_v1_artefacts_artefact_id_patch import (
    sync_detailed as patch_artefact,
)
from test_observer.client import Client as TestObserverClient
from test_observer.models import ArtefactPatch, ArtefactResponse, ArtefactStatus
from user_handle_cache import get_user_handle

logger = logging.getLogger(__name__)

# Get configured artefact families to include (default: all families)
# Can be configured as comma-separated list, e.g., "snap,deb,image"
ARTEFACT_FAMILIES_ENV = os.environ.get("ARTEFACT_FAMILIES", "")
INCLUDED_FAMILIES: Optional[Set[str]] = None

if ARTEFACT_FAMILIES_ENV:
    # Parse comma-separated list and normalize to lowercase
    families = [f.strip().lower() for f in ARTEFACT_FAMILIES_ENV.split(",") if f.strip()]
    if families:
        INCLUDED_FAMILIES = set(families)
        logger.info(f"Configured to include only these artefact families: {INCLUDED_FAMILIES}")
        # Warn if any family names look incorrect
        valid_families = {"snap", "deb", "image", "charm"}
        invalid = INCLUDED_FAMILIES - valid_families
        if invalid:
            logger.warning(f"Warning: These family names may be invalid: {invalid}. Valid families are: {valid_families}")
    else:
        logger.info("ARTEFACT_FAMILIES is empty, including all families")
else:
    logger.info("ARTEFACT_FAMILIES not configured, including all families")


def format_artefact_message(artefact: ArtefactResponse, is_overdue: bool = False) -> str:
    """Format a single artefact message with appropriate highlighting.
    
    Args:
        artefact: The artefact to format
        is_overdue: Whether the artefact is overdue
    """
    now = datetime.now().date()
    due_date_str = ""
    
    if artefact.due_date:
        days_until_due = (artefact.due_date - now).days
        
        if is_overdue:
            # Overdue - show in red with days overdue
            days_overdue = abs(days_until_due)
            due_date_str = f" 🔴 **OVERDUE by {days_overdue} day{'s' if days_overdue != 1 else ''}** ({artefact.due_date.strftime('%d-%m-%Y')})"
        elif days_until_due < 7:
            # Due within 7 days - show in bold with days remaining
            due_date_str = f" **⚠️ Due in {days_until_due} day{'s' if days_until_due != 1 else ''}** ({artefact.due_date.strftime('%d-%m-%Y')})"
        else:
            # Not urgent - show normally
            due_date_str = f" (due {artefact.due_date.strftime('%d-%m-%Y')})"
    
    completed_reviews = artefact.completed_environment_reviews_count
    all_reviews = artefact.all_environment_reviews_count
    review_percentage = (
        round((completed_reviews / all_reviews) * 100) if all_reviews > 0 else 0
    )
    
    return f"- **[{artefact.name} {artefact.version}](https://test-observer.canonical.com/#/{artefact.family}s/{artefact.id})**:{due_date_str} - {completed_reviews}/{all_reviews} reviews ({review_percentage:.0f}%)\n"


def reply_with_artefacts_summary(target_user, args: List[str]) -> str:
    """
    Reply to a user with a relevant set of artefacts, i.e. union of:
    - pending (not approved, not rejected) artefacts.
    - recently rejected artefacts.

    When no argument is provided, returns the summary for the sender
    (artefacts filtered with them as the assignee).
    
    Arguments:
    - No args or just a mattermost handle: Show artefacts for that user (defaults to sender)
    - name-contains: filtering by artefact name substring
    - all: returns all artefacts.
    - pending: list only in 'undecided' state.
    """

    artifact_filter = None
    assigned_to_filter = None
    filter_by_sender_as_assignee = True

    # Process arguments
    processed_args = []
    for arg in args:
        if arg.startswith("name-contains:"):
            artifact_filter = arg.split("name-contains:", 1)[1].lower()
            filter_by_sender_as_assignee = False
            processed_args.append(arg)
        elif arg in ["all", "pending"]:
            processed_args.append(arg)
        else:
            # Treat any other argument as a mattermost handle
            # Strip @ if present
            handle = arg.lstrip("@")
            if handle and not artifact_filter and not assigned_to_filter:
                assigned_to_filter = handle.lower()
                filter_by_sender_as_assignee = False

    if "all" in processed_args and (artifact_filter or assigned_to_filter):
        return "You can't use 'all' with 'name-contains' or username filter"

    if "all" in processed_args and "pending" in processed_args:
        return "You can't use 'all' with 'pending'"

    if len([arg for arg in args if arg.startswith("name-contains:")]) > 1:
        return "You can't use multiple 'name-contains' arguments"

    test_observer_client = TestObserverClient(
        base_url="https://test-observer-api.canonical.com"
    )

    out_msg = ""

    now = datetime.now().date()

    with test_observer_client:
        r = get_artefacts(client=test_observer_client)

        if not isinstance(r.parsed, list):
            logger.error("API response is not a list")
            return "Error retrieving artefacts"

        artefacts_by_user = artefacts_by_user_handle(
            r.parsed, artifact_filter, assigned_to_filter, "pending" in processed_args
        )

        if "all" in processed_args:
            # Show all artefacts when "all" is specified
            user_artefacts = artefacts_by_user
        elif filter_by_sender_as_assignee:
            # When no args provided, show artefacts for the sender
            sender_handle = target_user.username
            
            # Try to find artefacts for the sender
            # First try exact match
            if sender_handle in artefacts_by_user:
                user_artefacts = {sender_handle: artefacts_by_user[sender_handle]}
            else:
                # Try case-insensitive match
                sender_handle_lower = sender_handle.lower()
                matched_user = None
                for user_key in artefacts_by_user.keys():
                    if user_key.lower() == sender_handle_lower:
                        matched_user = user_key
                        break
                
                if matched_user:
                    user_artefacts = {matched_user: artefacts_by_user[matched_user]}
                else:
                    # Log for debugging
                    logger.info(f"No artefacts found for sender '{sender_handle}'. Available users: {list(artefacts_by_user.keys())}")
                    user_artefacts = {}
        else:
            # When filter_by_sender_as_assignee is False, show all filtered artefacts
            # (filtered by assigned_to_filter, artifact_filter, or other criteria)
            user_artefacts = artefacts_by_user

        # Add heading and instructions link if there are any artefacts
        if user_artefacts:
            out_msg += "## Artefact Review\n\n"
            out_msg += "You have some Test Observer artefacts to review. For review instructions, please take a look [here](https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/).\n\n"
        
        # Group artefacts by user and separate overdue from current
        for user, artefacts in sorted(user_artefacts.items()):
            # Separate overdue and current artefacts
            overdue = []
            current = []
            
            for artefact in artefacts:
                if artefact.due_date and artefact.due_date < now:
                    overdue.append(artefact)
                else:
                    current.append(artefact)
            
            # Display user header
            if user == "No assignee":
                out_msg += f"**{user}**\n"
            else:
                out_msg += f"**@{user}**\n"
            
            # Show overdue artefacts first (sorted by most overdue)
            if overdue:
                overdue.sort(key=lambda x: x.due_date or datetime.min.date())
                for artefact in overdue:
                    out_msg += format_artefact_message(artefact, is_overdue=True)
            
            # Add spacing between overdue and current if both exist
            if overdue and current:
                out_msg += "\n"
            
            # Show current artefacts (sorted by due date, soonest first)
            if current:
                current.sort(
                    key=lambda x: (
                        x.due_date is None,
                        x.due_date or datetime.max.date(),
                    )
                )
                for artefact in current:
                    out_msg += format_artefact_message(artefact, is_overdue=False)
            
            out_msg += "\n"

        # Sort un-assigned artefacts last
        unassigned_artefacts = artefacts_by_user.pop("No assignee", [])
        if unassigned_artefacts:
            artefacts_by_user["No assignee"] = unassigned_artefacts

    if out_msg == "":
        if filter_by_sender_as_assignee:
            # When looking for sender's artefacts specifically
            sender_handle = target_user.username if hasattr(target_user, 'username') else 'unknown'
            out_msg = f"No pending artefacts found for @{sender_handle}"
        elif assigned_to_filter:
            out_msg = f"No pending artefacts found for @{assigned_to_filter}"
        elif artifact_filter:
            out_msg = f"No pending artefacts found with name containing '{artifact_filter}'"
        else:
            out_msg = "No pending artefacts found"
    return out_msg


def artefacts_by_user_handle(
    artefacts_response: list[ArtefactResponse],
    artifact_filter: str | None,
    assigned_to_filter: str | None,
    pending: bool,
) -> Dict[str, List[ArtefactResponse]]:
    artefacts_by_user: Dict[str, List[ArtefactResponse]] = {}

    now = datetime.now().date()
    one_week_ago = now - timedelta(weeks=1)

    filtered_count = 0

    for artefact in artefacts_response:
        # Filter by configured families if specified
        if INCLUDED_FAMILIES and artefact.family not in INCLUDED_FAMILIES:
            continue
            
        if artefact.status == ArtefactStatus.APPROVED:
            continue

        if (
            artefact.status == ArtefactStatus.MARKED_AS_FAILED
            and artefact.due_date
            and artefact.due_date < one_week_ago
        ):
            continue

        if artifact_filter and artifact_filter not in artefact.name.lower():
            continue

        assignee = artefact.assignee
        if not assignee and not artefact.due_date:
            continue

        if assignee and assignee.launchpad_email:
            user_details = get_user_handle(assignee.launchpad_email)
            if user_details:
                assignee_handle = user_details["username"]
            else:
                assignee_handle = "No assignee"
        else:
            assignee_handle = "No assignee"

        if assigned_to_filter and assigned_to_filter.lower() != assignee_handle.lower():
            continue

        if pending and (artefact.status in [ArtefactStatus.MARKED_AS_FAILED]):
            continue

        # This artefact will be included
        filtered_count += 1

        if assignee_handle not in artefacts_by_user:
            artefacts_by_user[assignee_handle] = []

        artefacts_by_user[assignee_handle].append(artefact)

    return artefacts_by_user


def pending_artefacts_by_user_handle() -> Dict[str | None, List[ArtefactResponse]]:
    """
    Get all pending (not approved or failed) artefacts by user's Mattermost handle
    """
    test_observer_client = TestObserverClient(
        base_url="https://test-observer-api.canonical.com"
    )

    with test_observer_client:
        r = get_artefacts(client=test_observer_client)

        if not isinstance(r.parsed, list):
            raise Exception("Error retrieving artefacts")

        artefacts_by_user: Dict[str | None, List[ArtefactResponse]] = {}

        for artefact in r.parsed:
            # Filter by configured families if specified
            if INCLUDED_FAMILIES and artefact.family not in INCLUDED_FAMILIES:
                continue
                
            if artefact.status in [
                ArtefactStatus.APPROVED,
                ArtefactStatus.MARKED_AS_FAILED,
            ]:
                continue

            assignee = artefact.assignee
            if not assignee and not artefact.due_date:
                continue

            if assignee and assignee.launchpad_email:
                user_details = get_user_handle(assignee.launchpad_email)
                if user_details:
                    assignee_handle = user_details["username"]
                else:
                    assignee_handle = None
            else:
                assignee_handle = None

            if assignee_handle not in artefacts_by_user:
                artefacts_by_user[assignee_handle] = []

            artefacts_by_user[assignee_handle].append(artefact)

        return artefacts_by_user


def send_artefact_summaries(sender):
    """
    Send a digest of pending Test Observer artefacts per user.
    """
    pending_artefacts = pending_artefacts_by_user_handle()
    now = datetime.now().date()

    for user, artefacts in pending_artefacts.items():
        if len(artefacts) == 0:
            continue

        if user is not None:
            # Separate overdue and current artefacts
            overdue = []
            current = []
            
            for artefact in artefacts:
                if artefact.due_date and artefact.due_date < now:
                    overdue.append(artefact)
                else:
                    current.append(artefact)
            
            msg = f"Hello @{user}!\n\n"
            msg += "## Artefact Review\n\n"
            msg += "You have some Test Observer artefacts to review. For review instructions, please take a look [here](https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/).\n\n"
            
            # Show overdue artefacts first (sorted by most overdue)
            if overdue:
                overdue.sort(key=lambda x: x.due_date or datetime.min.date())
                for artefact in overdue:
                    msg += format_artefact_message(artefact, is_overdue=True)
            
            # Add spacing between overdue and current if both exist
            if overdue and current:
                msg += "\n"
            
            # Show current artefacts (sorted by due date, soonest first)
            if current:
                current.sort(key=lambda x: (x.due_date is None, x.due_date or datetime.max.date()))
                for artefact in current:
                    msg += format_artefact_message(artefact, is_overdue=False)

            identifier = sender.build_identifier(f"@{user}")
            sender.send(identifier, msg)


def extract_artefact_id_from_url(url_or_id: str) -> int:
    """
    Extract artefact ID from a Test Observer URL or return the ID if it's already an integer.
    
    Supports URLs like:
    - https://test-observer.canonical.com/#/snaps/123
    - https://test-observer.canonical.com/#/debs/456
    - https://test-observer.canonical.com/#/images/789
    
    Args:
        url_or_id: Either a Test Observer URL or an artefact ID
    
    Returns:
        The artefact ID as an integer
    
    Raises:
        ValueError: If the input is not a valid URL or ID
    """
    # First try to parse as integer
    try:
        return int(url_or_id)
    except ValueError:
        pass
    
    # Try to extract from URL
    # Pattern matches: /#/[family]s/[id] where family is snap, deb, image, etc.
    pattern = r'#/(?:snaps?|debs?|images?|charms?)/([0-9]+)'
    match = re.search(pattern, url_or_id)
    
    if match:
        return int(match.group(1))
    
    raise ValueError(f"Could not extract artefact ID from: {url_or_id}")


def archive_artefact_by_id(artefact_id: int, comment: str = None) -> str:
    """
    Archive an artefact by its ID.
    
    Args:
        artefact_id: The ID of the artefact to archive
        comment: Optional comment to add when archiving
    
    Returns:
        Success or error message
    """
    test_observer_client = TestObserverClient(
        base_url="https://test-observer-api.canonical.com"
    )
    
    with test_observer_client:
        # Create patch request to archive the artefact
        patch_data = ArtefactPatch(
            archived=True,
            comment=comment if comment else "Archived via errbot admin command"
        )
        
        try:
            response = patch_artefact(
                client=test_observer_client,
                artefact_id=artefact_id,
                body=patch_data
            )
            
            if response.parsed:
                artefact = response.parsed
                return f"Successfully archived artefact: {artefact.name} {artefact.version} (ID: {artefact.id})"
            else:
                return f"Failed to archive artefact {artefact_id}: No response from API"
        except Exception as e:
            logger.error(f"Error archiving artefact {artefact_id}: {e}")
            return f"Error archiving artefact {artefact_id}: {str(e)}"
