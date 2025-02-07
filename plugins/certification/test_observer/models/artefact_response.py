import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artefact_status import ArtefactStatus

if TYPE_CHECKING:
    from ..models.user_response import UserResponse


T = TypeVar("T", bound="ArtefactResponse")


@_attrs_define
class ArtefactResponse:
    """
    Attributes:
        id (int):
        name (str):
        version (str):
        track (str):
        store (str):
        series (str):
        repo (str):
        os (str):
        release (str):
        owner (str):
        sha256 (str):
        image_url (str):
        stage (str):
        family (str):
        status (ArtefactStatus):
        assignee (Union['UserResponse', None]):
        due_date (Union[None, datetime.date]):
        bug_link (str):
        all_environment_reviews_count (int):
        completed_environment_reviews_count (int):
    """

    id: int
    name: str
    version: str
    track: str
    store: str
    series: str
    repo: str
    os: str
    release: str
    owner: str
    sha256: str
    image_url: str
    stage: str
    family: str
    status: ArtefactStatus
    assignee: Union["UserResponse", None]
    due_date: Union[None, datetime.date]
    bug_link: str
    all_environment_reviews_count: int
    completed_environment_reviews_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_response import UserResponse

        id = self.id

        name = self.name

        version = self.version

        track = self.track

        store = self.store

        series = self.series

        repo = self.repo

        os = self.os

        release = self.release

        owner = self.owner

        sha256 = self.sha256

        image_url = self.image_url

        stage = self.stage

        family = self.family

        status = self.status.value

        assignee: Union[None, dict[str, Any]]
        if isinstance(self.assignee, UserResponse):
            assignee = self.assignee.to_dict()
        else:
            assignee = self.assignee

        due_date: Union[None, str]
        if isinstance(self.due_date, datetime.date):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        bug_link = self.bug_link

        all_environment_reviews_count = self.all_environment_reviews_count

        completed_environment_reviews_count = self.completed_environment_reviews_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "version": version,
                "track": track,
                "store": store,
                "series": series,
                "repo": repo,
                "os": os,
                "release": release,
                "owner": owner,
                "sha256": sha256,
                "image_url": image_url,
                "stage": stage,
                "family": family,
                "status": status,
                "assignee": assignee,
                "due_date": due_date,
                "bug_link": bug_link,
                "all_environment_reviews_count": all_environment_reviews_count,
                "completed_environment_reviews_count": completed_environment_reviews_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_response import UserResponse

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        version = d.pop("version")

        track = d.pop("track")

        store = d.pop("store")

        series = d.pop("series")

        repo = d.pop("repo")

        os = d.pop("os")

        release = d.pop("release")

        owner = d.pop("owner")

        sha256 = d.pop("sha256")

        image_url = d.pop("image_url")

        stage = d.pop("stage")

        family = d.pop("family")

        status = ArtefactStatus(d.pop("status"))

        def _parse_assignee(data: object) -> Union["UserResponse", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                assignee_type_0 = UserResponse.from_dict(data)

                return assignee_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UserResponse", None], data)

        assignee = _parse_assignee(d.pop("assignee"))

        def _parse_due_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data).date()

                return due_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        due_date = _parse_due_date(d.pop("due_date"))

        bug_link = d.pop("bug_link")

        all_environment_reviews_count = d.pop("all_environment_reviews_count")

        completed_environment_reviews_count = d.pop(
            "completed_environment_reviews_count"
        )

        artefact_response = cls(
            id=id,
            name=name,
            version=version,
            track=track,
            store=store,
            series=series,
            repo=repo,
            os=os,
            release=release,
            owner=owner,
            sha256=sha256,
            image_url=image_url,
            stage=stage,
            family=family,
            status=status,
            assignee=assignee,
            due_date=due_date,
            bug_link=bug_link,
            all_environment_reviews_count=all_environment_reviews_count,
            completed_environment_reviews_count=completed_environment_reviews_count,
        )

        artefact_response.additional_properties = d
        return artefact_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
