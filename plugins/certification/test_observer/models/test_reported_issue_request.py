from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestReportedIssueRequest")


@_attrs_define
class TestReportedIssueRequest:
    """
    Attributes:
        description (str):
        url (str):
        template_id (Union[Unset, str]):  Default: ''.
        case_name (Union[Unset, str]):  Default: ''.
    """

    description: str
    url: str
    template_id: Union[Unset, str] = ""
    case_name: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        url = self.url

        template_id = self.template_id

        case_name = self.case_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "url": url,
            }
        )
        if template_id is not UNSET:
            field_dict["template_id"] = template_id
        if case_name is not UNSET:
            field_dict["case_name"] = case_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        url = d.pop("url")

        template_id = d.pop("template_id", UNSET)

        case_name = d.pop("case_name", UNSET)

        test_reported_issue_request = cls(
            description=description,
            url=url,
            template_id=template_id,
            case_name=case_name,
        )

        test_reported_issue_request.additional_properties = d
        return test_reported_issue_request

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
