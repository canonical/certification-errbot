import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestReportedIssueResponse")


@_attrs_define
class TestReportedIssueResponse:
    """
    Attributes:
        id (int):
        description (str):
        url (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        template_id (Union[Unset, str]):  Default: ''.
        case_name (Union[Unset, str]):  Default: ''.
    """

    id: int
    description: str
    url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    template_id: Union[Unset, str] = ""
    case_name: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        description = self.description

        url = self.url

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        template_id = self.template_id

        case_name = self.case_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "description": description,
                "url": url,
                "created_at": created_at,
                "updated_at": updated_at,
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
        id = d.pop("id")

        description = d.pop("description")

        url = d.pop("url")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        template_id = d.pop("template_id", UNSET)

        case_name = d.pop("case_name", UNSET)

        test_reported_issue_response = cls(
            id=id,
            description=description,
            url=url,
            created_at=created_at,
            updated_at=updated_at,
            template_id=template_id,
            case_name=case_name,
        )

        test_reported_issue_response.additional_properties = d
        return test_reported_issue_response

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
