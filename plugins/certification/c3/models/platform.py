import json
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Platform")


@_attrs_define
class Platform:
    """Serialiser for Platform model

    Attributes:
        id (int):
        name (str): Unique name for the hardware platform
        vendor_name (str):
        form_factor (str):
        codename (Union[Unset, str]): Unique identifier for the hardware platform
        aliases (Union[Unset, list[Any]]):
    """

    id: int
    name: str
    vendor_name: str
    form_factor: str
    codename: Union[Unset, str] = UNSET
    aliases: Union[Unset, list[Any]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        vendor_name = self.vendor_name

        form_factor = self.form_factor

        codename = self.codename

        aliases: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "vendor_name": vendor_name,
                "form_factor": form_factor,
            }
        )
        if codename is not UNSET:
            field_dict["codename"] = codename
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        vendor_name = (None, str(self.vendor_name).encode(), "text/plain")

        form_factor = (None, str(self.form_factor).encode(), "text/plain")

        codename = (
            self.codename
            if isinstance(self.codename, Unset)
            else (None, str(self.codename).encode(), "text/plain")
        )

        aliases: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.aliases, Unset):
            _temp_aliases = self.aliases
            aliases = (None, json.dumps(_temp_aliases).encode(), "application/json")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "name": name,
                "vendor_name": vendor_name,
                "form_factor": form_factor,
            }
        )
        if codename is not UNSET:
            field_dict["codename"] = codename
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        vendor_name = d.pop("vendor_name")

        form_factor = d.pop("form_factor")

        codename = d.pop("codename", UNSET)

        aliases = cast(list[Any], d.pop("aliases", UNSET))

        platform = cls(
            id=id,
            name=name,
            vendor_name=vendor_name,
            form_factor=form_factor,
            codename=codename,
            aliases=aliases,
        )

        platform.additional_properties = d
        return platform

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
