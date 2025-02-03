from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.family_name import FamilyName

if TYPE_CHECKING:
    from ..models.artefact_build_minimal_dto import ArtefactBuildMinimalDTO
    from ..models.artefact_dto import ArtefactDTO
    from ..models.test_execution_dto import TestExecutionDTO


T = TypeVar("T", bound="PendingRerun")


@_attrs_define
class PendingRerun:
    """
    Attributes:
        test_execution_id (int):
        ci_link (Union[None, str]):
        family (FamilyName):
        test_execution (TestExecutionDTO):
        artefact (ArtefactDTO):
        artefact_build (ArtefactBuildMinimalDTO):
    """

    test_execution_id: int
    ci_link: Union[None, str]
    family: FamilyName
    test_execution: "TestExecutionDTO"
    artefact: "ArtefactDTO"
    artefact_build: "ArtefactBuildMinimalDTO"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        test_execution_id = self.test_execution_id

        ci_link: Union[None, str]
        ci_link = self.ci_link

        family = self.family.value

        test_execution = self.test_execution.to_dict()

        artefact = self.artefact.to_dict()

        artefact_build = self.artefact_build.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_execution_id": test_execution_id,
                "ci_link": ci_link,
                "family": family,
                "test_execution": test_execution,
                "artefact": artefact,
                "artefact_build": artefact_build,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.artefact_build_minimal_dto import ArtefactBuildMinimalDTO
        from ..models.artefact_dto import ArtefactDTO
        from ..models.test_execution_dto import TestExecutionDTO

        d = src_dict.copy()
        test_execution_id = d.pop("test_execution_id")

        def _parse_ci_link(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ci_link = _parse_ci_link(d.pop("ci_link"))

        family = FamilyName(d.pop("family"))

        test_execution = TestExecutionDTO.from_dict(d.pop("test_execution"))

        artefact = ArtefactDTO.from_dict(d.pop("artefact"))

        artefact_build = ArtefactBuildMinimalDTO.from_dict(d.pop("artefact_build"))

        pending_rerun = cls(
            test_execution_id=test_execution_id,
            ci_link=ci_link,
            family=family,
            test_execution=test_execution,
            artefact=artefact,
            artefact_build=artefact_build,
        )

        pending_rerun.additional_properties = d
        return pending_rerun

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
