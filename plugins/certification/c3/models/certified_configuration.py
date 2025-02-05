import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CertifiedConfiguration")


@_attrs_define
class CertifiedConfiguration:
    """Serializer for Certified Configuration objects

    It replicates the behaviour of the v1 API but replaces Platform names
    with Configuration names in the model field.

        Attributes:
            resource_uri (str):
            canonical_id (Union[Unset, str]):
            make (Union[Unset, str]):
            model (Union[Unset, str]):
            level (Union[Unset, str]):
            release (Union[Unset, str]):
            category (Union[Unset, str]):
            major_release (Union[Unset, str]):
            completed (Union[None, Unset, datetime.datetime]):
    """

    resource_uri: str
    canonical_id: Union[Unset, str] = UNSET
    make: Union[Unset, str] = UNSET
    model: Union[Unset, str] = UNSET
    level: Union[Unset, str] = UNSET
    release: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    major_release: Union[Unset, str] = UNSET
    completed: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uri = self.resource_uri

        canonical_id = self.canonical_id

        make = self.make

        model = self.model

        level = self.level

        release = self.release

        category = self.category

        major_release = self.major_release

        completed: Union[None, Unset, str]
        if isinstance(self.completed, Unset):
            completed = UNSET
        elif isinstance(self.completed, datetime.datetime):
            completed = self.completed.isoformat()
        else:
            completed = self.completed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uri": resource_uri,
            }
        )
        if canonical_id is not UNSET:
            field_dict["canonical_id"] = canonical_id
        if make is not UNSET:
            field_dict["make"] = make
        if model is not UNSET:
            field_dict["model"] = model
        if level is not UNSET:
            field_dict["level"] = level
        if release is not UNSET:
            field_dict["release"] = release
        if category is not UNSET:
            field_dict["category"] = category
        if major_release is not UNSET:
            field_dict["major_release"] = major_release
        if completed is not UNSET:
            field_dict["completed"] = completed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_uri = d.pop("resource_uri")

        canonical_id = d.pop("canonical_id", UNSET)

        make = d.pop("make", UNSET)

        model = d.pop("model", UNSET)

        level = d.pop("level", UNSET)

        release = d.pop("release", UNSET)

        category = d.pop("category", UNSET)

        major_release = d.pop("major_release", UNSET)

        def _parse_completed(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_type_0 = isoparse(data)

                return completed_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed = _parse_completed(d.pop("completed", UNSET))

        certified_configuration = cls(
            resource_uri=resource_uri,
            canonical_id=canonical_id,
            make=make,
            model=model,
            level=level,
            release=release,
            category=category,
            major_release=major_release,
            completed=completed,
        )

        certified_configuration.additional_properties = d
        return certified_configuration

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
