import pyvisa as visa
from enum import Enum, auto


class TriggerStatus:
    def __init__(self, internal_state_register: int) -> None:
        self.ready = bool((internal_state_register & 8192) != 0)
        self.triggered = bool((internal_state_register & 1) != 0)
        return


class ChannelType(Enum):
    AC = auto()
    DC = auto()
    Digital = auto()


class Channel:
    def __init__(self, channel_id: int, volts_per_division: float, voltage_offset: float, channel_type: ChannelType) -> None:
        self.id = channel_id
        self.type = channel_type
        self.volts_per_division = volts_per_division
        self.voltage_offset = voltage_offset
        return


class Waveform:
    def __init__(self, raw_data, channel: Channel, sampling_rate: float, time_per_division: float) -> None:
        self.values = []
        self.times = []
        self.units = 'V'
        self.time_units = 's'

        data = list(raw_data)[15:]
        data.pop()
        data.pop()

        for value in data:
            if value > 127:
                value = value - 256
            else:
                pass
            self.values.append(value)

        for i in range(0,len(self.values)):
            self.values[i] = self.values[i]/25*channel.volts_per_division-channel.voltage_offset
            self.times.append(-(time_per_division*14/2)+i*(1/sampling_rate))     
        return

    def __str__(self):
        return ','.join(str(i) for i in self.values)


class Oscilloscope:
    def __init__(self, connection_string: str) -> None:
        self.scpi = self.resource_manager.open_resource(connection_string)
        self.scpi.read_termination = '\n'
        self.scpi.write_termination = '\n'
        self.channels = {}
        self.initialize()
        return
    
    def timeout(self, timeout_length:int = -1) -> int:
        if timeout_length > 0:
            self.scpi.timeout = timeout_length
        else:
            pass
        return self.scpi.timeout

    def chunk_size(self, chunk_size:int = -1) -> int:
        if chunk_size > 0:
            self.scpi.chunk_size = chunk_size
        else:
            pass
        return self.scpi.chunk_size

    def add_channel(self, channel_id: int) -> Channel:
        volts_per_division = float(self.scpi.query("c%d:vdiv?" % channel_id))
        volatage_offset = float(self.scpi.query("c%d:ofst?" % channel_id))
        self.channels[channel_id] = Channel()
        return

    def write(self, string: str) -> str:
        return self.scpi.write(string)

    def query(self, string: str) -> str:
        return self.scpi.query(string)

    def read(self, string: str) -> str:
        return self.scpi.read(string)

    def trigger_status(self) -> TriggerStatus:
        return TriggerStatus(int(self.scpi.query("INR?")))

    def waveform(self, channel_id: int) -> Waveform:
        return Waveform()

    def initialize(self) -> None:
        self.scpi.write("CHDR OFF")
        sample_rate = self.scpi.query("sara?")
        sample_rate_unit = {'G':1E9,'M':1E6,'k':1E3}
        for unit in sample_rate_unit.keys():
            if sample_rate.find(unit)!=-1:
                sample_rate = sample_rate.split(unit)
                sample_rate = float(sample_rate[0])*sample_rate_unit[unit]
                break
        self.sample_rate = float(sample_rate)
        self.time_per_division = self.scpi.query("tdiv?")
        return
