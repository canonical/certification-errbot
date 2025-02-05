from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.component_release_status import ComponentReleaseStatus


T = TypeVar("T", bound="ComponentSummaries")


@_attrs_define
class ComponentSummaries:
    """Serializer for Component Device objects, used for the component summaries API

    Attributes:
        archived (bool): inactive project
        category (str): Category of the device, e.g. WIRELESS, VIDEO, etc.
        hardware_vendor_make (str): The independent hardware vendor (IHV) who made the component
        id (int):
        identifier (str):
        lts_releases (str):
        machine_canonical_ids (str):
        model (str):
        note (str):
        part_number (str):
        statuses (list['ComponentReleaseStatus']):
        subsystem_identifier (str):
        vendor_make (str): The vendor's marketing name for the make
        vendor_name (str):
    """

    archived: bool
    category: str
    hardware_vendor_make: str
    id: int
    identifier: str
    lts_releases: str
    machine_canonical_ids: str
    model: str
    note: str
    part_number: str
    statuses: list["ComponentReleaseStatus"]
    subsystem_identifier: str
    vendor_make: str
    vendor_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        archived = self.archived

        category = self.category

        hardware_vendor_make = self.hardware_vendor_make

        id = self.id

        identifier = self.identifier

        lts_releases = self.lts_releases

        machine_canonical_ids = self.machine_canonical_ids

        model = self.model

        note = self.note

        part_number = self.part_number

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()
            statuses.append(statuses_item)

        subsystem_identifier = self.subsystem_identifier

        vendor_make = self.vendor_make

        vendor_name = self.vendor_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "archived": archived,
                "category": category,
                "hardware_vendor_make": hardware_vendor_make,
                "id": id,
                "identifier": identifier,
                "lts_releases": lts_releases,
                "machine_canonical_ids": machine_canonical_ids,
                "model": model,
                "note": note,
                "part_number": part_number,
                "statuses": statuses,
                "subsystem_identifier": subsystem_identifier,
                "vendor_make": vendor_make,
                "vendor_name": vendor_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.component_release_status import ComponentReleaseStatus

        d = src_dict.copy()
        archived = d.pop("archived")

        category = d.pop("category")

        hardware_vendor_make = d.pop("hardware_vendor_make")

        id = d.pop("id")

        identifier = d.pop("identifier")

        lts_releases = d.pop("lts_releases")

        machine_canonical_ids = d.pop("machine_canonical_ids")

        model = d.pop("model")

        note = d.pop("note")

        part_number = d.pop("part_number")

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = ComponentReleaseStatus.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        subsystem_identifier = d.pop("subsystem_identifier")

        vendor_make = d.pop("vendor_make")

        vendor_name = d.pop("vendor_name")

        component_summaries = cls(
            archived=archived,
            category=category,
            hardware_vendor_make=hardware_vendor_make,
            id=id,
            identifier=identifier,
            lts_releases=lts_releases,
            machine_canonical_ids=machine_canonical_ids,
            model=model,
            note=note,
            part_number=part_number,
            statuses=statuses,
            subsystem_identifier=subsystem_identifier,
            vendor_make=vendor_make,
            vendor_name=vendor_name,
        )

        component_summaries.additional_properties = d
        return component_summaries

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
