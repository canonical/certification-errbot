import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WriteProject")


@_attrs_define
class WriteProject:
    """
    Attributes:
        id (int):
        name (str):
        description (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        documentation_url (Union[None, Unset, str]):
        contact (Union[None, Unset, int]):
    """

    id: int
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    documentation_url: Union[None, Unset, str] = UNSET
    contact: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if documentation_url is not UNSET:
            field_dict["documentation_url"] = documentation_url
        if contact is not UNSET:
            field_dict["contact"] = contact

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        description = (None, str(self.description).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

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

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if documentation_url is not UNSET:
            field_dict["documentation_url"] = documentation_url
        if contact is not UNSET:
            field_dict["contact"] = contact

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

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

        write_project = cls(
            id=id,
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            documentation_url=documentation_url,
            contact=contact,
        )

        write_project.additional_properties = d
        return write_project

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
