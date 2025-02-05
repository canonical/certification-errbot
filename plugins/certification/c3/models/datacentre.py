from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datacentre_env_var_type_0 import DatacentreEnvVarType0


T = TypeVar("T", bound="Datacentre")


@_attrs_define
class Datacentre:
    """Serializer for DataCentre objects

    Attributes:
        id (int):
        name (str):
        env_var (Union['DatacentreEnvVarType0', None, Unset]):
    """

    id: int
    name: str
    env_var: Union["DatacentreEnvVarType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datacentre_env_var_type_0 import DatacentreEnvVarType0

        id = self.id

        name = self.name

        env_var: Union[None, Unset, dict[str, Any]]
        if isinstance(self.env_var, Unset):
            env_var = UNSET
        elif isinstance(self.env_var, DatacentreEnvVarType0):
            env_var = self.env_var.to_dict()
        else:
            env_var = self.env_var

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if env_var is not UNSET:
            field_dict["env_var"] = env_var

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.datacentre_env_var_type_0 import DatacentreEnvVarType0

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        def _parse_env_var(data: object) -> Union["DatacentreEnvVarType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_var_type_0 = DatacentreEnvVarType0.from_dict(data)

                return env_var_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatacentreEnvVarType0", None, Unset], data)

        env_var = _parse_env_var(d.pop("env_var", UNSET))

        datacentre = cls(
            id=id,
            name=name,
            env_var=env_var,
        )

        datacentre.additional_properties = d
        return datacentre

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
