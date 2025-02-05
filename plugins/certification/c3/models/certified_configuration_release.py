from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CertifiedConfigurationRelease")


@_attrs_define
class CertifiedConfigurationRelease:
    """Serializer for the Certified Configuration Release objects

    Certified Configuration Releases are releases with at least one certified
    configuration.

        Attributes:
            release (Union[Unset, str]):
            desktops (Union[None, Unset, int]):
            laptops (Union[None, Unset, int]):
            servers (Union[None, Unset, int]):
            soc (Union[None, Unset, int]):
            smart_core (Union[None, Unset, int]):
            total (Union[None, Unset, int]):
    """

    release: Union[Unset, str] = UNSET
    desktops: Union[None, Unset, int] = UNSET
    laptops: Union[None, Unset, int] = UNSET
    servers: Union[None, Unset, int] = UNSET
    soc: Union[None, Unset, int] = UNSET
    smart_core: Union[None, Unset, int] = UNSET
    total: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        release = self.release

        desktops: Union[None, Unset, int]
        if isinstance(self.desktops, Unset):
            desktops = UNSET
        else:
            desktops = self.desktops

        laptops: Union[None, Unset, int]
        if isinstance(self.laptops, Unset):
            laptops = UNSET
        else:
            laptops = self.laptops

        servers: Union[None, Unset, int]
        if isinstance(self.servers, Unset):
            servers = UNSET
        else:
            servers = self.servers

        soc: Union[None, Unset, int]
        if isinstance(self.soc, Unset):
            soc = UNSET
        else:
            soc = self.soc

        smart_core: Union[None, Unset, int]
        if isinstance(self.smart_core, Unset):
            smart_core = UNSET
        else:
            smart_core = self.smart_core

        total: Union[None, Unset, int]
        if isinstance(self.total, Unset):
            total = UNSET
        else:
            total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if release is not UNSET:
            field_dict["release"] = release
        if desktops is not UNSET:
            field_dict["desktops"] = desktops
        if laptops is not UNSET:
            field_dict["laptops"] = laptops
        if servers is not UNSET:
            field_dict["servers"] = servers
        if soc is not UNSET:
            field_dict["soc"] = soc
        if smart_core is not UNSET:
            field_dict["smart_core"] = smart_core
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        release = d.pop("release", UNSET)

        def _parse_desktops(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        desktops = _parse_desktops(d.pop("desktops", UNSET))

        def _parse_laptops(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        laptops = _parse_laptops(d.pop("laptops", UNSET))

        def _parse_servers(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        servers = _parse_servers(d.pop("servers", UNSET))

        def _parse_soc(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        soc = _parse_soc(d.pop("soc", UNSET))

        def _parse_smart_core(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        smart_core = _parse_smart_core(d.pop("smart_core", UNSET))

        def _parse_total(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total = _parse_total(d.pop("total", UNSET))

        certified_configuration_release = cls(
            release=release,
            desktops=desktops,
            laptops=laptops,
            servers=servers,
            soc=soc,
            smart_core=smart_core,
            total=total,
        )

        certified_configuration_release.additional_properties = d
        return certified_configuration_release

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
