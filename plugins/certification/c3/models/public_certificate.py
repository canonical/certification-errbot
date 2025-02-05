import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bios import Bios
    from ..models.public_release import PublicRelease


T = TypeVar("T", bound="PublicCertificate")


@_attrs_define
class PublicCertificate:
    """Include details about configuration certificate, release, bios, and kernel info

    Attributes:
        canonical_id (str):
        vendor (str):
        platform (str):
        configuration (str):
        created_at (datetime.datetime):
        release (PublicRelease): Public serialiser for the release model
        architecture (Union[None, str]):
        kernel_version (Union[None, str]):
        bios (Union['Bios', None]):
        firmware_revision (Union[None, str]):
        completed (Union[None, Unset, datetime.datetime]):
        name (Union[None, Unset, str]):
    """

    canonical_id: str
    vendor: str
    platform: str
    configuration: str
    created_at: datetime.datetime
    release: "PublicRelease"
    architecture: Union[None, str]
    kernel_version: Union[None, str]
    bios: Union["Bios", None]
    firmware_revision: Union[None, str]
    completed: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bios import Bios

        canonical_id = self.canonical_id

        vendor = self.vendor

        platform = self.platform

        configuration = self.configuration

        created_at = self.created_at.isoformat()

        release = self.release.to_dict()

        architecture: Union[None, str]
        architecture = self.architecture

        kernel_version: Union[None, str]
        kernel_version = self.kernel_version

        bios: Union[None, dict[str, Any]]
        if isinstance(self.bios, Bios):
            bios = self.bios.to_dict()
        else:
            bios = self.bios

        firmware_revision: Union[None, str]
        firmware_revision = self.firmware_revision

        completed: Union[None, Unset, str]
        if isinstance(self.completed, Unset):
            completed = UNSET
        elif isinstance(self.completed, datetime.datetime):
            completed = self.completed.isoformat()
        else:
            completed = self.completed

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canonical_id": canonical_id,
                "vendor": vendor,
                "platform": platform,
                "configuration": configuration,
                "created_at": created_at,
                "release": release,
                "architecture": architecture,
                "kernel_version": kernel_version,
                "bios": bios,
                "firmware_revision": firmware_revision,
            }
        )
        if completed is not UNSET:
            field_dict["completed"] = completed
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.bios import Bios
        from ..models.public_release import PublicRelease

        d = src_dict.copy()
        canonical_id = d.pop("canonical_id")

        vendor = d.pop("vendor")

        platform = d.pop("platform")

        configuration = d.pop("configuration")

        created_at = isoparse(d.pop("created_at"))

        release = PublicRelease.from_dict(d.pop("release"))

        def _parse_architecture(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        architecture = _parse_architecture(d.pop("architecture"))

        def _parse_kernel_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        kernel_version = _parse_kernel_version(d.pop("kernel_version"))

        def _parse_bios(data: object) -> Union["Bios", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                bios_type_1 = Bios.from_dict(data)

                return bios_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Bios", None], data)

        bios = _parse_bios(d.pop("bios"))

        def _parse_firmware_revision(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        firmware_revision = _parse_firmware_revision(d.pop("firmware_revision"))

        def _parse_completed(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_type_0 = isoparse(data)

                return completed_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed = _parse_completed(d.pop("completed", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        public_certificate = cls(
            canonical_id=canonical_id,
            vendor=vendor,
            platform=platform,
            configuration=configuration,
            created_at=created_at,
            release=release,
            architecture=architecture,
            kernel_version=kernel_version,
            bios=bios,
            firmware_revision=firmware_revision,
            completed=completed,
            name=name,
        )

        public_certificate.additional_properties = d
        return public_certificate

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
