from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.start_snap_test_execution_request_execution_stage import StartSnapTestExecutionRequestExecutionStage
from ..models.start_snap_test_execution_request_family import StartSnapTestExecutionRequestFamily
from ..models.test_execution_status import TestExecutionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="StartSnapTestExecutionRequest")


@_attrs_define
class StartSnapTestExecutionRequest:
    """
    Attributes:
        name (str):
        version (str):
        arch (str):
        environment (str):
        test_plan (str):
        family (StartSnapTestExecutionRequestFamily):
        revision (int):
        track (str):
        store (str):
        execution_stage (StartSnapTestExecutionRequestExecutionStage):
        ci_link (Union[None, Unset, str]):
        initial_status (Union[Unset, TestExecutionStatus]):  Default: TestExecutionStatus.IN_PROGRESS.
    """

    name: str
    version: str
    arch: str
    environment: str
    test_plan: str
    family: StartSnapTestExecutionRequestFamily
    revision: int
    track: str
    store: str
    execution_stage: StartSnapTestExecutionRequestExecutionStage
    ci_link: Union[None, Unset, str] = UNSET
    initial_status: Union[Unset, TestExecutionStatus] = TestExecutionStatus.IN_PROGRESS
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        arch = self.arch

        environment = self.environment

        test_plan = self.test_plan

        family = self.family.value

        revision = self.revision

        track = self.track

        store = self.store

        execution_stage = self.execution_stage.value

        ci_link: Union[None, Unset, str]
        if isinstance(self.ci_link, Unset):
            ci_link = UNSET
        else:
            ci_link = self.ci_link

        initial_status: Union[Unset, str] = UNSET
        if not isinstance(self.initial_status, Unset):
            initial_status = self.initial_status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "arch": arch,
                "environment": environment,
                "test_plan": test_plan,
                "family": family,
                "revision": revision,
                "track": track,
                "store": store,
                "execution_stage": execution_stage,
            }
        )
        if ci_link is not UNSET:
            field_dict["ci_link"] = ci_link
        if initial_status is not UNSET:
            field_dict["initial_status"] = initial_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        version = d.pop("version")

        arch = d.pop("arch")

        environment = d.pop("environment")

        test_plan = d.pop("test_plan")

        family = StartSnapTestExecutionRequestFamily(d.pop("family"))

        revision = d.pop("revision")

        track = d.pop("track")

        store = d.pop("store")

        execution_stage = StartSnapTestExecutionRequestExecutionStage(d.pop("execution_stage"))

        def _parse_ci_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ci_link = _parse_ci_link(d.pop("ci_link", UNSET))

        _initial_status = d.pop("initial_status", UNSET)
        initial_status: Union[Unset, TestExecutionStatus]
        if isinstance(_initial_status, Unset):
            initial_status = UNSET
        else:
            initial_status = TestExecutionStatus(_initial_status)

        start_snap_test_execution_request = cls(
            name=name,
            version=version,
            arch=arch,
            environment=environment,
            test_plan=test_plan,
            family=family,
            revision=revision,
            track=track,
            store=store,
            execution_stage=execution_stage,
            ci_link=ci_link,
            initial_status=initial_status,
        )

        start_snap_test_execution_request.additional_properties = d
        return start_snap_test_execution_request

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
