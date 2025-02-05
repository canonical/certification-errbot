"""Contains all the data models used in inputs/outputs"""

from .account import Account
from .bios import Bios
from .blank_enum import BlankEnum
from .bus_enum import BusEnum
from .certified_configuration import CertifiedConfiguration
from .certified_configuration_details import CertifiedConfigurationDetails
from .certified_configuration_details_network_item import (
    CertifiedConfigurationDetailsNetworkItem,
)
from .certified_configuration_details_notes_item import (
    CertifiedConfigurationDetailsNotesItem,
)
from .certified_configuration_details_processor_item import (
    CertifiedConfigurationDetailsProcessorItem,
)
from .certified_configuration_details_video_item import (
    CertifiedConfigurationDetailsVideoItem,
)
from .certified_configuration_details_wireless_item import (
    CertifiedConfigurationDetailsWirelessItem,
)
from .certified_configuration_device import CertifiedConfigurationDevice
from .certified_configuration_release import CertifiedConfigurationRelease
from .certified_platform import CertifiedPlatform
from .certified_platform_certificates import CertifiedPlatformCertificates
from .certified_vendor import CertifiedVendor
from .component_release_status import ComponentReleaseStatus
from .component_release_status_status_enum import ComponentReleaseStatusStatusEnum
from .component_summaries import ComponentSummaries
from .configuration import Configuration
from .configuration_mtm_type_0 import ConfigurationMtmType0
from .cpu_info import CPUInfo
from .datacentre import Datacentre
from .datacentre_env_var_type_0 import DatacentreEnvVarType0
from .device import Device
from .image import Image
from .lab_resource import LabResource
from .launchpad_person import LaunchpadPerson
from .level_enum import LevelEnum
from .location_unit import LocationUnit
from .machine_report import MachineReport
from .machine_report_cpu import MachineReportCpu
from .machine_report_cpu_additional_property import MachineReportCpuAdditionalProperty
from .machine_report_devices import MachineReportDevices
from .machine_report_devices_additional_property_item import (
    MachineReportDevicesAdditionalPropertyItem,
)
from .machine_report_memory import MachineReportMemory
from .make_enum import MakeEnum
from .minimal_project import MinimalProject
from .minimized_port import MinimizedPort
from .network_details import NetworkDetails
from .outlet import Outlet
from .paginated_report_summary_base_list import PaginatedReportSummaryBaseList
from .paginated_submission_list import PaginatedSubmissionList
from .paginated_switch_list import PaginatedSwitchList
from .patched_configuration import PatchedConfiguration
from .patched_configuration_mtm_type_0 import PatchedConfigurationMtmType0
from .patched_image import PatchedImage
from .patched_lab_resource import PatchedLabResource
from .patched_platform import PatchedPlatform
from .patched_write_physical_machine import PatchedWritePhysicalMachine
from .patched_write_project import PatchedWriteProject
from .physical_machine_view import PhysicalMachineView
from .platform import Platform
from .port import Port
from .provision_type_enum import ProvisionTypeEnum
from .public_certificate import PublicCertificate
from .public_device_instance import PublicDeviceInstance
from .public_release import PublicRelease
from .read_physical_machine import ReadPhysicalMachine
from .read_project import ReadProject
from .report_summary_base import ReportSummaryBase
from .report_summary_base_rejected_jobs import ReportSummaryBaseRejectedJobs
from .role_enum import RoleEnum
from .status_dea_enum import StatusDeaEnum
from .submission import Submission
from .switch import Switch
from .test_result import TestResult
from .write_physical_machine import WritePhysicalMachine
from .write_project import WriteProject

__all__ = (
    "Account",
    "Bios",
    "BlankEnum",
    "BusEnum",
    "CertifiedConfiguration",
    "CertifiedConfigurationDetails",
    "CertifiedConfigurationDetailsNetworkItem",
    "CertifiedConfigurationDetailsNotesItem",
    "CertifiedConfigurationDetailsProcessorItem",
    "CertifiedConfigurationDetailsVideoItem",
    "CertifiedConfigurationDetailsWirelessItem",
    "CertifiedConfigurationDevice",
    "CertifiedConfigurationRelease",
    "CertifiedPlatform",
    "CertifiedPlatformCertificates",
    "CertifiedVendor",
    "ComponentReleaseStatus",
    "ComponentReleaseStatusStatusEnum",
    "ComponentSummaries",
    "Configuration",
    "ConfigurationMtmType0",
    "CPUInfo",
    "Datacentre",
    "DatacentreEnvVarType0",
    "Device",
    "Image",
    "LabResource",
    "LaunchpadPerson",
    "LevelEnum",
    "LocationUnit",
    "MachineReport",
    "MachineReportCpu",
    "MachineReportCpuAdditionalProperty",
    "MachineReportDevices",
    "MachineReportDevicesAdditionalPropertyItem",
    "MachineReportMemory",
    "MakeEnum",
    "MinimalProject",
    "MinimizedPort",
    "NetworkDetails",
    "Outlet",
    "PaginatedReportSummaryBaseList",
    "PaginatedSubmissionList",
    "PaginatedSwitchList",
    "PatchedConfiguration",
    "PatchedConfigurationMtmType0",
    "PatchedImage",
    "PatchedLabResource",
    "PatchedPlatform",
    "PatchedWritePhysicalMachine",
    "PatchedWriteProject",
    "PhysicalMachineView",
    "Platform",
    "Port",
    "ProvisionTypeEnum",
    "PublicCertificate",
    "PublicDeviceInstance",
    "PublicRelease",
    "ReadPhysicalMachine",
    "ReadProject",
    "ReportSummaryBase",
    "ReportSummaryBaseRejectedJobs",
    "RoleEnum",
    "StatusDeaEnum",
    "Submission",
    "Switch",
    "TestResult",
    "WritePhysicalMachine",
    "WriteProject",
)
