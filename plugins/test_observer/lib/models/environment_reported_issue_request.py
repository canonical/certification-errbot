from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnvironmentReportedIssueRequest")


@_attrs_define
class EnvironmentReportedIssueRequest:
    """
    Attributes:
        environment_name (str):
        description (str):
        is_confirmed (bool):
        url (Union[None, Unset, str]):
    """

    environment_name: str
    description: str
    is_confirmed: bool
    url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        environment_name = self.environment_name

        description = self.description

        is_confirmed = self.is_confirmed

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "environment_name": environment_name,
                "description": description,
                "is_confirmed": is_confirmed,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        environment_name = d.pop("environment_name")

        description = d.pop("description")

        is_confirmed = d.pop("is_confirmed")

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        environment_reported_issue_request = cls(
            environment_name=environment_name,
            description=description,
            is_confirmed=is_confirmed,
            url=url,
        )

        environment_reported_issue_request.additional_properties = d
        return environment_reported_issue_request

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
