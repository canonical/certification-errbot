from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LaunchpadPerson")


@_attrs_define
class LaunchpadPerson:
    """Serializer for LaunchpadPerson objects.

    Attributes:
        id (int):
        name (str):
        launchpad_status (str):
        display_name (Union[Unset, str]):
        self_link (Union[Unset, str]):
    """

    id: int
    name: str
    launchpad_status: str
    display_name: Union[Unset, str] = UNSET
    self_link: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        launchpad_status = self.launchpad_status

        display_name = self.display_name

        self_link = self.self_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "launchpad_status": launchpad_status,
            }
        )
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if self_link is not UNSET:
            field_dict["self_link"] = self_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        launchpad_status = d.pop("launchpad_status")

        display_name = d.pop("display_name", UNSET)

        self_link = d.pop("self_link", UNSET)

        launchpad_person = cls(
            id=id,
            name=name,
            launchpad_status=launchpad_status,
            display_name=display_name,
            self_link=self_link,
        )

        launchpad_person.additional_properties = d
        return launchpad_person

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
