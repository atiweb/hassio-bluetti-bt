"""AC2P fields."""

from typing import List

from ..base_devices.ProtocolV2Device import ProtocolV2Device
from ..utils.commands import ReadHoldingRegisters


class AC2P(ProtocolV2Device):
    def __init__(self, address: str, sn: str):
        super().__init__(address, "AC2P", sn)

        # Core fields - Using base registers from ProtocolV2Device
        # total_battery_percent (102), device_type (110-115), serial_number (116-119)
        # power_generation (154) are already defined in ProtocolV2Device
        
        # Power stats (registers 140-147)
        self.struct.add_uint_field('dc_output_power', 140)
        self.struct.add_uint_field('ac_output_power', 142)
        self.struct.add_uint_field('dc_input_power', 144)
        self.struct.add_uint_field('ac_input_power', 146)

        # Status flags
        self.struct.add_bool_field('ac_output_on', 1509)
        self.struct.add_bool_field('dc_output_on', 2012)
        self.struct.add_bool_field('power_lifting_on', 2021)
        
        # AC Output details (registers 1500, 1510-1512)
        # Register 1500: AC output frequency (x0.1 = Hz)
        self.struct.add_decimal_field('ac_output_frequency', 1500, 1)
        # Register 1510: AC output power (duplicate, already in 142)
        # Register 1511: AC output voltage (x0.1 = V)
        self.struct.add_decimal_field('internal_ac_voltage', 1511, 1)
        # Register 1512: AC output current (x0.1 = A)
        self.struct.add_decimal_field('internal_current_one', 1512, 1)
        
        # Internal temperature (register 2001)
        # Temperature is in high byte only (0x1A01 -> 0x1A = 26°C), so divide by 256
        self.struct.add_uint_field('internal_temp', 2001, multiplier=1/256)

    @property
    def polling_commands(self) -> List[ReadHoldingRegisters]:
        return [
            ReadHoldingRegisters(102, 1),    # total_battery_percent
            ReadHoldingRegisters(110, 6),    # device_type
            ReadHoldingRegisters(116, 4),    # serial_number
            ReadHoldingRegisters(140, 8),    # power stats (dc_out, ac_out, dc_in, ac_in)
            ReadHoldingRegisters(154, 1),    # power_generation
            ReadHoldingRegisters(1500, 1),   # ac_output_frequency
            ReadHoldingRegisters(1509, 1),   # ac_output_on
            ReadHoldingRegisters(1510, 3),   # ac_output_power, voltage, current
            ReadHoldingRegisters(2001, 1),   # internal_temp
            ReadHoldingRegisters(2012, 1),   # dc_output_on
            ReadHoldingRegisters(2021, 1),   # power_lifting_on
        ]

    @property
    def writable_ranges(self) -> List[range]:
        return [
            range(2021, 2022),  # power_lifting_on
        ]
