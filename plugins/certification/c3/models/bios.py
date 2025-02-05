from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Bios")


@_attrs_define
class Bios:
    """Serializer for the Bios model

    Attributes:
        name (str):
        vendor (str):
        version (str):
        firmware_type (str):
    """

    name: str
    vendor: str
    version: str
    firmware_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        vendor = self.vendor

        version = self.version

        firmware_type = self.firmware_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "vendor": vendor,
                "version": version,
                "firmware_type": firmware_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        vendor = d.pop("vendor")

        version = d.pop("version")

        firmware_type = d.pop("firmware_type")

        bios = cls(
            name=name,
            vendor=vendor,
            version=version,
            firmware_type=firmware_type,
        )

        bios.additional_properties = d
        return bios

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
