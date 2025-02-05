import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublicRelease")


@_attrs_define
class PublicRelease:
    """Public serialiser for the release model

    Attributes:
        codename (str):
        release (str):
        release_date (Union[None, Unset, datetime.date]):
        supported_until (Union[None, Unset, datetime.date]):
        i_version (Union[None, Unset, int]):
    """

    codename: str
    release: str
    release_date: Union[None, Unset, datetime.date] = UNSET
    supported_until: Union[None, Unset, datetime.date] = UNSET
    i_version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        codename = self.codename

        release = self.release

        release_date: Union[None, Unset, str]
        if isinstance(self.release_date, Unset):
            release_date = UNSET
        elif isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        supported_until: Union[None, Unset, str]
        if isinstance(self.supported_until, Unset):
            supported_until = UNSET
        elif isinstance(self.supported_until, datetime.date):
            supported_until = self.supported_until.isoformat()
        else:
            supported_until = self.supported_until

        i_version: Union[None, Unset, int]
        if isinstance(self.i_version, Unset):
            i_version = UNSET
        else:
            i_version = self.i_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "codename": codename,
                "release": release,
            }
        )
        if release_date is not UNSET:
            field_dict["release_date"] = release_date
        if supported_until is not UNSET:
            field_dict["supported_until"] = supported_until
        if i_version is not UNSET:
            field_dict["i_version"] = i_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        codename = d.pop("codename")

        release = d.pop("release")

        def _parse_release_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_date_type_0 = isoparse(data).date()

                return release_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        release_date = _parse_release_date(d.pop("release_date", UNSET))

        def _parse_supported_until(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                supported_until_type_0 = isoparse(data).date()

                return supported_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        supported_until = _parse_supported_until(d.pop("supported_until", UNSET))

        def _parse_i_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        i_version = _parse_i_version(d.pop("i_version", UNSET))

        public_release = cls(
            codename=codename,
            release=release,
            release_date=release_date,
            supported_until=supported_until,
            i_version=i_version,
        )

        public_release.additional_properties = d
        return public_release

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
