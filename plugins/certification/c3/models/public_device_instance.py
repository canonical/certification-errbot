from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.device import Device


T = TypeVar("T", bound="PublicDeviceInstance")


@_attrs_define
class PublicDeviceInstance:
    """Serialize devices for certified machines

    Attributes:
        machine_canonical_id (str):
        certificate_name (str): Name of the certificate that has the report attached to it
        device (Device): Serializer for the Device model
        driver_name (str):
        cpu_codename (str):
    """

    machine_canonical_id: str
    certificate_name: str
    device: "Device"
    driver_name: str
    cpu_codename: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        machine_canonical_id = self.machine_canonical_id

        certificate_name = self.certificate_name

        device = self.device.to_dict()

        driver_name = self.driver_name

        cpu_codename = self.cpu_codename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "machine_canonical_id": machine_canonical_id,
                "certificate_name": certificate_name,
                "device": device,
                "driver_name": driver_name,
                "cpu_codename": cpu_codename,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.device import Device

        d = src_dict.copy()
        machine_canonical_id = d.pop("machine_canonical_id")

        certificate_name = d.pop("certificate_name")

        device = Device.from_dict(d.pop("device"))

        driver_name = d.pop("driver_name")

        cpu_codename = d.pop("cpu_codename")

        public_device_instance = cls(
            machine_canonical_id=machine_canonical_id,
            certificate_name=certificate_name,
            device=device,
            driver_name=driver_name,
            cpu_codename=cpu_codename,
        )

        public_device_instance.additional_properties = d
        return public_device_instance

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
