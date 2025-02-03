from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_execution_status import TestExecutionStatus

if TYPE_CHECKING:
    from ..models.environment_dto import EnvironmentDTO


T = TypeVar("T", bound="TestExecutionDTO")


@_attrs_define
class TestExecutionDTO:
    """
    Attributes:
        id (int):
        ci_link (Union[None, str]):
        c3_link (Union[None, str]):
        environment (EnvironmentDTO):
        status (TestExecutionStatus):
        test_plan (str):
        is_rerun_requested (bool):
    """

    id: int
    ci_link: Union[None, str]
    c3_link: Union[None, str]
    environment: "EnvironmentDTO"
    status: TestExecutionStatus
    test_plan: str
    is_rerun_requested: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ci_link: Union[None, str]
        ci_link = self.ci_link

        c3_link: Union[None, str]
        c3_link = self.c3_link

        environment = self.environment.to_dict()

        status = self.status.value

        test_plan = self.test_plan

        is_rerun_requested = self.is_rerun_requested

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ci_link": ci_link,
                "c3_link": c3_link,
                "environment": environment,
                "status": status,
                "test_plan": test_plan,
                "is_rerun_requested": is_rerun_requested,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.environment_dto import EnvironmentDTO

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_ci_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ci_link = _parse_ci_link(d.pop("ci_link"))

        def _parse_c3_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        c3_link = _parse_c3_link(d.pop("c3_link"))

        environment = EnvironmentDTO.from_dict(d.pop("environment"))

        status = TestExecutionStatus(d.pop("status"))

        test_plan = d.pop("test_plan")

        is_rerun_requested = d.pop("is_rerun_requested")

        test_execution_dto = cls(
            id=id,
            ci_link=ci_link,
            c3_link=c3_link,
            environment=environment,
            status=status,
            test_plan=test_plan,
            is_rerun_requested=is_rerun_requested,
        )

        test_execution_dto.additional_properties = d
        return test_execution_dto

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
