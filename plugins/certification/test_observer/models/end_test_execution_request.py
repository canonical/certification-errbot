from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.c3_test_result import C3TestResult


T = TypeVar("T", bound="EndTestExecutionRequest")


@_attrs_define
class EndTestExecutionRequest:
    """
    Attributes:
        ci_link (str):
        test_results (list['C3TestResult']):
        c3_link (Union[None, Unset, str]):
        checkbox_version (Union[None, Unset, str]):
    """

    ci_link: str
    test_results: list["C3TestResult"]
    c3_link: Union[None, Unset, str] = UNSET
    checkbox_version: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ci_link = self.ci_link

        test_results = []
        for test_results_item_data in self.test_results:
            test_results_item = test_results_item_data.to_dict()
            test_results.append(test_results_item)

        c3_link: Union[None, Unset, str]
        if isinstance(self.c3_link, Unset):
            c3_link = UNSET
        else:
            c3_link = self.c3_link

        checkbox_version: Union[None, Unset, str]
        if isinstance(self.checkbox_version, Unset):
            checkbox_version = UNSET
        else:
            checkbox_version = self.checkbox_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ci_link": ci_link,
                "test_results": test_results,
            }
        )
        if c3_link is not UNSET:
            field_dict["c3_link"] = c3_link
        if checkbox_version is not UNSET:
            field_dict["checkbox_version"] = checkbox_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.c3_test_result import C3TestResult

        d = src_dict.copy()
        ci_link = d.pop("ci_link")

        test_results = []
        _test_results = d.pop("test_results")
        for test_results_item_data in _test_results:
            test_results_item = C3TestResult.from_dict(test_results_item_data)

            test_results.append(test_results_item)

        def _parse_c3_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        c3_link = _parse_c3_link(d.pop("c3_link", UNSET))

        def _parse_checkbox_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        checkbox_version = _parse_checkbox_version(d.pop("checkbox_version", UNSET))

        end_test_execution_request = cls(
            ci_link=ci_link,
            test_results=test_results,
            c3_link=c3_link,
            checkbox_version=checkbox_version,
        )

        end_test_execution_request.additional_properties = d
        return end_test_execution_request

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
