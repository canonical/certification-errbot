from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_execution_status import TestExecutionStatus
from ..models.test_executions_patch_request_status_type_1 import (
    TestExecutionsPatchRequestStatusType1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestExecutionsPatchRequest")


@_attrs_define
class TestExecutionsPatchRequest:
    """
    Attributes:
        c3_link (Union[None, Unset, str]):
        ci_link (Union[None, Unset, str]):
        status (Union[None, TestExecutionStatus, TestExecutionsPatchRequestStatusType1, Unset]):
    """

    c3_link: Union[None, Unset, str] = UNSET
    ci_link: Union[None, Unset, str] = UNSET
    status: Union[
        None, TestExecutionStatus, TestExecutionsPatchRequestStatusType1, Unset
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        c3_link: Union[None, Unset, str]
        if isinstance(self.c3_link, Unset):
            c3_link = UNSET
        else:
            c3_link = self.c3_link

        ci_link: Union[None, Unset, str]
        if isinstance(self.ci_link, Unset):
            ci_link = UNSET
        else:
            ci_link = self.ci_link

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, TestExecutionStatus):
            status = self.status.value
        elif isinstance(self.status, TestExecutionsPatchRequestStatusType1):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if c3_link is not UNSET:
            field_dict["c3_link"] = c3_link
        if ci_link is not UNSET:
            field_dict["ci_link"] = ci_link
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_c3_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        c3_link = _parse_c3_link(d.pop("c3_link", UNSET))

        def _parse_ci_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ci_link = _parse_ci_link(d.pop("ci_link", UNSET))

        def _parse_status(
            data: object,
        ) -> Union[
            None, TestExecutionStatus, TestExecutionsPatchRequestStatusType1, Unset
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = TestExecutionStatus(data)

                return status_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = TestExecutionsPatchRequestStatusType1(data)

                return status_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TestExecutionStatus,
                    TestExecutionsPatchRequestStatusType1,
                    Unset,
                ],
                data,
            )

        status = _parse_status(d.pop("status", UNSET))

        test_executions_patch_request = cls(
            c3_link=c3_link,
            ci_link=ci_link,
            status=status,
        )

        test_executions_patch_request.additional_properties = d
        return test_executions_patch_request

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
