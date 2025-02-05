import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Image")


@_attrs_define
class Image:
    """
    Attributes:
        id (int):
        project (int):
        name (str):
        url (str):
        buildstamp (str):
        username (str):
        password (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: int
    project: int
    name: str
    url: str
    buildstamp: str
    username: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project = self.project

        name = self.name

        url = self.url

        buildstamp = self.buildstamp

        username = self.username

        password = self.password

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project": project,
                "name": name,
                "url": url,
                "buildstamp": buildstamp,
                "username": username,
                "password": password,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        project = (None, str(self.project).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        url = (None, str(self.url).encode(), "text/plain")

        buildstamp = (None, str(self.buildstamp).encode(), "text/plain")

        username = (None, str(self.username).encode(), "text/plain")

        password = (None, str(self.password).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "project": project,
                "name": name,
                "url": url,
                "buildstamp": buildstamp,
                "username": username,
                "password": password,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project = d.pop("project")

        name = d.pop("name")

        url = d.pop("url")

        buildstamp = d.pop("buildstamp")

        username = d.pop("username")

        password = d.pop("password")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        image = cls(
            id=id,
            project=project,
            name=name,
            url=url,
            buildstamp=buildstamp,
            username=username,
            password=password,
            created_at=created_at,
            updated_at=updated_at,
        )

        image.additional_properties = d
        return image

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
