import json
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role_enum import RoleEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_unit import LocationUnit
    from ..models.outlet import Outlet
    from ..models.port import Port


T = TypeVar("T", bound="LabResource")


@_attrs_define
class LabResource:
    """Serializer for fetching Lab Resource for a physical machine

    Attributes:
        id (int):
        role (RoleEnum): * `DUT` - Device Under Test
            * `Support` - Support Machine
        datacentre (Union[None, str]):
        locations (list['LocationUnit']):
        outlets (list['Outlet']):
        ports (list['Port']):
        canonical_id (Union[None, Unset, str]):
        ip_address (Union[None, Unset, str]):
        maas_server (Union[None, Unset, str]):
    """

    id: int
    role: RoleEnum
    datacentre: Union[None, str]
    locations: list["LocationUnit"]
    outlets: list["Outlet"]
    ports: list["Port"]
    canonical_id: Union[None, Unset, str] = UNSET
    ip_address: Union[None, Unset, str] = UNSET
    maas_server: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        role = self.role.value

        datacentre: Union[None, str]
        datacentre = self.datacentre

        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()
            locations.append(locations_item)

        outlets = []
        for outlets_item_data in self.outlets:
            outlets_item = outlets_item_data.to_dict()
            outlets.append(outlets_item)

        ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            ports.append(ports_item)

        canonical_id: Union[None, Unset, str]
        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        else:
            canonical_id = self.canonical_id

        ip_address: Union[None, Unset, str]
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        maas_server: Union[None, Unset, str]
        if isinstance(self.maas_server, Unset):
            maas_server = UNSET
        else:
            maas_server = self.maas_server

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "role": role,
                "datacentre": datacentre,
                "locations": locations,
                "outlets": outlets,
                "ports": ports,
            }
        )
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if maas_server is not UNSET:
            field_dict["maas_server"] = maas_server

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        role = (None, str(self.role.value).encode(), "text/plain")

        datacentre: tuple[None, bytes, str]

        if isinstance(self.datacentre, str):
            datacentre = (None, str(self.datacentre).encode(), "text/plain")
        else:
            datacentre = (None, str(self.datacentre).encode(), "text/plain")

        _temp_locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()
            _temp_locations.append(locations_item)
        locations = (None, json.dumps(_temp_locations).encode(), "application/json")

        _temp_outlets = []
        for outlets_item_data in self.outlets:
            outlets_item = outlets_item_data.to_dict()
            _temp_outlets.append(outlets_item)
        outlets = (None, json.dumps(_temp_outlets).encode(), "application/json")

        _temp_ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            _temp_ports.append(ports_item)
        ports = (None, json.dumps(_temp_ports).encode(), "application/json")

        canonical_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        elif isinstance(self.canonical_id, str):
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")
        else:
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")

        ip_address: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        elif isinstance(self.ip_address, str):
            ip_address = (None, str(self.ip_address).encode(), "text/plain")
        else:
            ip_address = (None, str(self.ip_address).encode(), "text/plain")

        maas_server: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.maas_server, Unset):
            maas_server = UNSET
        elif isinstance(self.maas_server, str):
            maas_server = (None, str(self.maas_server).encode(), "text/plain")
        else:
            maas_server = (None, str(self.maas_server).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "role": role,
                "datacentre": datacentre,
                "locations": locations,
                "outlets": outlets,
                "ports": ports,
            }
        )
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if maas_server is not UNSET:
            field_dict["maas_server"] = maas_server

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.location_unit import LocationUnit
        from ..models.outlet import Outlet
        from ..models.port import Port

        d = src_dict.copy()
        id = d.pop("id")

        role = RoleEnum(d.pop("role"))

        def _parse_datacentre(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        datacentre = _parse_datacentre(d.pop("datacentre"))

        locations = []
        _locations = d.pop("locations")
        for locations_item_data in _locations:
            locations_item = LocationUnit.from_dict(locations_item_data)

            locations.append(locations_item)

        outlets = []
        _outlets = d.pop("outlets")
        for outlets_item_data in _outlets:
            outlets_item = Outlet.from_dict(outlets_item_data)

            outlets.append(outlets_item)

        ports = []
        _ports = d.pop("ports")
        for ports_item_data in _ports:
            ports_item = Port.from_dict(ports_item_data)

            ports.append(ports_item)

        def _parse_canonical_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id", UNSET))

        def _parse_ip_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        def _parse_maas_server(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        maas_server = _parse_maas_server(d.pop("maas_server", UNSET))

        lab_resource = cls(
            id=id,
            role=role,
            datacentre=datacentre,
            locations=locations,
            outlets=outlets,
            ports=ports,
            canonical_id=canonical_id,
            ip_address=ip_address,
            maas_server=maas_server,
        )

        lab_resource.additional_properties = d
        return lab_resource

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
