from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_execution_dto import TestExecutionDTO


T = TypeVar("T", bound="ArtefactBuildDTO")


@_attrs_define
class ArtefactBuildDTO:
    """
    Attributes:
        id (int):
        architecture (str):
        revision (Union[None, int]):
        test_executions (list['TestExecutionDTO']):
    """

    id: int
    architecture: str
    revision: Union[None, int]
    test_executions: list["TestExecutionDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        architecture = self.architecture

        revision: Union[None, int]
        revision = self.revision

        test_executions = []
        for test_executions_item_data in self.test_executions:
            test_executions_item = test_executions_item_data.to_dict()
            test_executions.append(test_executions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "architecture": architecture,
                "revision": revision,
                "test_executions": test_executions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.test_execution_dto import TestExecutionDTO

        d = src_dict.copy()
        id = d.pop("id")

        architecture = d.pop("architecture")

        def _parse_revision(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        revision = _parse_revision(d.pop("revision"))

        test_executions = []
        _test_executions = d.pop("test_executions")
        for test_executions_item_data in _test_executions:
            test_executions_item = TestExecutionDTO.from_dict(test_executions_item_data)

            test_executions.append(test_executions_item)

        artefact_build_dto = cls(
            id=id,
            architecture=architecture,
            revision=revision,
            test_executions=test_executions,
        )

        artefact_build_dto.additional_properties = d
        return artefact_build_dto

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
