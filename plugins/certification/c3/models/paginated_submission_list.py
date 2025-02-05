from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.submission import Submission


T = TypeVar("T", bound="PaginatedSubmissionList")


@_attrs_define
class PaginatedSubmissionList:
    """
    Attributes:
        count (Union[Unset, int]):  Example: 123.
        next_ (Union[None, Unset, str]):  Example: http://api.example.org/accounts/?page=4.
        previous (Union[None, Unset, str]):  Example: http://api.example.org/accounts/?page=2.
        results (Union[Unset, list['Submission']]):
    """

    count: Union[Unset, int] = UNSET
    next_: Union[None, Unset, str] = UNSET
    previous: Union[None, Unset, str] = UNSET
    results: Union[Unset, list["Submission"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        next_: Union[None, Unset, str]
        if isinstance(self.next_, Unset):
            next_ = UNSET
        else:
            next_ = self.next_

        previous: Union[None, Unset, str]
        if isinstance(self.previous, Unset):
            previous = UNSET
        else:
            previous = self.previous

        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.submission import Submission

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        def _parse_next_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        next_ = _parse_next_(d.pop("next", UNSET))

        def _parse_previous(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous = _parse_previous(d.pop("previous", UNSET))

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = Submission.from_dict(results_item_data)

            results.append(results_item)

        paginated_submission_list = cls(
            count=count,
            next_=next_,
            previous=previous,
            results=results,
        )

        paginated_submission_list.additional_properties = d
        return paginated_submission_list

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
