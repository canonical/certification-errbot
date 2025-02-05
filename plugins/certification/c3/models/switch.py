import json
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.make_enum import MakeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.minimized_port import MinimizedPort


T = TypeVar("T", bound="Switch")


@_attrs_define
class Switch:
    """Serializer for Network Switch objects

    Attributes:
        id (int):
        datacentre (int):
        make (MakeEnum): * `48p-ethernet` - 48 Port Ethernet Switch
            * `24p-ethernet` - 24 Port Ethernet Switch
            * `24p-poe` - 24 Port PoE Switch
            * `48p-poe` - 48 Port PoE Switch
            * `32p-100g-ethernet` - 32 Port 100G Ethernet Switch
            * `48p-10g-4p-100g-ethernet` - 48x10G + 4x100G Ethernet Switch
        ports (list['MinimizedPort']):
        name (Union[None, Unset, str]):
        ip (Union[None, Unset, str]):
    """

    id: int
    datacentre: int
    make: MakeEnum
    ports: list["MinimizedPort"]
    name: Union[None, Unset, str] = UNSET
    ip: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        datacentre = self.datacentre

        make = self.make.value

        ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            ports.append(ports_item)

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        ip: Union[None, Unset, str]
        if isinstance(self.ip, Unset):
            ip = UNSET
        else:
            ip = self.ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "datacentre": datacentre,
                "make": make,
                "ports": ports,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if ip is not UNSET:
            field_dict["ip"] = ip

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        datacentre = (None, str(self.datacentre).encode(), "text/plain")

        make = (None, str(self.make.value).encode(), "text/plain")

        _temp_ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            _temp_ports.append(ports_item)
        ports = (None, json.dumps(_temp_ports).encode(), "application/json")

        name: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, str):
            name = (None, str(self.name).encode(), "text/plain")
        else:
            name = (None, str(self.name).encode(), "text/plain")

        ip: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.ip, Unset):
            ip = UNSET
        elif isinstance(self.ip, str):
            ip = (None, str(self.ip).encode(), "text/plain")
        else:
            ip = (None, str(self.ip).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "datacentre": datacentre,
                "make": make,
                "ports": ports,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if ip is not UNSET:
            field_dict["ip"] = ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.minimized_port import MinimizedPort

        d = src_dict.copy()
        id = d.pop("id")

        datacentre = d.pop("datacentre")

        make = MakeEnum(d.pop("make"))

        ports = []
        _ports = d.pop("ports")
        for ports_item_data in _ports:
            ports_item = MinimizedPort.from_dict(ports_item_data)

            ports.append(ports_item)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip = _parse_ip(d.pop("ip", UNSET))

        switch = cls(
            id=id,
            datacentre=datacentre,
            make=make,
            ports=ports,
            name=name,
            ip=ip,
        )

        switch.additional_properties = d
        return switch

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
