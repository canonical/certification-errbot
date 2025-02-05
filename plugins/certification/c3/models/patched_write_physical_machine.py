import datetime
import json
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.provision_type_enum import ProvisionTypeEnum
from ..models.role_enum import RoleEnum
from ..models.status_dea_enum import StatusDeaEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedWritePhysicalMachine")


@_attrs_define
class PatchedWritePhysicalMachine:
    """Serializer for writing PhysicalMachine objects.

    This serializer is intended for creating or modifying PhysicalMachine
    instances. Unlike the read serializer, ForeignKey fields are not treated
    as nested serializers. The objective is to link them to the
    PhysicalMachine, not modify them directly. Additionally, validation for
    the existence of ForeignKey instances is unnecessary, as it is left to
    the database integrity constraints.

        Attributes:
            id (Union[Unset, int]):
            account (Union[None, Unset, int]):
            arch (Union[None, Unset, int]):
            canonical_contact (Union[None, Unset, str]): The Canonical person responsible for the machine
            canonical_id (Union[None, Unset, str]):
            canonical_label (Union[Unset, str]): Unique identifier for the hardware configuration
            comment (Union[Unset, str]):
            configuration (Union[Unset, int]):
            customized_queues (Union[Unset, list[str]]):
            date_received (Union[None, Unset, datetime.date]):
            device_id (Union[None, Unset, str]):
            hardware_build (Union[Unset, str]):
            holder (Union[None, Unset, str]): The person in possession of the machine
            in_oil (Union[Unset, bool]):
            is_confidential (Union[Unset, bool]):
            launchpad_tag (Union[None, Unset, str]): The tag used in Launchpad for this machine's project
            location (Union[None, Unset, str]):
            mac_address (Union[None, Unset, str]):
            testflinger_approved (Union[Unset, bool]): The machine can be added to and used by Testflinger
            maas_node_id (Union[None, Unset, str]): The node ID assigned by MAAS
            parent (Union[None, Unset, str]):
            platform (Union[Unset, int]):
            provision_type (Union[BlankEnum, None, ProvisionTypeEnum, Unset]): The type of provisioning used for this
                machine

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
            role (Union[Unset, RoleEnum]): * `DUT` - Device Under Test
                * `Support` - Support Machine
            secure_id (Union[Unset, str]):
            serial_number (Union[Unset, str]):
            sku (Union[None, Unset, str]):
            status (Union[BlankEnum, StatusDeaEnum, Unset]):
            website (Union[None, Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    account: Union[None, Unset, int] = UNSET
    arch: Union[None, Unset, int] = UNSET
    canonical_contact: Union[None, Unset, str] = UNSET
    canonical_id: Union[None, Unset, str] = UNSET
    canonical_label: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    configuration: Union[Unset, int] = UNSET
    customized_queues: Union[Unset, list[str]] = UNSET
    date_received: Union[None, Unset, datetime.date] = UNSET
    device_id: Union[None, Unset, str] = UNSET
    hardware_build: Union[Unset, str] = UNSET
    holder: Union[None, Unset, str] = UNSET
    in_oil: Union[Unset, bool] = UNSET
    is_confidential: Union[Unset, bool] = UNSET
    launchpad_tag: Union[None, Unset, str] = UNSET
    location: Union[None, Unset, str] = UNSET
    mac_address: Union[None, Unset, str] = UNSET
    testflinger_approved: Union[Unset, bool] = UNSET
    maas_node_id: Union[None, Unset, str] = UNSET
    parent: Union[None, Unset, str] = UNSET
    platform: Union[Unset, int] = UNSET
    provision_type: Union[BlankEnum, None, ProvisionTypeEnum, Unset] = UNSET
    role: Union[Unset, RoleEnum] = UNSET
    secure_id: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    sku: Union[None, Unset, str] = UNSET
    status: Union[BlankEnum, StatusDeaEnum, Unset] = UNSET
    website: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        account: Union[None, Unset, int]
        if isinstance(self.account, Unset):
            account = UNSET
        else:
            account = self.account

        arch: Union[None, Unset, int]
        if isinstance(self.arch, Unset):
            arch = UNSET
        else:
            arch = self.arch

        canonical_contact: Union[None, Unset, str]
        if isinstance(self.canonical_contact, Unset):
            canonical_contact = UNSET
        else:
            canonical_contact = self.canonical_contact

        canonical_id: Union[None, Unset, str]
        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        else:
            canonical_id = self.canonical_id

        canonical_label = self.canonical_label

        comment = self.comment

        configuration = self.configuration

        customized_queues: Union[Unset, list[str]] = UNSET
        if not isinstance(self.customized_queues, Unset):
            customized_queues = self.customized_queues

        date_received: Union[None, Unset, str]
        if isinstance(self.date_received, Unset):
            date_received = UNSET
        elif isinstance(self.date_received, datetime.date):
            date_received = self.date_received.isoformat()
        else:
            date_received = self.date_received

        device_id: Union[None, Unset, str]
        if isinstance(self.device_id, Unset):
            device_id = UNSET
        else:
            device_id = self.device_id

        hardware_build = self.hardware_build

        holder: Union[None, Unset, str]
        if isinstance(self.holder, Unset):
            holder = UNSET
        else:
            holder = self.holder

        in_oil = self.in_oil

        is_confidential = self.is_confidential

        launchpad_tag: Union[None, Unset, str]
        if isinstance(self.launchpad_tag, Unset):
            launchpad_tag = UNSET
        else:
            launchpad_tag = self.launchpad_tag

        location: Union[None, Unset, str]
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        mac_address: Union[None, Unset, str]
        if isinstance(self.mac_address, Unset):
            mac_address = UNSET
        else:
            mac_address = self.mac_address

        testflinger_approved = self.testflinger_approved

        maas_node_id: Union[None, Unset, str]
        if isinstance(self.maas_node_id, Unset):
            maas_node_id = UNSET
        else:
            maas_node_id = self.maas_node_id

        parent: Union[None, Unset, str]
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        platform = self.platform

        provision_type: Union[None, Unset, str]
        if isinstance(self.provision_type, Unset):
            provision_type = UNSET
        elif isinstance(self.provision_type, ProvisionTypeEnum):
            provision_type = self.provision_type.value
        elif isinstance(self.provision_type, BlankEnum):
            provision_type = self.provision_type.value
        else:
            provision_type = self.provision_type

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        secure_id = self.secure_id

        serial_number = self.serial_number

        sku: Union[None, Unset, str]
        if isinstance(self.sku, Unset):
            sku = UNSET
        else:
            sku = self.sku

        status: Union[Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, StatusDeaEnum):
            status = self.status.value
        else:
            status = self.status.value

        website: Union[None, Unset, str]
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if account is not UNSET:
            field_dict["account"] = account
        if arch is not UNSET:
            field_dict["arch"] = arch
        if canonical_contact is not UNSET:
            field_dict["canonical_contact"] = canonical_contact
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if canonical_label is not UNSET:
            field_dict["canonical_label"] = canonical_label
        if comment is not UNSET:
            field_dict["comment"] = comment
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if customized_queues is not UNSET:
            field_dict["customized_queues"] = customized_queues
        if date_received is not UNSET:
            field_dict["date_received"] = date_received
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if hardware_build is not UNSET:
            field_dict["hardware_build"] = hardware_build
        if holder is not UNSET:
            field_dict["holder"] = holder
        if in_oil is not UNSET:
            field_dict["in_oil"] = in_oil
        if is_confidential is not UNSET:
            field_dict["is_confidential"] = is_confidential
        if launchpad_tag is not UNSET:
            field_dict["launchpad_tag"] = launchpad_tag
        if location is not UNSET:
            field_dict["location"] = location
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address
        if testflinger_approved is not UNSET:
            field_dict["testflinger_approved"] = testflinger_approved
        if maas_node_id is not UNSET:
            field_dict["maas_node_id"] = maas_node_id
        if parent is not UNSET:
            field_dict["parent"] = parent
        if platform is not UNSET:
            field_dict["platform"] = platform
        if provision_type is not UNSET:
            field_dict["provision_type"] = provision_type
        if role is not UNSET:
            field_dict["role"] = role
        if secure_id is not UNSET:
            field_dict["secure_id"] = secure_id
        if serial_number is not UNSET:
            field_dict["serial_number"] = serial_number
        if sku is not UNSET:
            field_dict["sku"] = sku
        if status is not UNSET:
            field_dict["status"] = status
        if website is not UNSET:
            field_dict["website"] = website

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (
            self.id
            if isinstance(self.id, Unset)
            else (None, str(self.id).encode(), "text/plain")
        )

        account: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.account, Unset):
            account = UNSET
        elif isinstance(self.account, int):
            account = (None, str(self.account).encode(), "text/plain")
        else:
            account = (None, str(self.account).encode(), "text/plain")

        arch: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.arch, Unset):
            arch = UNSET
        elif isinstance(self.arch, int):
            arch = (None, str(self.arch).encode(), "text/plain")
        else:
            arch = (None, str(self.arch).encode(), "text/plain")

        canonical_contact: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.canonical_contact, Unset):
            canonical_contact = UNSET
        elif isinstance(self.canonical_contact, str):
            canonical_contact = (
                None,
                str(self.canonical_contact).encode(),
                "text/plain",
            )
        else:
            canonical_contact = (
                None,
                str(self.canonical_contact).encode(),
                "text/plain",
            )

        canonical_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.canonical_id, Unset):
            canonical_id = UNSET
        elif isinstance(self.canonical_id, str):
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")
        else:
            canonical_id = (None, str(self.canonical_id).encode(), "text/plain")

        canonical_label = (
            self.canonical_label
            if isinstance(self.canonical_label, Unset)
            else (None, str(self.canonical_label).encode(), "text/plain")
        )

        comment = (
            self.comment
            if isinstance(self.comment, Unset)
            else (None, str(self.comment).encode(), "text/plain")
        )

        configuration = (
            self.configuration
            if isinstance(self.configuration, Unset)
            else (None, str(self.configuration).encode(), "text/plain")
        )

        customized_queues: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.customized_queues, Unset):
            _temp_customized_queues = self.customized_queues
            customized_queues = (
                None,
                json.dumps(_temp_customized_queues).encode(),
                "application/json",
            )

        date_received: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.date_received, Unset):
            date_received = UNSET
        elif isinstance(self.date_received, datetime.date):
            date_received = self.date_received.isoformat().encode()
        else:
            date_received = (None, str(self.date_received).encode(), "text/plain")

        device_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.device_id, Unset):
            device_id = UNSET
        elif isinstance(self.device_id, str):
            device_id = (None, str(self.device_id).encode(), "text/plain")
        else:
            device_id = (None, str(self.device_id).encode(), "text/plain")

        hardware_build = (
            self.hardware_build
            if isinstance(self.hardware_build, Unset)
            else (None, str(self.hardware_build).encode(), "text/plain")
        )

        holder: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.holder, Unset):
            holder = UNSET
        elif isinstance(self.holder, str):
            holder = (None, str(self.holder).encode(), "text/plain")
        else:
            holder = (None, str(self.holder).encode(), "text/plain")

        in_oil = (
            self.in_oil
            if isinstance(self.in_oil, Unset)
            else (None, str(self.in_oil).encode(), "text/plain")
        )

        is_confidential = (
            self.is_confidential
            if isinstance(self.is_confidential, Unset)
            else (None, str(self.is_confidential).encode(), "text/plain")
        )

        launchpad_tag: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.launchpad_tag, Unset):
            launchpad_tag = UNSET
        elif isinstance(self.launchpad_tag, str):
            launchpad_tag = (None, str(self.launchpad_tag).encode(), "text/plain")
        else:
            launchpad_tag = (None, str(self.launchpad_tag).encode(), "text/plain")

        location: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, str):
            location = (None, str(self.location).encode(), "text/plain")
        else:
            location = (None, str(self.location).encode(), "text/plain")

        mac_address: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.mac_address, Unset):
            mac_address = UNSET
        elif isinstance(self.mac_address, str):
            mac_address = (None, str(self.mac_address).encode(), "text/plain")
        else:
            mac_address = (None, str(self.mac_address).encode(), "text/plain")

        testflinger_approved = (
            self.testflinger_approved
            if isinstance(self.testflinger_approved, Unset)
            else (None, str(self.testflinger_approved).encode(), "text/plain")
        )

        maas_node_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.maas_node_id, Unset):
            maas_node_id = UNSET
        elif isinstance(self.maas_node_id, str):
            maas_node_id = (None, str(self.maas_node_id).encode(), "text/plain")
        else:
            maas_node_id = (None, str(self.maas_node_id).encode(), "text/plain")

        parent: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.parent, Unset):
            parent = UNSET
        elif isinstance(self.parent, str):
            parent = (None, str(self.parent).encode(), "text/plain")
        else:
            parent = (None, str(self.parent).encode(), "text/plain")

        platform = (
            self.platform
            if isinstance(self.platform, Unset)
            else (None, str(self.platform).encode(), "text/plain")
        )

        provision_type: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.provision_type, Unset):
            provision_type = UNSET
        elif isinstance(self.provision_type, ProvisionTypeEnum):
            provision_type = (
                None,
                str(self.provision_type.value).encode(),
                "text/plain",
            )
        elif isinstance(self.provision_type, BlankEnum):
            provision_type = (
                None,
                str(self.provision_type.value).encode(),
                "text/plain",
            )
        elif isinstance(self.provision_type, None):
            provision_type = (None, str(self.provision_type).encode(), "text/plain")
        else:
            provision_type = (None, str(self.provision_type).encode(), "text/plain")

        role: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.role, Unset):
            role = (None, str(self.role.value).encode(), "text/plain")

        secure_id = (
            self.secure_id
            if isinstance(self.secure_id, Unset)
            else (None, str(self.secure_id).encode(), "text/plain")
        )

        serial_number = (
            self.serial_number
            if isinstance(self.serial_number, Unset)
            else (None, str(self.serial_number).encode(), "text/plain")
        )

        sku: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.sku, Unset):
            sku = UNSET
        elif isinstance(self.sku, str):
            sku = (None, str(self.sku).encode(), "text/plain")
        else:
            sku = (None, str(self.sku).encode(), "text/plain")

        status: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, StatusDeaEnum):
            status = (None, str(self.status.value).encode(), "text/plain")
        else:
            status = (None, str(self.status.value).encode(), "text/plain")

        website: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.website, Unset):
            website = UNSET
        elif isinstance(self.website, str):
            website = (None, str(self.website).encode(), "text/plain")
        else:
            website = (None, str(self.website).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if account is not UNSET:
            field_dict["account"] = account
        if arch is not UNSET:
            field_dict["arch"] = arch
        if canonical_contact is not UNSET:
            field_dict["canonical_contact"] = canonical_contact
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if canonical_label is not UNSET:
            field_dict["canonical_label"] = canonical_label
        if comment is not UNSET:
            field_dict["comment"] = comment
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if customized_queues is not UNSET:
            field_dict["customized_queues"] = customized_queues
        if date_received is not UNSET:
            field_dict["date_received"] = date_received
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if hardware_build is not UNSET:
            field_dict["hardware_build"] = hardware_build
        if holder is not UNSET:
            field_dict["holder"] = holder
        if in_oil is not UNSET:
            field_dict["in_oil"] = in_oil
        if is_confidential is not UNSET:
            field_dict["is_confidential"] = is_confidential
        if launchpad_tag is not UNSET:
            field_dict["launchpad_tag"] = launchpad_tag
        if location is not UNSET:
            field_dict["location"] = location
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address
        if testflinger_approved is not UNSET:
            field_dict["testflinger_approved"] = testflinger_approved
        if maas_node_id is not UNSET:
            field_dict["maas_node_id"] = maas_node_id
        if parent is not UNSET:
            field_dict["parent"] = parent
        if platform is not UNSET:
            field_dict["platform"] = platform
        if provision_type is not UNSET:
            field_dict["provision_type"] = provision_type
        if role is not UNSET:
            field_dict["role"] = role
        if secure_id is not UNSET:
            field_dict["secure_id"] = secure_id
        if serial_number is not UNSET:
            field_dict["serial_number"] = serial_number
        if sku is not UNSET:
            field_dict["sku"] = sku
        if status is not UNSET:
            field_dict["status"] = status
        if website is not UNSET:
            field_dict["website"] = website

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_account(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        account = _parse_account(d.pop("account", UNSET))

        def _parse_arch(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        arch = _parse_arch(d.pop("arch", UNSET))

        def _parse_canonical_contact(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        canonical_contact = _parse_canonical_contact(d.pop("canonical_contact", UNSET))

        def _parse_canonical_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id", UNSET))

        canonical_label = d.pop("canonical_label", UNSET)

        comment = d.pop("comment", UNSET)

        configuration = d.pop("configuration", UNSET)

        customized_queues = cast(list[str], d.pop("customized_queues", UNSET))

        def _parse_date_received(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_received_type_0 = isoparse(data).date()

                return date_received_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        date_received = _parse_date_received(d.pop("date_received", UNSET))

        def _parse_device_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        device_id = _parse_device_id(d.pop("device_id", UNSET))

        hardware_build = d.pop("hardware_build", UNSET)

        def _parse_holder(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        holder = _parse_holder(d.pop("holder", UNSET))

        in_oil = d.pop("in_oil", UNSET)

        is_confidential = d.pop("is_confidential", UNSET)

        def _parse_launchpad_tag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        launchpad_tag = _parse_launchpad_tag(d.pop("launchpad_tag", UNSET))

        def _parse_location(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_mac_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mac_address = _parse_mac_address(d.pop("mac_address", UNSET))

        testflinger_approved = d.pop("testflinger_approved", UNSET)

        def _parse_maas_node_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        maas_node_id = _parse_maas_node_id(d.pop("maas_node_id", UNSET))

        def _parse_parent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        platform = d.pop("platform", UNSET)

        def _parse_provision_type(
            data: object,
        ) -> Union[BlankEnum, None, ProvisionTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provision_type_type_0 = ProvisionTypeEnum(data)

                return provision_type_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provision_type_type_1 = BlankEnum(data)

                return provision_type_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, ProvisionTypeEnum, Unset], data)

        provision_type = _parse_provision_type(d.pop("provision_type", UNSET))

        _role = d.pop("role", UNSET)
        role: Union[Unset, RoleEnum]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RoleEnum(_role)

        secure_id = d.pop("secure_id", UNSET)

        serial_number = d.pop("serial_number", UNSET)

        def _parse_sku(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sku = _parse_sku(d.pop("sku", UNSET))

        def _parse_status(data: object) -> Union[BlankEnum, StatusDeaEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = StatusDeaEnum(data)

                return status_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            status_type_1 = BlankEnum(data)

            return status_type_1

        status = _parse_status(d.pop("status", UNSET))

        def _parse_website(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        website = _parse_website(d.pop("website", UNSET))

        patched_write_physical_machine = cls(
            id=id,
            account=account,
            arch=arch,
            canonical_contact=canonical_contact,
            canonical_id=canonical_id,
            canonical_label=canonical_label,
            comment=comment,
            configuration=configuration,
            customized_queues=customized_queues,
            date_received=date_received,
            device_id=device_id,
            hardware_build=hardware_build,
            holder=holder,
            in_oil=in_oil,
            is_confidential=is_confidential,
            launchpad_tag=launchpad_tag,
            location=location,
            mac_address=mac_address,
            testflinger_approved=testflinger_approved,
            maas_node_id=maas_node_id,
            parent=parent,
            platform=platform,
            provision_type=provision_type,
            role=role,
            secure_id=secure_id,
            serial_number=serial_number,
            sku=sku,
            status=status,
            website=website,
        )

        patched_write_physical_machine.additional_properties = d
        return patched_write_physical_machine

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
