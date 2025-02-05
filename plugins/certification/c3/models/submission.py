import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Submission")


@_attrs_define
class Submission:
    """Serializer for submissions (not machine reports) that are made by submitting
    checkbox reports as .tar.xz files

        Attributes:
            id (int):
            report_id (Union[None, int]):
            status (Union[None, str]):
            failure_reason (Union[None, str]):
            created_at (datetime.datetime):
            processed (Union[None, datetime.datetime]):
    """

    id: int
    report_id: Union[None, int]
    status: Union[None, str]
    failure_reason: Union[None, str]
    created_at: datetime.datetime
    processed: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        report_id: Union[None, int]
        report_id = self.report_id

        status: Union[None, str]
        status = self.status

        failure_reason: Union[None, str]
        failure_reason = self.failure_reason

        created_at = self.created_at.isoformat()

        processed: Union[None, str]
        if isinstance(self.processed, datetime.datetime):
            processed = self.processed.isoformat()
        else:
            processed = self.processed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "report_id": report_id,
                "status": status,
                "failure_reason": failure_reason,
                "created_at": created_at,
                "processed": processed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_report_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        report_id = _parse_report_id(d.pop("report_id"))

        def _parse_status(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        status = _parse_status(d.pop("status"))

        def _parse_failure_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        failure_reason = _parse_failure_reason(d.pop("failure_reason"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_processed(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                processed_type_0 = isoparse(data)

                return processed_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        processed = _parse_processed(d.pop("processed"))

        submission = cls(
            id=id,
            report_id=report_id,
            status=status,
            failure_reason=failure_reason,
            created_at=created_at,
            processed=processed,
        )

        submission.additional_properties = d
        return submission

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
