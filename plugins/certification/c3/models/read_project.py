import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.image import Image
    from ..models.launchpad_person import LaunchpadPerson
    from ..models.platform import Platform


T = TypeVar("T", bound="ReadProject")


@_attrs_define
class ReadProject:
    """
    Attributes:
        id (int):
        name (str):
        description (str):
        documentation_url (Union[None, str]):
        contact (LaunchpadPerson): Serializer for LaunchpadPerson objects.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        images (list['Image']):
        platforms (list['Platform']):
    """

    id: int
    name: str
    description: str
    documentation_url: Union[None, str]
    contact: "LaunchpadPerson"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    images: list["Image"]
    platforms: list["Platform"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        documentation_url: Union[None, str]
        documentation_url = self.documentation_url

        contact = self.contact.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()
            images.append(images_item)

        platforms = []
        for platforms_item_data in self.platforms:
            platforms_item = platforms_item_data.to_dict()
            platforms.append(platforms_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "documentation_url": documentation_url,
                "contact": contact,
                "created_at": created_at,
                "updated_at": updated_at,
                "images": images,
                "platforms": platforms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.image import Image
        from ..models.launchpad_person import LaunchpadPerson
        from ..models.platform import Platform

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        def _parse_documentation_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        documentation_url = _parse_documentation_url(d.pop("documentation_url"))

        contact = LaunchpadPerson.from_dict(d.pop("contact"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        images = []
        _images = d.pop("images")
        for images_item_data in _images:
            images_item = Image.from_dict(images_item_data)

            images.append(images_item)

        platforms = []
        _platforms = d.pop("platforms")
        for platforms_item_data in _platforms:
            platforms_item = Platform.from_dict(platforms_item_data)

            platforms.append(platforms_item)

        read_project = cls(
            id=id,
            name=name,
            description=description,
            documentation_url=documentation_url,
            contact=contact,
            created_at=created_at,
            updated_at=updated_at,
            images=images,
            platforms=platforms,
        )

        read_project.additional_properties = d
        return read_project

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
