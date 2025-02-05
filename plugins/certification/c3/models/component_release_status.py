import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.component_release_status_status_enum import (
    ComponentReleaseStatusStatusEnum,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.public_release import PublicRelease


T = TypeVar("T", bound="ComponentReleaseStatus")


@_attrs_define
class ComponentReleaseStatus:
    """Serializer for the ComponentReleaseStatus objects

    Attributes:
        created (datetime.datetime):
        updated (datetime.datetime):
        certified_release (PublicRelease): Public serialiser for the release model
        status (Union[Unset, ComponentReleaseStatusStatusEnum]): * `certified` - Certified
            * `inprogress` - In Progress
            * `unsupported` - Unsupported
        third_party_driver (Union[Unset, bool]): A third party driver is needed to support this release
    """

    created: datetime.datetime
    updated: datetime.datetime
    certified_release: "PublicRelease"
    status: Union[Unset, ComponentReleaseStatusStatusEnum] = UNSET
    third_party_driver: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created.isoformat()

        updated = self.updated.isoformat()

        certified_release = self.certified_release.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        third_party_driver = self.third_party_driver

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "updated": updated,
                "certified_release": certified_release,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if third_party_driver is not UNSET:
            field_dict["third_party_driver"] = third_party_driver

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.public_release import PublicRelease

        d = src_dict.copy()
        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        certified_release = PublicRelease.from_dict(d.pop("certified_release"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ComponentReleaseStatusStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ComponentReleaseStatusStatusEnum(_status)

        third_party_driver = d.pop("third_party_driver", UNSET)

        component_release_status = cls(
            created=created,
            updated=updated,
            certified_release=certified_release,
            status=status,
            third_party_driver=third_party_driver,
        )

        component_release_status.additional_properties = d
        return component_release_status

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
