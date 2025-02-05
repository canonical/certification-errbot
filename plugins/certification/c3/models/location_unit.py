from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LocationUnit")


@_attrs_define
class LocationUnit:
    """Serializer for LocationUnit objects

    This serializer is designed exclusively for read operations, presenting
    detailed information about LocationUnit instances.

        Attributes:
            frame (Union[None, str]):
            shelf (int):
            partition (int):
    """

    frame: Union[None, str]
    shelf: int
    partition: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        frame: Union[None, str]
        frame = self.frame

        shelf = self.shelf

        partition = self.partition

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "frame": frame,
                "shelf": shelf,
                "partition": partition,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_frame(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        frame = _parse_frame(d.pop("frame"))

        shelf = d.pop("shelf")

        partition = d.pop("partition")

        location_unit = cls(
            frame=frame,
            shelf=shelf,
            partition=partition,
        )

        location_unit.additional_properties = d
        return location_unit

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
