from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArtefactBuildMinimalResponse")


@_attrs_define
class ArtefactBuildMinimalResponse:
    """
    Attributes:
        id (int):
        architecture (str):
        revision (Union[None, int]):
    """

    id: int
    architecture: str
    revision: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        architecture = self.architecture

        revision: Union[None, int]
        revision = self.revision

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "architecture": architecture,
                "revision": revision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        architecture = d.pop("architecture")

        def _parse_revision(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        revision = _parse_revision(d.pop("revision"))

        artefact_build_minimal_response = cls(
            id=id,
            architecture=architecture,
            revision=revision,
        )

        artefact_build_minimal_response.additional_properties = d
        return artefact_build_minimal_response

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
