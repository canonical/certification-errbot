from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.level_enum import LevelEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.certified_configuration_details_network_item import (
        CertifiedConfigurationDetailsNetworkItem,
    )
    from ..models.certified_configuration_details_notes_item import (
        CertifiedConfigurationDetailsNotesItem,
    )
    from ..models.certified_configuration_details_processor_item import (
        CertifiedConfigurationDetailsProcessorItem,
    )
    from ..models.certified_configuration_details_video_item import (
        CertifiedConfigurationDetailsVideoItem,
    )
    from ..models.certified_configuration_details_wireless_item import (
        CertifiedConfigurationDetailsWirelessItem,
    )


T = TypeVar("T", bound="CertifiedConfigurationDetails")


@_attrs_define
class CertifiedConfigurationDetails:
    """Serializer for Certified Configuration Details objects

    Attributes:
        id (int):
        canonical_id (str):
        architecture (str):
        bios (str):
        hardware_website (str):
        category (str): The category of a machine comes from the form factor of the platform.

            Some form factors have parent form factors, in which
            case we return the parent form factor name
        kernel_version (str): Return the kernel version that was tested for this certificate.

            Based on the certified_kernel_version method in the Certificate model.
        notes (list['CertifiedConfigurationDetailsNotesItem']): Returns all the notes related to the certificate.

            The notes cannot be prefetched with the certificate, as they are not
            directly related to the certificate object.
        make (str):
        model (str):
        platform_name (str):
        platform_id (str):
        processor (list['CertifiedConfigurationDetailsProcessorItem']): Returns the processor information of the
            configuration certified
        network (list['CertifiedConfigurationDetailsNetworkItem']): Returns the network information of the configuration
            certified
        video (list['CertifiedConfigurationDetailsVideoItem']): Returns the video card (GPU) information of the
            configuration certified
        wireless (list['CertifiedConfigurationDetailsWirelessItem']): Returns the wireless card information of the
            configuration certified
        certified_release (str):
        form_factor (str):
        platform_certified_configuration_count (int): Returns the number of certificates for the platform
        level (Union[BlankEnum, LevelEnum, Unset]):
        name (Union[None, Unset, str]):
    """

    id: int
    canonical_id: str
    architecture: str
    bios: str
    hardware_website: str
    category: str
    kernel_version: str
    notes: list["CertifiedConfigurationDetailsNotesItem"]
    make: str
    model: str
    platform_name: str
    platform_id: str
    processor: list["CertifiedConfigurationDetailsProcessorItem"]
    network: list["CertifiedConfigurationDetailsNetworkItem"]
    video: list["CertifiedConfigurationDetailsVideoItem"]
    wireless: list["CertifiedConfigurationDetailsWirelessItem"]
    certified_release: str
    form_factor: str
    platform_certified_configuration_count: int
    level: Union[BlankEnum, LevelEnum, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        canonical_id = self.canonical_id

        architecture = self.architecture

        bios = self.bios

        hardware_website = self.hardware_website

        category = self.category

        kernel_version = self.kernel_version

        notes = []
        for notes_item_data in self.notes:
            notes_item = notes_item_data.to_dict()
            notes.append(notes_item)

        make = self.make

        model = self.model

        platform_name = self.platform_name

        platform_id = self.platform_id

        processor = []
        for processor_item_data in self.processor:
            processor_item = processor_item_data.to_dict()
            processor.append(processor_item)

        network = []
        for network_item_data in self.network:
            network_item = network_item_data.to_dict()
            network.append(network_item)

        video = []
        for video_item_data in self.video:
            video_item = video_item_data.to_dict()
            video.append(video_item)

        wireless = []
        for wireless_item_data in self.wireless:
            wireless_item = wireless_item_data.to_dict()
            wireless.append(wireless_item)

        certified_release = self.certified_release

        form_factor = self.form_factor

        platform_certified_configuration_count = (
            self.platform_certified_configuration_count
        )

        level: Union[Unset, str]
        if isinstance(self.level, Unset):
            level = UNSET
        elif isinstance(self.level, LevelEnum):
            level = self.level.value
        else:
            level = self.level.value

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "canonical_id": canonical_id,
                "architecture": architecture,
                "bios": bios,
                "hardware_website": hardware_website,
                "category": category,
                "kernel_version": kernel_version,
                "notes": notes,
                "make": make,
                "model": model,
                "platform_name": platform_name,
                "platform_id": platform_id,
                "processor": processor,
                "network": network,
                "video": video,
                "wireless": wireless,
                "certified_release": certified_release,
                "form_factor": form_factor,
                "platform_certified_configuration_count": platform_certified_configuration_count,
            }
        )
        if level is not UNSET:
            field_dict["level"] = level
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.certified_configuration_details_network_item import (
            CertifiedConfigurationDetailsNetworkItem,
        )
        from ..models.certified_configuration_details_notes_item import (
            CertifiedConfigurationDetailsNotesItem,
        )
        from ..models.certified_configuration_details_processor_item import (
            CertifiedConfigurationDetailsProcessorItem,
        )
        from ..models.certified_configuration_details_video_item import (
            CertifiedConfigurationDetailsVideoItem,
        )
        from ..models.certified_configuration_details_wireless_item import (
            CertifiedConfigurationDetailsWirelessItem,
        )

        d = src_dict.copy()
        id = d.pop("id")

        canonical_id = d.pop("canonical_id")

        architecture = d.pop("architecture")

        bios = d.pop("bios")

        hardware_website = d.pop("hardware_website")

        category = d.pop("category")

        kernel_version = d.pop("kernel_version")

        notes = []
        _notes = d.pop("notes")
        for notes_item_data in _notes:
            notes_item = CertifiedConfigurationDetailsNotesItem.from_dict(
                notes_item_data
            )

            notes.append(notes_item)

        make = d.pop("make")

        model = d.pop("model")

        platform_name = d.pop("platform_name")

        platform_id = d.pop("platform_id")

        processor = []
        _processor = d.pop("processor")
        for processor_item_data in _processor:
            processor_item = CertifiedConfigurationDetailsProcessorItem.from_dict(
                processor_item_data
            )

            processor.append(processor_item)

        network = []
        _network = d.pop("network")
        for network_item_data in _network:
            network_item = CertifiedConfigurationDetailsNetworkItem.from_dict(
                network_item_data
            )

            network.append(network_item)

        video = []
        _video = d.pop("video")
        for video_item_data in _video:
            video_item = CertifiedConfigurationDetailsVideoItem.from_dict(
                video_item_data
            )

            video.append(video_item)

        wireless = []
        _wireless = d.pop("wireless")
        for wireless_item_data in _wireless:
            wireless_item = CertifiedConfigurationDetailsWirelessItem.from_dict(
                wireless_item_data
            )

            wireless.append(wireless_item)

        certified_release = d.pop("certified_release")

        form_factor = d.pop("form_factor")

        platform_certified_configuration_count = d.pop(
            "platform_certified_configuration_count"
        )

        def _parse_level(data: object) -> Union[BlankEnum, LevelEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                level_type_0 = LevelEnum(data)

                return level_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            level_type_1 = BlankEnum(data)

            return level_type_1

        level = _parse_level(d.pop("level", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        certified_configuration_details = cls(
            id=id,
            canonical_id=canonical_id,
            architecture=architecture,
            bios=bios,
            hardware_website=hardware_website,
            category=category,
            kernel_version=kernel_version,
            notes=notes,
            make=make,
            model=model,
            platform_name=platform_name,
            platform_id=platform_id,
            processor=processor,
            network=network,
            video=video,
            wireless=wireless,
            certified_release=certified_release,
            form_factor=form_factor,
            platform_certified_configuration_count=platform_certified_configuration_count,
            level=level,
            name=name,
        )

        certified_configuration_details.additional_properties = d
        return certified_configuration_details

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
