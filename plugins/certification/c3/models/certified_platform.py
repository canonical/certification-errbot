from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.certified_platform_certificates import CertifiedPlatformCertificates


T = TypeVar("T", bound="CertifiedPlatform")


@_attrs_define
class CertifiedPlatform:
    """Serialize the platform model for the public API

    Attributes:
        id (int):
        name (str): Unique name for the hardware platform
        vendor (str):
        certificates (CertifiedPlatformCertificates):
        category (str): The category of a machine comes from the form factor of the platform.

            Some form factors have parent form factors, in which
            case we return the parent form factor name
    """

    id: int
    name: str
    vendor: str
    certificates: "CertifiedPlatformCertificates"
    category: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        vendor = self.vendor

        certificates = self.certificates.to_dict()

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "vendor": vendor,
                "certificates": certificates,
                "category": category,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.certified_platform_certificates import (
            CertifiedPlatformCertificates,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        vendor = d.pop("vendor")

        certificates = CertifiedPlatformCertificates.from_dict(d.pop("certificates"))

        category = d.pop("category")

        certified_platform = cls(
            id=id,
            name=name,
            vendor=vendor,
            certificates=certificates,
            category=category,
        )

        certified_platform.additional_properties = d
        return certified_platform

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
