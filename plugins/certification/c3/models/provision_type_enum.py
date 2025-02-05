from enum import Enum


class ProvisionTypeEnum(str, Enum):
    CM3 = "cm3"
    DELL_OEMSCRIPT = "dell_oemscript"
    HP_OEMSCRIPT = "hp_oemscript"
    LENOVO_OEMSCRIPT = "lenovo_oemscript"
    MAAS = "maas"
    MUXPI = "muxpi"
    NETBOOT = "netboot"
    NOPROVISION = "noprovision"
    OEMRECOVERY = "oemrecovery"
    OEMSCRIPT = "oemscript"
    OEM_AUTOINSTALL = "oem_autoinstall"
    RPI3 = "rpi3"
    SDWIRE = "sdwire"
    ZAPPER_IOT = "zapper_iot"
    ZAPPER_KVM = "zapper_kvm"

    def __str__(self) -> str:
        return str(self.value)
