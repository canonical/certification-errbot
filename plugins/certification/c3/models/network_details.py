from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.provision_type_enum import ProvisionTypeEnum

if TYPE_CHECKING:
    from ..models.lab_resource import LabResource


T = TypeVar("T", bound="NetworkDetails")


@_attrs_define
class NetworkDetails:
    """Serializer for fetching network details for every
    Lab Resource in a datacentre

        Attributes:
            account (Union[None, str]):
            platform (Union[None, str]):
            mac_address (Union[None, str]):
            device_id (Union[None, str]):
            provision_type (Union[None, ProvisionTypeEnum]): The type of provisioning used for this machine

                * `noprovision` - None
                * `maas` - MAAS
                * `muxpi` - MuxPi
                * `sdwire` - SD-Wire
                * `netboot` - Netboot
                * `rpi3` - Raspberry Pi 3
                * `cm3` - Raspberry Pi Compute Module 3
                * `zapper_iot` - Zapper IoT
                * `zapper_kvm` - Zapper KVM
                * `oem_autoinstall` - OEM Autoinstall
                * `oemrecovery` - OEM Recovery
                * `oemscript` - OEM Script
                * `dell_oemscript` - Dell OEM Script
                * `hp_oemscript` - HP OEM Script
                * `lenovo_oemscript` - Lenovo OEM Script
            maas_node_id (Union[None, str]): The node ID assigned by MAAS
            customized_queues (list[str]):
            labresource (LabResource): Serializer for fetching Lab Resource for a physical machine
            controller_platform (Union[None, str]): Get platform name field from support machine
            child_canonical_id (Union[None, str]): Get canonical_id field from support machine
            controller_mac_address (Union[None, str]): Get mac_address field from support machine
            controller_ip_address (Union[None, str]): Get ip_address field from support machine
            secure_id (str):
            testflinger_approved (bool): The machine can be added to and used by Testflinger
    """

    account: Union[None, str]
    platform: Union[None, str]
    mac_address: Union[None, str]
    device_id: Union[None, str]
    provision_type: Union[None, ProvisionTypeEnum]
    maas_node_id: Union[None, str]
    customized_queues: list[str]
    labresource: "LabResource"
    controller_platform: Union[None, str]
    child_canonical_id: Union[None, str]
    controller_mac_address: Union[None, str]
    controller_ip_address: Union[None, str]
    secure_id: str
    testflinger_approved: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account: Union[None, str]
        account = self.account

        platform: Union[None, str]
        platform = self.platform

        mac_address: Union[None, str]
        mac_address = self.mac_address

        device_id: Union[None, str]
        device_id = self.device_id

        provision_type: Union[None, str]
        if isinstance(self.provision_type, ProvisionTypeEnum):
            provision_type = self.provision_type.value
        else:
            provision_type = self.provision_type

        maas_node_id: Union[None, str]
        maas_node_id = self.maas_node_id

        customized_queues = self.customized_queues

        labresource = self.labresource.to_dict()

        controller_platform: Union[None, str]
        controller_platform = self.controller_platform

        child_canonical_id: Union[None, str]
        child_canonical_id = self.child_canonical_id

        controller_mac_address: Union[None, str]
        controller_mac_address = self.controller_mac_address

        controller_ip_address: Union[None, str]
        controller_ip_address = self.controller_ip_address

        secure_id = self.secure_id

        testflinger_approved = self.testflinger_approved

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "platform": platform,
                "mac_address": mac_address,
                "device_id": device_id,
                "provision_type": provision_type,
                "maas_node_id": maas_node_id,
                "customized_queues": customized_queues,
                "labresource": labresource,
                "controller_platform": controller_platform,
                "child_canonical_id": child_canonical_id,
                "controller_mac_address": controller_mac_address,
                "controller_ip_address": controller_ip_address,
                "secure_id": secure_id,
                "testflinger_approved": testflinger_approved,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.lab_resource import LabResource

        d = src_dict.copy()

        def _parse_account(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        account = _parse_account(d.pop("account"))

        def _parse_platform(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        platform = _parse_platform(d.pop("platform"))

        def _parse_mac_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mac_address = _parse_mac_address(d.pop("mac_address"))

        def _parse_device_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_id = _parse_device_id(d.pop("device_id"))

        def _parse_provision_type(data: object) -> Union[None, ProvisionTypeEnum]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provision_type_type_0 = ProvisionTypeEnum(data)

                return provision_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ProvisionTypeEnum], data)

        provision_type = _parse_provision_type(d.pop("provision_type"))

        def _parse_maas_node_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        maas_node_id = _parse_maas_node_id(d.pop("maas_node_id"))

        customized_queues = cast(list[str], d.pop("customized_queues"))

        labresource = LabResource.from_dict(d.pop("labresource"))

        def _parse_controller_platform(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        controller_platform = _parse_controller_platform(d.pop("controller_platform"))

        def _parse_child_canonical_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        child_canonical_id = _parse_child_canonical_id(d.pop("child_canonical_id"))

        def _parse_controller_mac_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        controller_mac_address = _parse_controller_mac_address(
            d.pop("controller_mac_address")
        )

        def _parse_controller_ip_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        controller_ip_address = _parse_controller_ip_address(
            d.pop("controller_ip_address")
        )

        secure_id = d.pop("secure_id")

        testflinger_approved = d.pop("testflinger_approved")

        network_details = cls(
            account=account,
            platform=platform,
            mac_address=mac_address,
            device_id=device_id,
            provision_type=provision_type,
            maas_node_id=maas_node_id,
            customized_queues=customized_queues,
            labresource=labresource,
            controller_platform=controller_platform,
            child_canonical_id=child_canonical_id,
            controller_mac_address=controller_mac_address,
            controller_ip_address=controller_ip_address,
            secure_id=secure_id,
            testflinger_approved=testflinger_approved,
        )

        network_details.additional_properties = d
        return network_details

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
