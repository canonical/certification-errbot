from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """Serializer for Account objects.

    Attributes:
        id (int):
        account_type (str):
        secure_id (str):
        name (Union[None, Unset, str]):
        website (Union[None, Unset, str]):
        phone (Union[None, Unset, str]):
        fax (Union[None, Unset, str]):
        billing_street (Union[None, Unset, str]):
        billing_city (Union[None, Unset, str]):
        billing_state (Union[None, Unset, str]):
        billing_postal_code (Union[None, Unset, str]):
        billing_country (Union[None, Unset, str]):
        record_type_id (Union[None, Unset, str]):
        display_groups (Union[Unset, str]): Comma-separated list of User Groups that the Accounts page will show as
            direct members of the Account.
        user_groups (Union[Unset, list[int]]):
    """

    id: int
    account_type: str
    secure_id: str
    name: Union[None, Unset, str] = UNSET
    website: Union[None, Unset, str] = UNSET
    phone: Union[None, Unset, str] = UNSET
    fax: Union[None, Unset, str] = UNSET
    billing_street: Union[None, Unset, str] = UNSET
    billing_city: Union[None, Unset, str] = UNSET
    billing_state: Union[None, Unset, str] = UNSET
    billing_postal_code: Union[None, Unset, str] = UNSET
    billing_country: Union[None, Unset, str] = UNSET
    record_type_id: Union[None, Unset, str] = UNSET
    display_groups: Union[Unset, str] = UNSET
    user_groups: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        account_type = self.account_type

        secure_id = self.secure_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        website: Union[None, Unset, str]
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        phone: Union[None, Unset, str]
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        fax: Union[None, Unset, str]
        if isinstance(self.fax, Unset):
            fax = UNSET
        else:
            fax = self.fax

        billing_street: Union[None, Unset, str]
        if isinstance(self.billing_street, Unset):
            billing_street = UNSET
        else:
            billing_street = self.billing_street

        billing_city: Union[None, Unset, str]
        if isinstance(self.billing_city, Unset):
            billing_city = UNSET
        else:
            billing_city = self.billing_city

        billing_state: Union[None, Unset, str]
        if isinstance(self.billing_state, Unset):
            billing_state = UNSET
        else:
            billing_state = self.billing_state

        billing_postal_code: Union[None, Unset, str]
        if isinstance(self.billing_postal_code, Unset):
            billing_postal_code = UNSET
        else:
            billing_postal_code = self.billing_postal_code

        billing_country: Union[None, Unset, str]
        if isinstance(self.billing_country, Unset):
            billing_country = UNSET
        else:
            billing_country = self.billing_country

        record_type_id: Union[None, Unset, str]
        if isinstance(self.record_type_id, Unset):
            record_type_id = UNSET
        else:
            record_type_id = self.record_type_id

        display_groups = self.display_groups

        user_groups: Union[Unset, list[int]] = UNSET
        if not isinstance(self.user_groups, Unset):
            user_groups = self.user_groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "account_type": account_type,
                "secure_id": secure_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if website is not UNSET:
            field_dict["website"] = website
        if phone is not UNSET:
            field_dict["phone"] = phone
        if fax is not UNSET:
            field_dict["fax"] = fax
        if billing_street is not UNSET:
            field_dict["billing_street"] = billing_street
        if billing_city is not UNSET:
            field_dict["billing_city"] = billing_city
        if billing_state is not UNSET:
            field_dict["billing_state"] = billing_state
        if billing_postal_code is not UNSET:
            field_dict["billing_postal_code"] = billing_postal_code
        if billing_country is not UNSET:
            field_dict["billing_country"] = billing_country
        if record_type_id is not UNSET:
            field_dict["record_type_id"] = record_type_id
        if display_groups is not UNSET:
            field_dict["display_groups"] = display_groups
        if user_groups is not UNSET:
            field_dict["user_groups"] = user_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        account_type = d.pop("account_type")

        secure_id = d.pop("secure_id")

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_website(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        website = _parse_website(d.pop("website", UNSET))

        def _parse_phone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_fax(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fax = _parse_fax(d.pop("fax", UNSET))

        def _parse_billing_street(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        billing_street = _parse_billing_street(d.pop("billing_street", UNSET))

        def _parse_billing_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        billing_city = _parse_billing_city(d.pop("billing_city", UNSET))

        def _parse_billing_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        billing_state = _parse_billing_state(d.pop("billing_state", UNSET))

        def _parse_billing_postal_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        billing_postal_code = _parse_billing_postal_code(
            d.pop("billing_postal_code", UNSET)
        )

        def _parse_billing_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        billing_country = _parse_billing_country(d.pop("billing_country", UNSET))

        def _parse_record_type_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        record_type_id = _parse_record_type_id(d.pop("record_type_id", UNSET))

        display_groups = d.pop("display_groups", UNSET)

        user_groups = cast(list[int], d.pop("user_groups", UNSET))

        account = cls(
            id=id,
            account_type=account_type,
            secure_id=secure_id,
            name=name,
            website=website,
            phone=phone,
            fax=fax,
            billing_street=billing_street,
            billing_city=billing_city,
            billing_state=billing_state,
            billing_postal_code=billing_postal_code,
            billing_country=billing_country,
            record_type_id=record_type_id,
            display_groups=display_groups,
            user_groups=user_groups,
        )

        account.additional_properties = d
        return account

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
