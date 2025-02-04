from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.artefact_build_environment_review_decision import (
    ArtefactBuildEnvironmentReviewDecision,
)

if TYPE_CHECKING:
    from ..models.artefact_build_minimal_dto import ArtefactBuildMinimalDTO
    from ..models.environment_dto import EnvironmentDTO


T = TypeVar("T", bound="ArtefactBuildEnvironmentReviewDTO")


@_attrs_define
class ArtefactBuildEnvironmentReviewDTO:
    """
    Attributes:
        id (int):
        review_decision (list[ArtefactBuildEnvironmentReviewDecision]):
        review_comment (str):
        environment (EnvironmentDTO):
        artefact_build (ArtefactBuildMinimalDTO):
    """

    id: int
    review_decision: list[ArtefactBuildEnvironmentReviewDecision]
    review_comment: str
    environment: "EnvironmentDTO"
    artefact_build: "ArtefactBuildMinimalDTO"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        review_decision = []
        for review_decision_item_data in self.review_decision:
            review_decision_item = review_decision_item_data.value
            review_decision.append(review_decision_item)

        review_comment = self.review_comment

        environment = self.environment.to_dict()

        artefact_build = self.artefact_build.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "review_decision": review_decision,
                "review_comment": review_comment,
                "environment": environment,
                "artefact_build": artefact_build,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.artefact_build_minimal_dto import ArtefactBuildMinimalDTO
        from ..models.environment_dto import EnvironmentDTO

        d = src_dict.copy()
        id = d.pop("id")

        review_decision = []
        _review_decision = d.pop("review_decision")
        for review_decision_item_data in _review_decision:
            review_decision_item = ArtefactBuildEnvironmentReviewDecision(
                review_decision_item_data
            )

            review_decision.append(review_decision_item)

        review_comment = d.pop("review_comment")

        environment = EnvironmentDTO.from_dict(d.pop("environment"))

        artefact_build = ArtefactBuildMinimalDTO.from_dict(d.pop("artefact_build"))

        artefact_build_environment_review_dto = cls(
            id=id,
            review_decision=review_decision,
            review_comment=review_comment,
            environment=environment,
            artefact_build=artefact_build,
        )

        artefact_build_environment_review_dto.additional_properties = d
        return artefact_build_environment_review_dto

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
