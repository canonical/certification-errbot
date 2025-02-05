import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.report_summary_base_rejected_jobs import ReportSummaryBaseRejectedJobs
    from ..models.test_result import TestResult


T = TypeVar("T", bound="ReportSummaryBase")


@_attrs_define
class ReportSummaryBase:
    """Serializer for generating ReportSummary from the MachineReport model

    The implementation has a similar logic to the MachineReportSerializer,
    however, it contains more fields from the report to fully replicate
    the v1 version of the API endpoint.

        Attributes:
            id (int):
            arch_name (Union[None, str]):
            canonical_id (Union[None, str]):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            signed_off_at (Union[None, datetime.datetime]):
            container_name (Union[None, str]):
            created_by (int):
            custom_joblist (Union[None, bool]): True if the user ran a modified set of jobs in the testplan
            description (Union[None, str]): A description of the purpose of the submission, e.g. 'Stress testing', 'Core
                snap update test', etc.
            duration (float): Total duration of the test run
            failed_test_count (int):
            firmware_revision (Union[None, str]):
            is_specification (bool):
            kernel_cmdline (Union[None, str]):
            kernel_version (Union[None, str]):
            memory_swap (Union[None, str]):
            memory_total (Union[None, str]):
            passed_test_count (int):
            pci_subsystem (Union[None, str]):
            physical_machine (str):
            platform_name (Union[None, str]):
            product_name (Union[None, str]):
            product_version (Union[None, str]):
            rejected_jobs (ReportSummaryBaseRejectedJobs): A json list with information about tests that were deselected
                from the testplan
            release_version (Union[None, str]):
            resource_uri (str):
            shared_hexr (Union[None, bool]):
            signed_off (bool):
            skipped_test_count (int):
            source (str):
            submission_data_url (str):
            submission_id (Union[None, str]): id of submission service request this report is based on
            test_count (int):
            testplan_id (str): Name of the checkbox testplan
            updated_by (int):
            testresult_set (list['TestResult']):
    """

    id: int
    arch_name: Union[None, str]
    canonical_id: Union[None, str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    signed_off_at: Union[None, datetime.datetime]
    container_name: Union[None, str]
    created_by: int
    custom_joblist: Union[None, bool]
    description: Union[None, str]
    duration: float
    failed_test_count: int
    firmware_revision: Union[None, str]
    is_specification: bool
    kernel_cmdline: Union[None, str]
    kernel_version: Union[None, str]
    memory_swap: Union[None, str]
    memory_total: Union[None, str]
    passed_test_count: int
    pci_subsystem: Union[None, str]
    physical_machine: str
    platform_name: Union[None, str]
    product_name: Union[None, str]
    product_version: Union[None, str]
    rejected_jobs: "ReportSummaryBaseRejectedJobs"
    release_version: Union[None, str]
    resource_uri: str
    shared_hexr: Union[None, bool]
    signed_off: bool
    skipped_test_count: int
    source: str
    submission_data_url: str
    submission_id: Union[None, str]
    test_count: int
    testplan_id: str
    updated_by: int
    testresult_set: list["TestResult"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        arch_name: Union[None, str]
        arch_name = self.arch_name

        canonical_id: Union[None, str]
        canonical_id = self.canonical_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        signed_off_at: Union[None, str]
        if isinstance(self.signed_off_at, datetime.datetime):
            signed_off_at = self.signed_off_at.isoformat()
        else:
            signed_off_at = self.signed_off_at

        container_name: Union[None, str]
        container_name = self.container_name

        created_by = self.created_by

        custom_joblist: Union[None, bool]
        custom_joblist = self.custom_joblist

        description: Union[None, str]
        description = self.description

        duration = self.duration

        failed_test_count = self.failed_test_count

        firmware_revision: Union[None, str]
        firmware_revision = self.firmware_revision

        is_specification = self.is_specification

        kernel_cmdline: Union[None, str]
        kernel_cmdline = self.kernel_cmdline

        kernel_version: Union[None, str]
        kernel_version = self.kernel_version

        memory_swap: Union[None, str]
        memory_swap = self.memory_swap

        memory_total: Union[None, str]
        memory_total = self.memory_total

        passed_test_count = self.passed_test_count

        pci_subsystem: Union[None, str]
        pci_subsystem = self.pci_subsystem

        physical_machine = self.physical_machine

        platform_name: Union[None, str]
        platform_name = self.platform_name

        product_name: Union[None, str]
        product_name = self.product_name

        product_version: Union[None, str]
        product_version = self.product_version

        rejected_jobs = self.rejected_jobs.to_dict()

        release_version: Union[None, str]
        release_version = self.release_version

        resource_uri = self.resource_uri

        shared_hexr: Union[None, bool]
        shared_hexr = self.shared_hexr

        signed_off = self.signed_off

        skipped_test_count = self.skipped_test_count

        source = self.source

        submission_data_url = self.submission_data_url

        submission_id: Union[None, str]
        submission_id = self.submission_id

        test_count = self.test_count

        testplan_id = self.testplan_id

        updated_by = self.updated_by

        testresult_set = []
        for testresult_set_item_data in self.testresult_set:
            testresult_set_item = testresult_set_item_data.to_dict()
            testresult_set.append(testresult_set_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "arch_name": arch_name,
                "canonical_id": canonical_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "signed_off_at": signed_off_at,
                "container_name": container_name,
                "created_by": created_by,
                "custom_joblist": custom_joblist,
                "description": description,
                "duration": duration,
                "failed_test_count": failed_test_count,
                "firmware_revision": firmware_revision,
                "is_specification": is_specification,
                "kernel_cmdline": kernel_cmdline,
                "kernel_version": kernel_version,
                "memory_swap": memory_swap,
                "memory_total": memory_total,
                "passed_test_count": passed_test_count,
                "pci_subsystem": pci_subsystem,
                "physical_machine": physical_machine,
                "platform_name": platform_name,
                "product_name": product_name,
                "product_version": product_version,
                "rejected_jobs": rejected_jobs,
                "release_version": release_version,
                "resource_uri": resource_uri,
                "shared_hexr": shared_hexr,
                "signed_off": signed_off,
                "skipped_test_count": skipped_test_count,
                "source": source,
                "submission_data_url": submission_data_url,
                "submission_id": submission_id,
                "test_count": test_count,
                "testplan_id": testplan_id,
                "updated_by": updated_by,
                "testresult_set": testresult_set,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.report_summary_base_rejected_jobs import (
            ReportSummaryBaseRejectedJobs,
        )
        from ..models.test_result import TestResult

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_arch_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        arch_name = _parse_arch_name(d.pop("arch_name"))

        def _parse_canonical_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_signed_off_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                signed_off_at_type_0 = isoparse(data)

                return signed_off_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        signed_off_at = _parse_signed_off_at(d.pop("signed_off_at"))

        def _parse_container_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        container_name = _parse_container_name(d.pop("container_name"))

        created_by = d.pop("created_by")

        def _parse_custom_joblist(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        custom_joblist = _parse_custom_joblist(d.pop("custom_joblist"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        duration = d.pop("duration")

        failed_test_count = d.pop("failed_test_count")

        def _parse_firmware_revision(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        firmware_revision = _parse_firmware_revision(d.pop("firmware_revision"))

        is_specification = d.pop("is_specification")

        def _parse_kernel_cmdline(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        kernel_cmdline = _parse_kernel_cmdline(d.pop("kernel_cmdline"))

        def _parse_kernel_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        kernel_version = _parse_kernel_version(d.pop("kernel_version"))

        def _parse_memory_swap(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        memory_swap = _parse_memory_swap(d.pop("memory_swap"))

        def _parse_memory_total(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        memory_total = _parse_memory_total(d.pop("memory_total"))

        passed_test_count = d.pop("passed_test_count")

        def _parse_pci_subsystem(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pci_subsystem = _parse_pci_subsystem(d.pop("pci_subsystem"))

        physical_machine = d.pop("physical_machine")

        def _parse_platform_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        platform_name = _parse_platform_name(d.pop("platform_name"))

        def _parse_product_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        product_name = _parse_product_name(d.pop("product_name"))

        def _parse_product_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        product_version = _parse_product_version(d.pop("product_version"))

        rejected_jobs = ReportSummaryBaseRejectedJobs.from_dict(d.pop("rejected_jobs"))

        def _parse_release_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        release_version = _parse_release_version(d.pop("release_version"))

        resource_uri = d.pop("resource_uri")

        def _parse_shared_hexr(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        shared_hexr = _parse_shared_hexr(d.pop("shared_hexr"))

        signed_off = d.pop("signed_off")

        skipped_test_count = d.pop("skipped_test_count")

        source = d.pop("source")

        submission_data_url = d.pop("submission_data_url")

        def _parse_submission_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        submission_id = _parse_submission_id(d.pop("submission_id"))

        test_count = d.pop("test_count")

        testplan_id = d.pop("testplan_id")

        updated_by = d.pop("updated_by")

        testresult_set = []
        _testresult_set = d.pop("testresult_set")
        for testresult_set_item_data in _testresult_set:
            testresult_set_item = TestResult.from_dict(testresult_set_item_data)

            testresult_set.append(testresult_set_item)

        report_summary_base = cls(
            id=id,
            arch_name=arch_name,
            canonical_id=canonical_id,
            created_at=created_at,
            updated_at=updated_at,
            signed_off_at=signed_off_at,
            container_name=container_name,
            created_by=created_by,
            custom_joblist=custom_joblist,
            description=description,
            duration=duration,
            failed_test_count=failed_test_count,
            firmware_revision=firmware_revision,
            is_specification=is_specification,
            kernel_cmdline=kernel_cmdline,
            kernel_version=kernel_version,
            memory_swap=memory_swap,
            memory_total=memory_total,
            passed_test_count=passed_test_count,
            pci_subsystem=pci_subsystem,
            physical_machine=physical_machine,
            platform_name=platform_name,
            product_name=product_name,
            product_version=product_version,
            rejected_jobs=rejected_jobs,
            release_version=release_version,
            resource_uri=resource_uri,
            shared_hexr=shared_hexr,
            signed_off=signed_off,
            skipped_test_count=skipped_test_count,
            source=source,
            submission_data_url=submission_data_url,
            submission_id=submission_id,
            test_count=test_count,
            testplan_id=testplan_id,
            updated_by=updated_by,
            testresult_set=testresult_set,
        )

        report_summary_base.additional_properties = d
        return report_summary_base

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
