from enum import Enum


class BusEnum(str, Enum):
    ATA_DEVICE = "ata_device"
    BACKLIGHT = "backlight"
    BLUETOOTH = "bluetooth"
    CCISS = "cciss"
    DMI = "dmi"
    FIREWIRE = "firewire"
    GAMEPORT = "gameport"
    IDE = "ide"
    INPUT = "input"
    MEMSTICK_HOST = "memstick_host"
    MMC = "mmc"
    MMC_HOST = "mmc_host"
    PCI = "pci"
    PLATFORM = "platform"
    PNP = "pnp"
    POWER_SUPPLY = "power_supply"
    PPDEV = "ppdev"
    RC = "rc"
    RFKILL = "rfkill"
    SCSI = "scsi"
    SCSI_HOST = "scsi_host"
    SERIO = "serio"
    SOUND = "sound"
    USB = "usb"
    USB_DEVICE = "usb_device"
    VIRTUAL = "virtual"

    def __str__(self) -> str:
        return str(self.value)
