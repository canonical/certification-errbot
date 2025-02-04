from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.start_image_test_execution_request_execution_stage import (
    StartImageTestExecutionRequestExecutionStage,
)
from ..models.start_image_test_execution_request_family import (
    StartImageTestExecutionRequestFamily,
)
from ..models.test_execution_status import TestExecutionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="StartImageTestExecutionRequest")


@_attrs_define
class StartImageTestExecutionRequest:
    """
    Attributes:
        name (str):
        version (str):
        arch (str):
        environment (str):
        test_plan (str):
        execution_stage (StartImageTestExecutionRequestExecutionStage):
        os (str):
        release (str):
        sha256 (str):
        owner (str):
        image_url (str):
        ci_link (Union[None, Unset, str]):
        initial_status (Union[Unset, TestExecutionStatus]):  Default: TestExecutionStatus.IN_PROGRESS.
        family (Union[Unset, StartImageTestExecutionRequestFamily]):  Default:
            StartImageTestExecutionRequestFamily.IMAGE.
    """

    name: str
    version: str
    arch: str
    environment: str
    test_plan: str
    execution_stage: StartImageTestExecutionRequestExecutionStage
    os: str
    release: str
    sha256: str
    owner: str
    image_url: str
    ci_link: Union[None, Unset, str] = UNSET
    initial_status: Union[Unset, TestExecutionStatus] = TestExecutionStatus.IN_PROGRESS
    family: Union[Unset, StartImageTestExecutionRequestFamily] = (
        StartImageTestExecutionRequestFamily.IMAGE
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        arch = self.arch

        environment = self.environment

        test_plan = self.test_plan

        execution_stage = self.execution_stage.value

        os = self.os

        release = self.release

        sha256 = self.sha256

        owner = self.owner

        image_url = self.image_url

        ci_link: Union[None, Unset, str]
        if isinstance(self.ci_link, Unset):
            ci_link = UNSET
        else:
            ci_link = self.ci_link

        initial_status: Union[Unset, str] = UNSET
        if not isinstance(self.initial_status, Unset):
            initial_status = self.initial_status.value

        family: Union[Unset, str] = UNSET
        if not isinstance(self.family, Unset):
            family = self.family.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "arch": arch,
                "environment": environment,
                "test_plan": test_plan,
                "execution_stage": execution_stage,
                "os": os,
                "release": release,
                "sha256": sha256,
                "owner": owner,
                "image_url": image_url,
            }
        )
        if ci_link is not UNSET:
            field_dict["ci_link"] = ci_link
        if initial_status is not UNSET:
            field_dict["initial_status"] = initial_status
        if family is not UNSET:
            field_dict["family"] = family

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        version = d.pop("version")

        arch = d.pop("arch")

        environment = d.pop("environment")

        test_plan = d.pop("test_plan")

        execution_stage = StartImageTestExecutionRequestExecutionStage(
            d.pop("execution_stage")
        )

        os = d.pop("os")

        release = d.pop("release")

        sha256 = d.pop("sha256")

        owner = d.pop("owner")

        image_url = d.pop("image_url")

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

        _family = d.pop("family", UNSET)
        family: Union[Unset, StartImageTestExecutionRequestFamily]
        if isinstance(_family, Unset):
            family = UNSET
        else:
            family = StartImageTestExecutionRequestFamily(_family)

        start_image_test_execution_request = cls(
            name=name,
            version=version,
            arch=arch,
            environment=environment,
            test_plan=test_plan,
            execution_stage=execution_stage,
            os=os,
            release=release,
            sha256=sha256,
            owner=owner,
            image_url=image_url,
            ci_link=ci_link,
            initial_status=initial_status,
            family=family,
        )

        start_image_test_execution_request.additional_properties = d
        return start_image_test_execution_request

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
