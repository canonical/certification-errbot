from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CertifiedConfigurationDevice")


@_attrs_define
class CertifiedConfigurationDevice:
    """
    Attributes:
        vendor_id (int):
        make (str):
        name (str):
        raw_name (str):
        raw_make (str):
        canonical_id (Union[Unset, str]):
        bus (Union[Unset, str]):
        identifier (Union[Unset, str]):
        subsystem (Union[Unset, str]):
        subvendor_id (Union[Unset, int]):
        subproduct_name (Union[Unset, str]):
        category (Union[Unset, str]):
    """

    vendor_id: int
    make: str
    name: str
    raw_name: str
    raw_make: str
    canonical_id: Union[Unset, str] = UNSET
    bus: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    subsystem: Union[Unset, str] = UNSET
    subvendor_id: Union[Unset, int] = UNSET
    subproduct_name: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vendor_id = self.vendor_id

        make = self.make

        name = self.name

        raw_name = self.raw_name

        raw_make = self.raw_make

        canonical_id = self.canonical_id

        bus = self.bus

        identifier = self.identifier

        subsystem = self.subsystem

        subvendor_id = self.subvendor_id

        subproduct_name = self.subproduct_name

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vendor_id": vendor_id,
                "make": make,
                "name": name,
                "raw_name": raw_name,
                "raw_make": raw_make,
            }
        )
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if bus is not UNSET:
            field_dict["bus"] = bus
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if subsystem is not UNSET:
            field_dict["subsystem"] = subsystem
        if subvendor_id is not UNSET:
            field_dict["subvendor_id"] = subvendor_id
        if subproduct_name is not UNSET:
            field_dict["subproduct_name"] = subproduct_name
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        vendor_id = d.pop("vendor_id")

        make = d.pop("make")

        name = d.pop("name")

        raw_name = d.pop("raw_name")

        raw_make = d.pop("raw_make")

        canonical_id = d.pop("canonical_id", UNSET)

        bus = d.pop("bus", UNSET)

        identifier = d.pop("identifier", UNSET)

        subsystem = d.pop("subsystem", UNSET)

        subvendor_id = d.pop("subvendor_id", UNSET)

        subproduct_name = d.pop("subproduct_name", UNSET)

        category = d.pop("category", UNSET)

        certified_configuration_device = cls(
            vendor_id=vendor_id,
            make=make,
            name=name,
            raw_name=raw_name,
            raw_make=raw_make,
            canonical_id=canonical_id,
            bus=bus,
            identifier=identifier,
            subsystem=subsystem,
            subvendor_id=subvendor_id,
            subproduct_name=subproduct_name,
            category=category,
        )

        certified_configuration_device.additional_properties = d
        return certified_configuration_device

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
