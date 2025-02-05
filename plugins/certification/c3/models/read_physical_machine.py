import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.provision_type_enum import ProvisionTypeEnum
from ..models.role_enum import RoleEnum
from ..models.status_dea_enum import StatusDeaEnum

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.launchpad_person import LaunchpadPerson
    from ..models.minimal_project import MinimalProject


T = TypeVar("T", bound="ReadPhysicalMachine")


@_attrs_define
class ReadPhysicalMachine:
    """Serializer for reading PhysicalMachine objects.

    This serializer is designed exclusively for read operations, presenting
    detailed information about PhysicalMachine instances. Nested serializers
    are used for certain fields to provide additional context without enabling
    modifications to those nested fields.

        Attributes:
            id (int):
            account (Account): Serializer for Account objects.
            arch_name (Union[None, str]):
            canonical_contact (LaunchpadPerson): Serializer for LaunchpadPerson objects.
            canonical_id (Union[None, str]):
            canonical_label (str): Unique identifier for the hardware configuration
            comment (str):
            configuration (int):
            cpu_codename (str):
            cpu_id (str): Retrieve CPU ID for a machine. Empty string is returned for an unknown value
            customized_queues (list[str]):
            date_received (Union[None, datetime.date]):
            device_id (Union[None, str]):
            hardware_build (str):
            holder (LaunchpadPerson): Serializer for LaunchpadPerson objects.
            in_oil (bool):
            is_confidential (bool):
            launchpad_tag (Union[None, str]): The tag used in Launchpad for this machine's project
            location_name (Union[None, str]):
            maas_node_id (Union[None, str]): The node ID assigned by MAAS
            mac_address (Union[None, str]):
            parent (Union[None, str]):
            platform (str):
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
            projects (list['MinimalProject']):
            resource_uri (str): Get resource_uri field
            role (RoleEnum): * `DUT` - Device Under Test
                * `Support` - Support Machine
            secure_id (str):
            serial_number (str):
            sku (Union[None, str]):
            status (StatusDeaEnum): * `Unknown` - Unknown
                * `With Canonical` - With Canonical
                * `Not yet sent` - Not yet sent
                * `In transit/Shipped` - In transit/Shipped
                * `Returned to partner/customer` - Returned to partner/customer
                * `Disposed of or destroyed` - Disposed of or destroyed
                * `Other` - Other
            testflinger_approved (bool): The machine can be added to and used by Testflinger
            website (Union[None, str]):
    """

    id: int
    account: "Account"
    arch_name: Union[None, str]
    canonical_contact: "LaunchpadPerson"
    canonical_id: Union[None, str]
    canonical_label: str
    comment: str
    configuration: int
    cpu_codename: str
    cpu_id: str
    customized_queues: list[str]
    date_received: Union[None, datetime.date]
    device_id: Union[None, str]
    hardware_build: str
    holder: "LaunchpadPerson"
    in_oil: bool
    is_confidential: bool
    launchpad_tag: Union[None, str]
    location_name: Union[None, str]
    maas_node_id: Union[None, str]
    mac_address: Union[None, str]
    parent: Union[None, str]
    platform: str
    provision_type: Union[None, ProvisionTypeEnum]
    projects: list["MinimalProject"]
    resource_uri: str
    role: RoleEnum
    secure_id: str
    serial_number: str
    sku: Union[None, str]
    status: StatusDeaEnum
    testflinger_approved: bool
    website: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        account = self.account.to_dict()

        arch_name: Union[None, str]
        arch_name = self.arch_name

        canonical_contact = self.canonical_contact.to_dict()

        canonical_id: Union[None, str]
        canonical_id = self.canonical_id

        canonical_label = self.canonical_label

        comment = self.comment

        configuration = self.configuration

        cpu_codename = self.cpu_codename

        cpu_id = self.cpu_id

        customized_queues = self.customized_queues

        date_received: Union[None, str]
        if isinstance(self.date_received, datetime.date):
            date_received = self.date_received.isoformat()
        else:
            date_received = self.date_received

        device_id: Union[None, str]
        device_id = self.device_id

        hardware_build = self.hardware_build

        holder = self.holder.to_dict()

        in_oil = self.in_oil

        is_confidential = self.is_confidential

        launchpad_tag: Union[None, str]
        launchpad_tag = self.launchpad_tag

        location_name: Union[None, str]
        location_name = self.location_name

        maas_node_id: Union[None, str]
        maas_node_id = self.maas_node_id

        mac_address: Union[None, str]
        mac_address = self.mac_address

        parent: Union[None, str]
        parent = self.parent

        platform = self.platform

        provision_type: Union[None, str]
        if isinstance(self.provision_type, ProvisionTypeEnum):
            provision_type = self.provision_type.value
        else:
            provision_type = self.provision_type

        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()
            projects.append(projects_item)

        resource_uri = self.resource_uri

        role = self.role.value

        secure_id = self.secure_id

        serial_number = self.serial_number

        sku: Union[None, str]
        sku = self.sku

        status = self.status.value

        testflinger_approved = self.testflinger_approved

        website: Union[None, str]
        website = self.website

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "account": account,
                "arch_name": arch_name,
                "canonical_contact": canonical_contact,
                "canonical_id": canonical_id,
                "canonical_label": canonical_label,
                "comment": comment,
                "configuration": configuration,
                "cpu_codename": cpu_codename,
                "cpu_id": cpu_id,
                "customized_queues": customized_queues,
                "date_received": date_received,
                "device_id": device_id,
                "hardware_build": hardware_build,
                "holder": holder,
                "in_oil": in_oil,
                "is_confidential": is_confidential,
                "launchpad_tag": launchpad_tag,
                "location_name": location_name,
                "maas_node_id": maas_node_id,
                "mac_address": mac_address,
                "parent": parent,
                "platform": platform,
                "provision_type": provision_type,
                "projects": projects,
                "resource_uri": resource_uri,
                "role": role,
                "secure_id": secure_id,
                "serial_number": serial_number,
                "sku": sku,
                "status": status,
                "testflinger_approved": testflinger_approved,
                "website": website,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.launchpad_person import LaunchpadPerson
        from ..models.minimal_project import MinimalProject

        d = src_dict.copy()
        id = d.pop("id")

        account = Account.from_dict(d.pop("account"))

        def _parse_arch_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        arch_name = _parse_arch_name(d.pop("arch_name"))

        canonical_contact = LaunchpadPerson.from_dict(d.pop("canonical_contact"))

        def _parse_canonical_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id"))

        canonical_label = d.pop("canonical_label")

        comment = d.pop("comment")

        configuration = d.pop("configuration")

        cpu_codename = d.pop("cpu_codename")

        cpu_id = d.pop("cpu_id")

        customized_queues = cast(list[str], d.pop("customized_queues"))

        def _parse_date_received(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_received_type_0 = isoparse(data).date()

                return date_received_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        date_received = _parse_date_received(d.pop("date_received"))

        def _parse_device_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        device_id = _parse_device_id(d.pop("device_id"))

        hardware_build = d.pop("hardware_build")

        holder = LaunchpadPerson.from_dict(d.pop("holder"))

        in_oil = d.pop("in_oil")

        is_confidential = d.pop("is_confidential")

        def _parse_launchpad_tag(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        launchpad_tag = _parse_launchpad_tag(d.pop("launchpad_tag"))

        def _parse_location_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        location_name = _parse_location_name(d.pop("location_name"))

        def _parse_maas_node_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        maas_node_id = _parse_maas_node_id(d.pop("maas_node_id"))

        def _parse_mac_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mac_address = _parse_mac_address(d.pop("mac_address"))

        def _parse_parent(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent = _parse_parent(d.pop("parent"))

        platform = d.pop("platform")

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

        projects = []
        _projects = d.pop("projects")
        for projects_item_data in _projects:
            projects_item = MinimalProject.from_dict(projects_item_data)

            projects.append(projects_item)

        resource_uri = d.pop("resource_uri")

        role = RoleEnum(d.pop("role"))

        secure_id = d.pop("secure_id")

        serial_number = d.pop("serial_number")

        def _parse_sku(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sku = _parse_sku(d.pop("sku"))

        status = StatusDeaEnum(d.pop("status"))

        testflinger_approved = d.pop("testflinger_approved")

        def _parse_website(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        website = _parse_website(d.pop("website"))

        read_physical_machine = cls(
            id=id,
            account=account,
            arch_name=arch_name,
            canonical_contact=canonical_contact,
            canonical_id=canonical_id,
            canonical_label=canonical_label,
            comment=comment,
            configuration=configuration,
            cpu_codename=cpu_codename,
            cpu_id=cpu_id,
            customized_queues=customized_queues,
            date_received=date_received,
            device_id=device_id,
            hardware_build=hardware_build,
            holder=holder,
            in_oil=in_oil,
            is_confidential=is_confidential,
            launchpad_tag=launchpad_tag,
            location_name=location_name,
            maas_node_id=maas_node_id,
            mac_address=mac_address,
            parent=parent,
            platform=platform,
            provision_type=provision_type,
            projects=projects,
            resource_uri=resource_uri,
            role=role,
            secure_id=secure_id,
            serial_number=serial_number,
            sku=sku,
            status=status,
            testflinger_approved=testflinger_approved,
            website=website,
        )

        read_physical_machine.additional_properties = d
        return read_physical_machine

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
