import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PhysicalMachineView")


@_attrs_define
class PhysicalMachineView:
    """Serializer for PhysicalMachineView objects

    Duplicates the behaviour of certifiedmodels v2 API endpoint with additional
    filter by status and contains private hardware as well

        Attributes:
            arch (str):
            canonical_id (str):
            category (str):
            completed (Union[None, datetime.datetime]):
            major_release (str):
            make (str):
            model (str):
            mac_address (Union[None, str]):
            maas_node_id (Union[None, str]):
            release (str):
            resource_uri (str):
            cert_level (str):
            cert_status (str):
            enablement_status (str):
            tf_provision_type (Union[None, str]):
            testflinger_state (Union[None, str]):
            queues (Union[None, str]):
            requested_provision_type (Union[None, str]):
    """

    arch: str
    canonical_id: str
    category: str
    completed: Union[None, datetime.datetime]
    major_release: str
    make: str
    model: str
    mac_address: Union[None, str]
    maas_node_id: Union[None, str]
    release: str
    resource_uri: str
    cert_level: str
    cert_status: str
    enablement_status: str
    tf_provision_type: Union[None, str]
    testflinger_state: Union[None, str]
    queues: Union[None, str]
    requested_provision_type: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arch = self.arch

        canonical_id = self.canonical_id

        category = self.category

        completed: Union[None, str]
        if isinstance(self.completed, datetime.datetime):
            completed = self.completed.isoformat()
        else:
            completed = self.completed

        major_release = self.major_release

        make = self.make

        model = self.model

        mac_address: Union[None, str]
        mac_address = self.mac_address

        maas_node_id: Union[None, str]
        maas_node_id = self.maas_node_id

        release = self.release

        resource_uri = self.resource_uri

        cert_level = self.cert_level

        cert_status = self.cert_status

        enablement_status = self.enablement_status

        tf_provision_type: Union[None, str]
        tf_provision_type = self.tf_provision_type

        testflinger_state: Union[None, str]
        testflinger_state = self.testflinger_state

        queues: Union[None, str]
        queues = self.queues

        requested_provision_type: Union[None, str]
        requested_provision_type = self.requested_provision_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "arch": arch,
                "canonical_id": canonical_id,
                "category": category,
                "completed": completed,
                "major_release": major_release,
                "make": make,
                "model": model,
                "mac_address": mac_address,
                "maas_node_id": maas_node_id,
                "release": release,
                "resource_uri": resource_uri,
                "cert_level": cert_level,
                "cert_status": cert_status,
                "enablement_status": enablement_status,
                "tf_provision_type": tf_provision_type,
                "testflinger_state": testflinger_state,
                "queues": queues,
                "requested_provision_type": requested_provision_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        arch = d.pop("arch")

        canonical_id = d.pop("canonical_id")

        category = d.pop("category")

        def _parse_completed(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_type_0 = isoparse(data)

                return completed_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        completed = _parse_completed(d.pop("completed"))

        major_release = d.pop("major_release")

        make = d.pop("make")

        model = d.pop("model")

        def _parse_mac_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mac_address = _parse_mac_address(d.pop("mac_address"))

        def _parse_maas_node_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        maas_node_id = _parse_maas_node_id(d.pop("maas_node_id"))

        release = d.pop("release")

        resource_uri = d.pop("resource_uri")

        cert_level = d.pop("cert_level")

        cert_status = d.pop("cert_status")

        enablement_status = d.pop("enablement_status")

        def _parse_tf_provision_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tf_provision_type = _parse_tf_provision_type(d.pop("tf_provision_type"))

        def _parse_testflinger_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        testflinger_state = _parse_testflinger_state(d.pop("testflinger_state"))

        def _parse_queues(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        queues = _parse_queues(d.pop("queues"))

        def _parse_requested_provision_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        requested_provision_type = _parse_requested_provision_type(
            d.pop("requested_provision_type")
        )

        physical_machine_view = cls(
            arch=arch,
            canonical_id=canonical_id,
            category=category,
            completed=completed,
            major_release=major_release,
            make=make,
            model=model,
            mac_address=mac_address,
            maas_node_id=maas_node_id,
            release=release,
            resource_uri=resource_uri,
            cert_level=cert_level,
            cert_status=cert_status,
            enablement_status=enablement_status,
            tf_provision_type=tf_provision_type,
            testflinger_state=testflinger_state,
            queues=queues,
            requested_provision_type=requested_provision_type,
        )

        physical_machine_view.additional_properties = d
        return physical_machine_view

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
