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


T = TypeVar("T", bound="PatchedLabResource")


@_attrs_define
class PatchedLabResource:
    """Serializer for fetching Lab Resource for a physical machine

    Attributes:
        id (Union[Unset, int]):
        canonical_id (Union[None, Unset, str]):
        role (Union[Unset, RoleEnum]): * `DUT` - Device Under Test
            * `Support` - Support Machine
        datacentre (Union[None, Unset, str]):
        locations (Union[Unset, list['LocationUnit']]):
        outlets (Union[Unset, list['Outlet']]):
        ports (Union[Unset, list['Port']]):
        ip_address (Union[None, Unset, str]):
        maas_server (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    canonical_id: Union[None, Unset, str] = UNSET
    role: Union[Unset, RoleEnum] = UNSET
    datacentre: Union[None, Unset, str] = UNSET
    locations: Union[Unset, list["LocationUnit"]] = UNSET
    outlets: Union[Unset, list["Outlet"]] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    ip_address: Union[None, Unset, str] = UNSET
    maas_server: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        canonical_id: Union[None, Unset, str]
        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        else:
            canonical_id = self.canonical_id

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        datacentre: Union[None, Unset, str]
        if isinstance(self.datacentre, Unset):
            datacentre = UNSET
        else:
            datacentre = self.datacentre

        locations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.locations, Unset):
            locations = []
            for locations_item_data in self.locations:
                locations_item = locations_item_data.to_dict()
                locations.append(locations_item)

        outlets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.outlets, Unset):
            outlets = []
            for outlets_item_data in self.outlets:
                outlets_item = outlets_item_data.to_dict()
                outlets.append(outlets_item)

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                ports.append(ports_item)

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
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if role is not UNSET:
            field_dict["role"] = role
        if datacentre is not UNSET:
            field_dict["datacentre"] = datacentre
        if locations is not UNSET:
            field_dict["locations"] = locations
        if outlets is not UNSET:
            field_dict["outlets"] = outlets
        if ports is not UNSET:
            field_dict["ports"] = ports
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if maas_server is not UNSET:
            field_dict["maas_server"] = maas_server

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (
            self.id
            if isinstance(self.id, Unset)
            else (None, str(self.id).encode(), "text/plain")
        )

        canonical_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        elif isinstance(self.canonical_id, str):
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")
        else:
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")

        role: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.role, Unset):
            role = (None, str(self.role.value).encode(), "text/plain")

        datacentre: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.datacentre, Unset):
            datacentre = UNSET
        elif isinstance(self.datacentre, str):
            datacentre = (None, str(self.datacentre).encode(), "text/plain")
        else:
            datacentre = (None, str(self.datacentre).encode(), "text/plain")

        locations: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.locations, Unset):
            _temp_locations = []
            for locations_item_data in self.locations:
                locations_item = locations_item_data.to_dict()
                _temp_locations.append(locations_item)
            locations = (None, json.dumps(_temp_locations).encode(), "application/json")

        outlets: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.outlets, Unset):
            _temp_outlets = []
            for outlets_item_data in self.outlets:
                outlets_item = outlets_item_data.to_dict()
                _temp_outlets.append(outlets_item)
            outlets = (None, json.dumps(_temp_outlets).encode(), "application/json")

        ports: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.ports, Unset):
            _temp_ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                _temp_ports.append(ports_item)
            ports = (None, json.dumps(_temp_ports).encode(), "application/json")

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

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if role is not UNSET:
            field_dict["role"] = role
        if datacentre is not UNSET:
            field_dict["datacentre"] = datacentre
        if locations is not UNSET:
            field_dict["locations"] = locations
        if outlets is not UNSET:
            field_dict["outlets"] = outlets
        if ports is not UNSET:
            field_dict["ports"] = ports
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
        id = d.pop("id", UNSET)

        def _parse_canonical_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id", UNSET))

        _role = d.pop("role", UNSET)
        role: Union[Unset, RoleEnum]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RoleEnum(_role)

        def _parse_datacentre(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        datacentre = _parse_datacentre(d.pop("datacentre", UNSET))

        locations = []
        _locations = d.pop("locations", UNSET)
        for locations_item_data in _locations or []:
            locations_item = LocationUnit.from_dict(locations_item_data)

            locations.append(locations_item)

        outlets = []
        _outlets = d.pop("outlets", UNSET)
        for outlets_item_data in _outlets or []:
            outlets_item = Outlet.from_dict(outlets_item_data)

            outlets.append(outlets_item)

        ports = []
        _ports = d.pop("ports", UNSET)
        for ports_item_data in _ports or []:
            ports_item = Port.from_dict(ports_item_data)

            ports.append(ports_item)

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

        patched_lab_resource = cls(
            id=id,
            canonical_id=canonical_id,
            role=role,
            datacentre=datacentre,
            locations=locations,
            outlets=outlets,
            ports=ports,
            ip_address=ip_address,
            maas_server=maas_server,
        )

        patched_lab_resource.additional_properties = d
        return patched_lab_resource

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
