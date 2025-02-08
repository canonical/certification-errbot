from datetime import datetime, timedelta
from test_observer.models import ArtefactStatus, ArtefactResponse
from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import sync_detailed as get_artefacts
from test_observer.client import Client as TestObserverClient

from user_handle_cache import get_assignee_handle
from typing import Any, List, Dict

now = datetime.now().date()
def artefacts_summary(msg: Any, args: List[str]) -> str:
    test_observer_client = TestObserverClient(base_url='https://test-observer-api.canonical.com')

    out_msg = ''
    artefacts_by_user: Dict[str, List[ArtefactResponse]] = {}

    one_week_ago = now - timedelta(weeks=1)
    artifact_filter = None
    assigned_to_filter = None

    filter_by_sender_as_assignee = True

    for arg in args:
        if arg.startswith("name-contains:"):
            artifact_filter = arg.split("name-contains:", 1)[1].lower()
            filter_by_sender_as_assignee = False

            if "all" in args:
                return "You can't use 'all' and 'name-contains' together"

        if arg.startswith("assigned-to:"):
            assigned_to_filter = arg.split("assigned-to:", 1)[1].lower()
            filter_by_sender_as_assignee = False

            if "all" in args:
                return "You can't use 'all' and 'assigned-to' together"

    with test_observer_client:
        r = get_artefacts(client=test_observer_client)

        if not isinstance(r.parsed, list):
            return "Error retrieving artefacts"

        for artefact in r.parsed:
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

            if len(args) > 0 and args[0] == 'pending' and (artefact.status in [ArtefactStatus.MARKED_AS_FAILED]):
                continue

            if assignee_handle not in artefacts_by_user:
                artefacts_by_user[assignee_handle] = []

            artefacts_by_user[assignee_handle].append(artefact)

        if "all" in args or not filter_by_sender_as_assignee:
            user_artefacts = artefacts_by_user
        else:
            sender_handle = msg.frm.username 
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
                due_date_str = f" (due {artefact.due_date.strftime('%d-%m-%Y')})" if artefact.due_date else ""
                completed_reviews = artefact.completed_environment_reviews_count
                all_reviews = artefact.all_environment_reviews_count
                review_percentage = round((completed_reviews / all_reviews) * 100) if all_reviews > 0 else 0
                out_msg += f"- **[{artefact.name} {artefact.version}](https://test-observer.canonical.com/#/{artefact.family}s/{artefact.id})**: {due_date_str} - {completed_reviews}/{all_reviews} reviews ({review_percentage:.0f}%)\n"
            out_msg += "\n"

        # Sort un-assigned artefacts last
        unassigned_artefacts = artefacts_by_user.pop("No assignee", [])
        if unassigned_artefacts:
            artefacts_by_user["No assignee"] = unassigned_artefacts

    return out_msg
