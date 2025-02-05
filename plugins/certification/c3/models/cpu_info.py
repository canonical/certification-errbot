from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CPUInfo")


@_attrs_define
class CPUInfo:
    """Serializer for dump of the CPU type of all machines that have been
    certified and their form-factor.

        Attributes:
            name (str):
            vendor (str):
            family (str):
            codename (str):
    """

    name: str
    vendor: str
    family: str
    codename: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        vendor = self.vendor

        family = self.family

        codename = self.codename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "vendor": vendor,
                "family": family,
                "codename": codename,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        vendor = d.pop("vendor")

        family = d.pop("family")

        codename = d.pop("codename")

        cpu_info = cls(
            name=name,
            vendor=vendor,
            family=family,
            codename=codename,
        )

        cpu_info.additional_properties = d
        return cpu_info

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
