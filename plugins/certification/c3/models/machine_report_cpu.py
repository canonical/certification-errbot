from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.machine_report_cpu_additional_property import (
        MachineReportCpuAdditionalProperty,
    )


T = TypeVar("T", bound="MachineReportCpu")


@_attrs_define
class MachineReportCpu:
    """Get fields from checkbox_report related to CPU"""

    additional_properties: dict[str, "MachineReportCpuAdditionalProperty"] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.machine_report_cpu_additional_property import (
            MachineReportCpuAdditionalProperty,
        )

        d = src_dict.copy()
        machine_report_cpu = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = MachineReportCpuAdditionalProperty.from_dict(
                prop_dict
            )

            additional_properties[prop_name] = additional_property

        machine_report_cpu.additional_properties = additional_properties
        return machine_report_cpu

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "MachineReportCpuAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: "MachineReportCpuAdditionalProperty"
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
