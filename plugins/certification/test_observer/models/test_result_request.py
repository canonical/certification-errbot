from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_result_status import TestResultStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestResultRequest")


@_attrs_define
class TestResultRequest:
    """
    Attributes:
        name (str):
        status (TestResultStatus):
        template_id (Union[Unset, str]):  Default: ''.
        category (Union[Unset, str]):  Default: ''.
        comment (Union[Unset, str]):  Default: ''.
        io_log (Union[Unset, str]):  Default: ''.
    """

    name: str
    status: TestResultStatus
    template_id: Union[Unset, str] = ""
    category: Union[Unset, str] = ""
    comment: Union[Unset, str] = ""
    io_log: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        template_id = self.template_id

        category = self.category

        comment = self.comment

        io_log = self.io_log

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
            }
        )
        if template_id is not UNSET:
            field_dict["template_id"] = template_id
        if category is not UNSET:
            field_dict["category"] = category
        if comment is not UNSET:
            field_dict["comment"] = comment
        if io_log is not UNSET:
            field_dict["io_log"] = io_log

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        status = TestResultStatus(d.pop("status"))

        template_id = d.pop("template_id", UNSET)

        category = d.pop("category", UNSET)

        comment = d.pop("comment", UNSET)

        io_log = d.pop("io_log", UNSET)

        test_result_request = cls(
            name=name,
            status=status,
            template_id=template_id,
            category=category,
            comment=comment,
            io_log=io_log,
        )

        test_result_request.additional_properties = d
        return test_result_request

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
