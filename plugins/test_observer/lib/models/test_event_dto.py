import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="TestEventDTO")


@_attrs_define
class TestEventDTO:
    """
    Attributes:
        event_name (str):
        timestamp (datetime.datetime):
        detail (str):
    """

    event_name: str
    timestamp: datetime.datetime
    detail: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_name = self.event_name

        timestamp = self.timestamp.isoformat()

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_name": event_name,
                "timestamp": timestamp,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        event_name = d.pop("event_name")

        timestamp = isoparse(d.pop("timestamp"))

        detail = d.pop("detail")

        test_event_dto = cls(
            event_name=event_name,
            timestamp=timestamp,
            detail=detail,
        )

        test_event_dto.additional_properties = d
        return test_event_dto

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
