from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Outlet")


@_attrs_define
class Outlet:
    """Serializer for Outlet objects

    Attributes:
        pdu_make (Union[None, str]):
        pdu_ip (Union[None, str]):
        outlet (int):
    """

    pdu_make: Union[None, str]
    pdu_ip: Union[None, str]
    outlet: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pdu_make: Union[None, str]
        pdu_make = self.pdu_make

        pdu_ip: Union[None, str]
        pdu_ip = self.pdu_ip

        outlet = self.outlet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pdu_make": pdu_make,
                "pdu_ip": pdu_ip,
                "outlet": outlet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_pdu_make(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pdu_make = _parse_pdu_make(d.pop("pdu_make"))

        def _parse_pdu_ip(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pdu_ip = _parse_pdu_ip(d.pop("pdu_ip"))

        outlet = d.pop("outlet")

        outlet = cls(
            pdu_make=pdu_make,
            pdu_ip=pdu_ip,
            outlet=outlet,
        )

        outlet.additional_properties = d
        return outlet

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
