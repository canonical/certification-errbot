from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.machine_report_cpu import MachineReportCpu
    from ..models.machine_report_devices import MachineReportDevices
    from ..models.machine_report_memory import MachineReportMemory


T = TypeVar("T", bound="MachineReport")


@_attrs_define
class MachineReport:
    """Serializer for MachineReport objects

    Contains canonicalID and the following fields from the checkbox_report:
      - memory (swap and total)
      - cpu make

        Attributes:
            canonical_id (Union[None, str]):
            submission (int):
            memory (MachineReportMemory): Get memory field from checkbox_report
            cpu (MachineReportCpu): Get fields from checkbox_report related to CPU
            kernel_version (str): Get kernel fields from checkbox_report
            devices (MachineReportDevices): Get info about the following devices:
                  - wired and wireless network cards
                  - gpu
                  - audio adapters
                  - motherboard
    """

    canonical_id: Union[None, str]
    submission: int
    memory: "MachineReportMemory"
    cpu: "MachineReportCpu"
    kernel_version: str
    devices: "MachineReportDevices"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        canonical_id: Union[None, str]
        canonical_id = self.canonical_id

        submission = self.submission

        memory = self.memory.to_dict()

        cpu = self.cpu.to_dict()

        kernel_version = self.kernel_version

        devices = self.devices.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canonical_id": canonical_id,
                "submission": submission,
                "memory": memory,
                "cpu": cpu,
                "kernel_version": kernel_version,
                "devices": devices,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.machine_report_cpu import MachineReportCpu
        from ..models.machine_report_devices import MachineReportDevices
        from ..models.machine_report_memory import MachineReportMemory

        d = src_dict.copy()

        def _parse_canonical_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        canonical_id = _parse_canonical_id(d.pop("canonical_id"))

        submission = d.pop("submission")

        memory = MachineReportMemory.from_dict(d.pop("memory"))

        cpu = MachineReportCpu.from_dict(d.pop("cpu"))

        kernel_version = d.pop("kernel_version")

        devices = MachineReportDevices.from_dict(d.pop("devices"))

        machine_report = cls(
            canonical_id=canonical_id,
            submission=submission,
            memory=memory,
            cpu=cpu,
            kernel_version=kernel_version,
            devices=devices,
        )

        machine_report.additional_properties = d
        return machine_report

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
