from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_status import TestResultStatus

T = TypeVar("T", bound="PreviousTestResult")


@_attrs_define
class PreviousTestResult:
    """
    Attributes:
        status (TestResultStatus):
        version (str):
        artefact_id (int):
    """

    status: TestResultStatus
    version: str
    artefact_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        version = self.version

        artefact_id = self.artefact_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "version": version,
                "artefact_id": artefact_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        status = TestResultStatus(d.pop("status"))

        version = d.pop("version")

        artefact_id = d.pop("artefact_id")

        previous_test_result = cls(
            status=status,
            version=version,
            artefact_id=artefact_id,
        )

        previous_test_result.additional_properties = d
        return previous_test_result

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
