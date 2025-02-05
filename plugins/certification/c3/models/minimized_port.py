from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MinimizedPort")


@_attrs_define
class MinimizedPort:
    """Serializer for Network Switch Port objects

    Attributes:
        reserved (bool): Return True if current port is associated to a LabResource
        machine (Union[None, str]):
        mac_address (Union[None, str]):
        port (int):
    """

    reserved: bool
    machine: Union[None, str]
    mac_address: Union[None, str]
    port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reserved = self.reserved

        machine: Union[None, str]
        machine = self.machine

        mac_address: Union[None, str]
        mac_address = self.mac_address

        port = self.port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reserved": reserved,
                "machine": machine,
                "mac_address": mac_address,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        reserved = d.pop("reserved")

        def _parse_machine(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        machine = _parse_machine(d.pop("machine"))

        def _parse_mac_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mac_address = _parse_mac_address(d.pop("mac_address"))

        port = d.pop("port")

        minimized_port = cls(
            reserved=reserved,
            machine=machine,
            mac_address=mac_address,
            port=port,
        )

        minimized_port.additional_properties = d
        return minimized_port

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
