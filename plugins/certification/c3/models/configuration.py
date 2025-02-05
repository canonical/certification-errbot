import datetime
import json
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_mtm_type_0 import ConfigurationMtmType0


T = TypeVar("T", bound="Configuration")


@_attrs_define
class Configuration:
    """Serializer for Configuration objects

    Attributes:
        id (int):
        name (str): Model name for a group of machines. Should be unique within a platform
        platform (int): Platform as parent object associated with the configuration
        description (Union[Unset, str]):
        canonical_label (Union[Unset, str]):
        sku (Union[Unset, str]): OEM specific configuration name
        additional_names (Union[Unset, list[str]]):
        mtm (Union['ConfigurationMtmType0', None, Unset]): Vendor specific JSONB metadata
        release_to_ship (Union[None, Unset, datetime.date]): Date when the hardware information can be released
    """

    id: int
    name: str
    platform: int
    description: Union[Unset, str] = UNSET
    canonical_label: Union[Unset, str] = UNSET
    sku: Union[Unset, str] = UNSET
    additional_names: Union[Unset, list[str]] = UNSET
    mtm: Union["ConfigurationMtmType0", None, Unset] = UNSET
    release_to_ship: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.configuration_mtm_type_0 import ConfigurationMtmType0

        id = self.id

        name = self.name

        platform = self.platform

        description = self.description

        canonical_label = self.canonical_label

        sku = self.sku

        additional_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.additional_names, Unset):
            additional_names = self.additional_names

        mtm: Union[None, Unset, dict[str, Any]]
        if isinstance(self.mtm, Unset):
            mtm = UNSET
        elif isinstance(self.mtm, ConfigurationMtmType0):
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "platform": platform,
            }
        )
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

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        platform = (None, str(self.platform).encode(), "text/plain")

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
        elif isinstance(self.mtm, ConfigurationMtmType0):
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

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "name": name,
                "platform": platform,
            }
        )
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.configuration_mtm_type_0 import ConfigurationMtmType0

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        platform = d.pop("platform")

        description = d.pop("description", UNSET)

        canonical_label = d.pop("canonical_label", UNSET)

        sku = d.pop("sku", UNSET)

        additional_names = cast(list[str], d.pop("additional_names", UNSET))

        def _parse_mtm(data: object) -> Union["ConfigurationMtmType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mtm_type_0 = ConfigurationMtmType0.from_dict(data)

                return mtm_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ConfigurationMtmType0", None, Unset], data)

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

        configuration = cls(
            id=id,
            name=name,
            platform=platform,
            description=description,
            canonical_label=canonical_label,
            sku=sku,
            additional_names=additional_names,
            mtm=mtm,
            release_to_ship=release_to_ship,
        )

        configuration.additional_properties = d
        return configuration

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
