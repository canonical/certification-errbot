from datetime import datetime, date, timedelta
from test_observer.models import ArtefactStatus, ArtefactResponse
from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import sync_detailed as get_artefacts
from test_observer.client import Client as TestObserverClient

from user_handle_cache import get_assignee_handle
from typing import List, Dict

import logging

logger = logging.getLogger(__name__)


def format_artefact_message(artefact: ArtefactResponse) -> str:
    due_date_str = f" (due {artefact.due_date.strftime('%d-%m-%Y')})" if artefact.due_date else ""
    completed_reviews = artefact.completed_environment_reviews_count
    all_reviews = artefact.all_environment_reviews_count
    review_percentage = round((completed_reviews / all_reviews) * 100) if all_reviews > 0 else 0
    return f"- **[{artefact.name} {artefact.version}](https://test-observer.canonical.com/#/{artefact.family}s/{artefact.id})**: {due_date_str} - {completed_reviews}/{all_reviews} reviews ({review_percentage:.0f}%)\n"

def reply_with_artefacts_summary(target_user, args: List[str]) -> str:
    """
    Reply to a user with a relevant set of artefacts, i.e. union of:
    - pending (not approved, not rejected) artefacts.
    - recently rejected artefacts.

    When no argument is provided, returns the summary for the sender
    (artefacts filtered with them as the assignee).
    
    Optional arguments to the command:
    - name-contains: filtering by artefact name substring
    - assigned-to: filtering by exact match to user's Mattermost handle
    - all: returns all artefacts.
    - pending: list only in 'undecided' state.
    """

    artifact_filter = None
    assigned_to_filter = None

    for arg in args:
        if arg.startswith("name-contains:"):
            artifact_filter = arg.split("name-contains:", 1)[1].lower()
            filter_by_sender_as_assignee = False

        if arg.startswith("assigned-to:"):
            assigned_to_filter = arg.split("assigned-to:", 1)[1].lower()
            filter_by_sender_as_assignee = False

    if "all" in args and (artifact_filter or assigned_to_filter):
        return "You can't use 'all' with 'name-contains' or 'assigned-to'"
    
    if "all" in args and "pending" in args:
        return "You can't use 'all' with 'pending'"
    
    if len([arg for arg in args if arg.startswith("name-contains:")]) > 1:
        return "You can't use multiple 'name-contains' arguments"
    
    if len([arg for arg in args if arg.startswith("assigned-to:")]) > 1:
        return "You can't use multiple 'assigned-to' arguments"

    test_observer_client = TestObserverClient(base_url='https://test-observer-api.canonical.com')

    out_msg = ''

    filter_by_sender_as_assignee = True

    now = datetime.now().date()

    with test_observer_client:
        r = get_artefacts(client=test_observer_client)

        if not isinstance(r.parsed, list):
            return "Error retrieving artefacts"

        artefacts_by_user = artefacts_by_user_handle(r.parsed, artifact_filter, assigned_to_filter, "pending" in args)

        if "all" in args or not filter_by_sender_as_assignee:
            user_artefacts = artefacts_by_user
        else:
            sender_handle = target_user.username 
            if sender_handle in artefacts_by_user:
                user_artefacts = {sender_handle: artefacts_by_user[sender_handle]}
            else:
                user_artefacts = {}

        for user, artefacts in sorted(user_artefacts.items()):
            artefacts.sort(key=lambda x: (x.assignee is None,
                                           x.due_date is None,
                                           False if x.due_date is None else x.due_date < now,
                                           x.due_date or datetime.max.date()))
            if user == "No assignee":
                out_msg += f"**{user}**\n"
            else:
                out_msg += f"**@{user}**\n"
            for artefact in artefacts:
                out_msg += format_artefact_message(artefact)
            out_msg += "\n"

        # Sort un-assigned artefacts last
        unassigned_artefacts = artefacts_by_user.pop("No assignee", [])
        if unassigned_artefacts:
            artefacts_by_user["No assignee"] = unassigned_artefacts

    if out_msg == '':
        out_msg = f"No pending artefacts (assigned to filter: {assigned_to_filter}, name filter: {artifact_filter})"

    return out_msg

def artefacts_by_user_handle(
        artefacts_response: list[ArtefactResponse],
        artifact_filter: str | None,
        assigned_to_filter: str | None,
        pending: bool) -> Dict[str, List[ArtefactResponse]]:
    artefacts_by_user: Dict[str, List[ArtefactResponse]] = {}

    now = datetime.now().date()
    one_week_ago = now - timedelta(weeks=1)

    for artefact in artefacts_response:
        if artefact.status == ArtefactStatus.APPROVED:
            continue

        if artefact.status == ArtefactStatus.MARKED_AS_FAILED and artefact.due_date and artefact.due_date < one_week_ago:
            continue

        if artifact_filter and artifact_filter not in artefact.name.lower():
            continue

        assignee = artefact.assignee
        if not assignee and not artefact.due_date:
            continue
        
        if assignee and assignee.launchpad_email:
            assignee_handle = get_assignee_handle(assignee.launchpad_email)["username"]
        else:
            assignee_handle = "No assignee"

        if assigned_to_filter and assigned_to_filter != assignee_handle.lower():
            continue

        if pending and (artefact.status in [ArtefactStatus.MARKED_AS_FAILED]):
            continue

        if assignee_handle not in artefacts_by_user:
            artefacts_by_user[assignee_handle] = []

        artefacts_by_user[assignee_handle].append(artefact)
    
    return artefacts_by_user

def pending_artefacts_by_user_handle() -> Dict[str | None, List[ArtefactResponse]]:
    """
    Get all pending (not approved or failed) artefacts by user's Mattermost handle
    """
    test_observer_client = TestObserverClient(base_url='https://test-observer-api.canonical.com')

    with test_observer_client:
        r = get_artefacts(client=test_observer_client)

        if not isinstance(r.parsed, list):
            raise Exception("Error retrieving artefacts")

        artefacts_by_user: Dict[str | None, List[ArtefactResponse]] = {}

        for artefact in r.parsed:
            if artefact.status in [ArtefactStatus.APPROVED, ArtefactStatus.MARKED_AS_FAILED]:
                continue

            assignee = artefact.assignee
            if not assignee and not artefact.due_date:
                continue

            if assignee and assignee.launchpad_email:
                assignee_handle = get_assignee_handle(assignee.launchpad_email)["username"]
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

    for user, artefacts in pending_artefacts.items():
        if len(artefacts) == 0:
            continue

        if user is not None:
            msg = ''
            msg += f"Hello @{user}! You have some test artefacts to review:\n"
            for artefact in artefacts:
                msg += format_artefact_message(artefact)

            identifier = sender.build_identifier(f"@{user}")
            logger.info(f"Sending digest to {user}")

            sender.send(identifier, msg)
