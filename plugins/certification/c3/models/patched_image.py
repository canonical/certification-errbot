import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedImage")


@_attrs_define
class PatchedImage:
    """
    Attributes:
        id (Union[Unset, int]):
        project (Union[Unset, int]):
        name (Union[Unset, str]):
        url (Union[Unset, str]):
        buildstamp (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    project: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    buildstamp: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project = self.project

        name = self.name

        url = self.url

        buildstamp = self.buildstamp

        username = self.username

        password = self.password

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if project is not UNSET:
            field_dict["project"] = project
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if buildstamp is not UNSET:
            field_dict["buildstamp"] = buildstamp
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (
            self.id
            if isinstance(self.id, Unset)
            else (None, str(self.id).encode(), "text/plain")
        )

        project = (
            self.project
            if isinstance(self.project, Unset)
            else (None, str(self.project).encode(), "text/plain")
        )

        name = (
            self.name
            if isinstance(self.name, Unset)
            else (None, str(self.name).encode(), "text/plain")
        )

        url = (
            self.url
            if isinstance(self.url, Unset)
            else (None, str(self.url).encode(), "text/plain")
        )

        buildstamp = (
            self.buildstamp
            if isinstance(self.buildstamp, Unset)
            else (None, str(self.buildstamp).encode(), "text/plain")
        )

        username = (
            self.username
            if isinstance(self.username, Unset)
            else (None, str(self.username).encode(), "text/plain")
        )

        password = (
            self.password
            if isinstance(self.password, Unset)
            else (None, str(self.password).encode(), "text/plain")
        )

        created_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat().encode()

        updated_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat().encode()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if project is not UNSET:
            field_dict["project"] = project
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if buildstamp is not UNSET:
            field_dict["buildstamp"] = buildstamp
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        project = d.pop("project", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        buildstamp = d.pop("buildstamp", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        patched_image = cls(
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

        patched_image.additional_properties = d
        return patched_image

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
