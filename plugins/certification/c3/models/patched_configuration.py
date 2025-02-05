import datetime
import json
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_configuration_mtm_type_0 import PatchedConfigurationMtmType0


T = TypeVar("T", bound="PatchedConfiguration")


@_attrs_define
class PatchedConfiguration:
    """Serializer for Configuration objects

    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]): Model name for a group of machines. Should be unique within a platform
        description (Union[Unset, str]):
        canonical_label (Union[Unset, str]):
        sku (Union[Unset, str]): OEM specific configuration name
        additional_names (Union[Unset, list[str]]):
        mtm (Union['PatchedConfigurationMtmType0', None, Unset]): Vendor specific JSONB metadata
        release_to_ship (Union[None, Unset, datetime.date]): Date when the hardware information can be released
        platform (Union[Unset, int]): Platform as parent object associated with the configuration
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    canonical_label: Union[Unset, str] = UNSET
    sku: Union[Unset, str] = UNSET
    additional_names: Union[Unset, list[str]] = UNSET
    mtm: Union["PatchedConfigurationMtmType0", None, Unset] = UNSET
    release_to_ship: Union[None, Unset, datetime.date] = UNSET
    platform: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.patched_configuration_mtm_type_0 import (
            PatchedConfigurationMtmType0,
        )

        id = self.id

        name = self.name

        description = self.description

        canonical_label = self.canonical_label

        sku = self.sku

        additional_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.additional_names, Unset):
            additional_names = self.additional_names

        mtm: Union[None, Unset, dict[str, Any]]
        if isinstance(self.mtm, Unset):
            mtm = UNSET
        elif isinstance(self.mtm, PatchedConfigurationMtmType0):
            mtm = self.mtm.to_dict()
        else:
            mtm = self.mtm

        release_to_ship: Union[None, Unset, str]
        if isinstance(self.release_to_ship, Unset):
            release_to_ship = UNSET
        elif isinstance(self.release_to_ship, datetime.date):
            release_to_ship = self.release_to_ship.isoformat()
        else:
            release_to_ship = self.release_to_ship

        platform = self.platform

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if canonical_label is not UNSET:
            field_dict["canonical_label"] = canonical_label
        if sku is not UNSET:
            field_dict["sku"] = sku
        if additional_names is not UNSET:
            field_dict["additional_names"] = additional_names
        if mtm is not UNSET:
            field_dict["mtm"] = mtm
        if release_to_ship is not UNSET:
            field_dict["release_to_ship"] = release_to_ship
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (
            self.id
            if isinstance(self.id, Unset)
            else (None, str(self.id).encode(), "text/plain")
        )

        name = (
            self.name
            if isinstance(self.name, Unset)
            else (None, str(self.name).encode(), "text/plain")
        )

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        canonical_label = (
            self.canonical_label
            if isinstance(self.canonical_label, Unset)
            else (None, str(self.canonical_label).encode(), "text/plain")
        )

        sku = (
            self.sku
            if isinstance(self.sku, Unset)
            else (None, str(self.sku).encode(), "text/plain")
        )

        additional_names: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.additional_names, Unset):
            _temp_additional_names = self.additional_names
            additional_names = (
                None,
                json.dumps(_temp_additional_names).encode(),
                "application/json",
            )

        mtm: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.mtm, Unset):
            mtm = UNSET
        elif isinstance(self.mtm, PatchedConfigurationMtmType0):
            mtm = (None, json.dumps(self.mtm.to_dict()).encode(), "application/json")
        else:
            mtm = (None, str(self.mtm).encode(), "text/plain")

        release_to_ship: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.release_to_ship, Unset):
            release_to_ship = UNSET
        elif isinstance(self.release_to_ship, datetime.date):
            release_to_ship = self.release_to_ship.isoformat().encode()
        else:
            release_to_ship = (None, str(self.release_to_ship).encode(), "text/plain")

        platform = (
            self.platform
            if isinstance(self.platform, Unset)
            else (None, str(self.platform).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if canonical_label is not UNSET:
            field_dict["canonical_label"] = canonical_label
        if sku is not UNSET:
            field_dict["sku"] = sku
        if additional_names is not UNSET:
            field_dict["additional_names"] = additional_names
        if mtm is not UNSET:
            field_dict["mtm"] = mtm
        if release_to_ship is not UNSET:
            field_dict["release_to_ship"] = release_to_ship
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.patched_configuration_mtm_type_0 import (
            PatchedConfigurationMtmType0,
        )

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        canonical_label = d.pop("canonical_label", UNSET)

        sku = d.pop("sku", UNSET)

        additional_names = cast(list[str], d.pop("additional_names", UNSET))

        def _parse_mtm(
            data: object,
        ) -> Union["PatchedConfigurationMtmType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mtm_type_0 = PatchedConfigurationMtmType0.from_dict(data)

                return mtm_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PatchedConfigurationMtmType0", None, Unset], data)

        mtm = _parse_mtm(d.pop("mtm", UNSET))

        def _parse_release_to_ship(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_to_ship_type_0 = isoparse(data).date()

                return release_to_ship_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        release_to_ship = _parse_release_to_ship(d.pop("release_to_ship", UNSET))

        platform = d.pop("platform", UNSET)

        patched_configuration = cls(
            id=id,
            name=name,
            description=description,
            canonical_label=canonical_label,
            sku=sku,
            additional_names=additional_names,
            mtm=mtm,
            release_to_ship=release_to_ship,
            platform=platform,
        )

        patched_configuration.additional_properties = d
        return patched_configuration

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
