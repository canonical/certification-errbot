from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.bus_enum import BusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Device")


@_attrs_define
class Device:
    """Serializer for the Device model

    Attributes:
        vendor (str):
        device_type (Union[None, str]):
        bus (Union[BlankEnum, BusEnum]):
        identifier (str):
        subsystem (Union[None, str]):
        version (Union[None, str]):
        category (Union[None, str]):
        name (Union[Unset, str]):
        subproduct_name (Union[None, Unset, str]):
        codename (Union[Unset, str]): The microarchitecture codename for the device
    """

    vendor: str
    device_type: Union[None, str]
    bus: Union[BlankEnum, BusEnum]
    identifier: str
    subsystem: Union[None, str]
    version: Union[None, str]
    category: Union[None, str]
    name: Union[Unset, str] = UNSET
    subproduct_name: Union[None, Unset, str] = UNSET
    codename: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vendor = self.vendor

        device_type: Union[None, str]
        device_type = self.device_type

        bus: str
        if isinstance(self.bus, BusEnum):
            bus = self.bus.value
        else:
            bus = self.bus.value

        identifier = self.identifier

        subsystem: Union[None, str]
        subsystem = self.subsystem

        version: Union[None, str]
        version = self.version

        category: Union[None, str]
        category = self.category

        name = self.name

        subproduct_name: Union[None, Unset, str]
        if isinstance(self.subproduct_name, Unset):
            subproduct_name = UNSET
        else:
            subproduct_name = self.subproduct_name

        codename = self.codename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vendor": vendor,
                "device_type": device_type,
                "bus": bus,
                "identifier": identifier,
                "subsystem": subsystem,
                "version": version,
                "category": category,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if subproduct_name is not UNSET:
            field_dict["subproduct_name"] = subproduct_name
        if codename is not UNSET:
            field_dict["codename"] = codename

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        vendor = d.pop("vendor")

        def _parse_device_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_type = _parse_device_type(d.pop("device_type"))

        def _parse_bus(data: object) -> Union[BlankEnum, BusEnum]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                bus_type_0 = BusEnum(data)

                return bus_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            bus_type_1 = BlankEnum(data)

            return bus_type_1

        bus = _parse_bus(d.pop("bus"))

        identifier = d.pop("identifier")

        def _parse_subsystem(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        subsystem = _parse_subsystem(d.pop("subsystem"))

        def _parse_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        version = _parse_version(d.pop("version"))

        def _parse_category(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category = _parse_category(d.pop("category"))

        name = d.pop("name", UNSET)

        def _parse_subproduct_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subproduct_name = _parse_subproduct_name(d.pop("subproduct_name", UNSET))

        codename = d.pop("codename", UNSET)

        device = cls(
            vendor=vendor,
            device_type=device_type,
            bus=bus,
            identifier=identifier,
            subsystem=subsystem,
            version=version,
            category=category,
            name=name,
            subproduct_name=subproduct_name,
            codename=codename,
        )

        device.additional_properties = d
        return device

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
