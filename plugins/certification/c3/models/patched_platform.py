import json
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedPlatform")


@_attrs_define
class PatchedPlatform:
    """Serialiser for Platform model

    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]): Unique name for the hardware platform
        vendor_name (Union[Unset, str]):
        form_factor (Union[Unset, str]):
        codename (Union[Unset, str]): Unique identifier for the hardware platform
        aliases (Union[Unset, list[Any]]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    vendor_name: Union[Unset, str] = UNSET
    form_factor: Union[Unset, str] = UNSET
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
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if vendor_name is not UNSET:
            field_dict["vendor_name"] = vendor_name
        if form_factor is not UNSET:
            field_dict["form_factor"] = form_factor
        if codename is not UNSET:
            field_dict["codename"] = codename
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

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

        vendor_name = (
            self.vendor_name
            if isinstance(self.vendor_name, Unset)
            else (None, str(self.vendor_name).encode(), "text/plain")
        )

        form_factor = (
            self.form_factor
            if isinstance(self.form_factor, Unset)
            else (None, str(self.form_factor).encode(), "text/plain")
        )

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

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if vendor_name is not UNSET:
            field_dict["vendor_name"] = vendor_name
        if form_factor is not UNSET:
            field_dict["form_factor"] = form_factor
        if codename is not UNSET:
            field_dict["codename"] = codename
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        vendor_name = d.pop("vendor_name", UNSET)

        form_factor = d.pop("form_factor", UNSET)

        codename = d.pop("codename", UNSET)

        aliases = cast(list[Any], d.pop("aliases", UNSET))

        patched_platform = cls(
            id=id,
            name=name,
            vendor_name=vendor_name,
            form_factor=form_factor,
            codename=codename,
            aliases=aliases,
        )

        patched_platform.additional_properties = d
        return patched_platform

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
