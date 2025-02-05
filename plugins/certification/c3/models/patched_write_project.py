import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedWriteProject")


@_attrs_define
class PatchedWriteProject:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        documentation_url (Union[None, Unset, str]):
        contact (Union[None, Unset, int]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    documentation_url: Union[None, Unset, str] = UNSET
    contact: Union[None, Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        documentation_url: Union[None, Unset, str]
        if isinstance(self.documentation_url, Unset):
            documentation_url = UNSET
        else:
            documentation_url = self.documentation_url

        contact: Union[None, Unset, int]
        if isinstance(self.contact, Unset):
            contact = UNSET
        else:
            contact = self.contact

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
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if documentation_url is not UNSET:
            field_dict["documentation_url"] = documentation_url
        if contact is not UNSET:
            field_dict["contact"] = contact
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

        name = (
            self.name
            if isinstance(self.name, Unset)
            else (None, str(self.name).encode(), "text/plain")
        )

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        documentation_url: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.documentation_url, Unset):
            documentation_url = UNSET
        elif isinstance(self.documentation_url, str):
            documentation_url = (
                None,
                str(self.documentation_url).encode(),
                "text/plain",
            )
        else:
            documentation_url = (
                None,
                str(self.documentation_url).encode(),
                "text/plain",
            )

        contact: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, int):
            contact = (None, str(self.contact).encode(), "text/plain")
        else:
            contact = (None, str(self.contact).encode(), "text/plain")

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
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if documentation_url is not UNSET:
            field_dict["documentation_url"] = documentation_url
        if contact is not UNSET:
            field_dict["contact"] = contact
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_documentation_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        documentation_url = _parse_documentation_url(d.pop("documentation_url", UNSET))

        def _parse_contact(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        contact = _parse_contact(d.pop("contact", UNSET))

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

        patched_write_project = cls(
            id=id,
            name=name,
            description=description,
            documentation_url=documentation_url,
            contact=contact,
            created_at=created_at,
            updated_at=updated_at,
        )

        patched_write_project.additional_properties = d
        return patched_write_project

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
