from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.c3_test_result_status import C3TestResultStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="C3TestResult")


@_attrs_define
class C3TestResult:
    """
    Attributes:
        name (str):
        status (C3TestResultStatus):
        category (str):
        comment (str):
        io_log (str):
        template_id (Union[None, Unset, str]):
    """

    name: str
    status: C3TestResultStatus
    category: str
    comment: str
    io_log: str
    template_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        category = self.category

        comment = self.comment

        io_log = self.io_log

        template_id: Union[None, Unset, str]
        if isinstance(self.template_id, Unset):
            template_id = UNSET
        else:
            template_id = self.template_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
                "category": category,
                "comment": comment,
                "io_log": io_log,
            }
        )
        if template_id is not UNSET:
            field_dict["template_id"] = template_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        status = C3TestResultStatus(d.pop("status"))

        category = d.pop("category")

        comment = d.pop("comment")

        io_log = d.pop("io_log")

        def _parse_template_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template_id = _parse_template_id(d.pop("template_id", UNSET))

        c3_test_result = cls(
            name=name,
            status=status,
            category=category,
            comment=comment,
            io_log=io_log,
            template_id=template_id,
        )

        c3_test_result.additional_properties = d
        return c3_test_result

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
