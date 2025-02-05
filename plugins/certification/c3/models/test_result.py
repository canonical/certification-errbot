from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestResult")


@_attrs_define
class TestResult:
    """Serializer for the TestResult objects

    Attributes:
        name (Union[None, str]):
        id (int):
        status (str):
        comment (Union[None, str]):
        io_log (Union[None, str]):
        category (Union[None, str]):
        template_id (Union[None, str]):
    """

    name: Union[None, str]
    id: int
    status: str
    comment: Union[None, str]
    io_log: Union[None, str]
    category: Union[None, str]
    template_id: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, str]
        name = self.name

        id = self.id

        status = self.status

        comment: Union[None, str]
        comment = self.comment

        io_log: Union[None, str]
        io_log = self.io_log

        category: Union[None, str]
        category = self.category

        template_id: Union[None, str]
        template_id = self.template_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "status": status,
                "comment": comment,
                "io_log": io_log,
                "category": category,
                "template_id": template_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        id = d.pop("id")

        status = d.pop("status")

        def _parse_comment(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        comment = _parse_comment(d.pop("comment"))

        def _parse_io_log(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        io_log = _parse_io_log(d.pop("io_log"))

        def _parse_category(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category = _parse_category(d.pop("category"))

        def _parse_template_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        template_id = _parse_template_id(d.pop("template_id"))

        test_result = cls(
            name=name,
            id=id,
            status=status,
            comment=comment,
            io_log=io_log,
            category=category,
            template_id=template_id,
        )

        test_result.additional_properties = d
        return test_result

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
