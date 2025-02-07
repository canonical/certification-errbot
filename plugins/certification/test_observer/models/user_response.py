from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """
    Attributes:
        id (int):
        launchpad_handle (str):
        launchpad_email (str):
        name (str):
    """

    id: int
    launchpad_handle: str
    launchpad_email: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        launchpad_handle = self.launchpad_handle

        launchpad_email = self.launchpad_email

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "launchpad_handle": launchpad_handle,
                "launchpad_email": launchpad_email,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        launchpad_handle = d.pop("launchpad_handle")

        launchpad_email = d.pop("launchpad_email")

        name = d.pop("name")

        user_response = cls(
            id=id,
            launchpad_handle=launchpad_handle,
            launchpad_email=launchpad_email,
            name=name,
        )

        user_response.additional_properties = d
        return user_response

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
