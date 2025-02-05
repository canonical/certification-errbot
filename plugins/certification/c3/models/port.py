from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Port")


@_attrs_define
class Port:
    """Serializer for Network Switch Port objects

    Attributes:
        switch_make (Union[None, str]):
        switch_ip (Union[None, str]):
        port (int):
    """

    switch_make: Union[None, str]
    switch_ip: Union[None, str]
    port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        switch_make: Union[None, str]
        switch_make = self.switch_make

        switch_ip: Union[None, str]
        switch_ip = self.switch_ip

        port = self.port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "switch_make": switch_make,
                "switch_ip": switch_ip,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_switch_make(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        switch_make = _parse_switch_make(d.pop("switch_make"))

        def _parse_switch_ip(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        switch_ip = _parse_switch_ip(d.pop("switch_ip"))

        port = d.pop("port")

        port = cls(
            switch_make=switch_make,
            switch_ip=switch_ip,
            port=port,
        )

        port.additional_properties = d
        return port

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
