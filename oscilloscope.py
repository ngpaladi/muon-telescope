import pyvisa as visa
from enum import Enum

class TriggerStatus:
    def __init__(self, internal_state_register:int) -> None:
        self.ready = bool((internal_state_register & 8192) !=0 )
        self.triggered = bool((internal_state_register & 1) !=0 )
        return

class ChannelType(Enum):
    AC = auto()
    DC = auto()

class Channel:
    def __init__(self, id:int, name:str, units:str, division:float, offset:float, ) -> None:
        self.name = name
        self.id = id
        self.units = units
        self.division = division
        return

class Waveform:
    def __init__(self, data:str, channel:Channel) -> None:
        self.values = []
        self.units = channel.units
        self.interval = 0.
        self.interval_units = 0.
        return

class Oscilloscope:
    def __init__(self, connection_string: str) -> None:
        self.scpi = self.resource_manager.open_resource(connection_string)
        self.scpi.read_termination = '\n'
        self.scpi.write_termination = '\n'
        self.channels = {}

    def add_channel(self, channel:Channel) -> Channel:


    def write(self, string: str) -> str:
        return self.scpi.write(string)

    def query(self, string: str) -> str:
        return self.scpi.query(string)

    def read(self, string: str) -> str:
        return self.scpi.read(string)
    
    def trigger_status(self) -> TriggerStatus:
        return TriggerStatus(int(self.scpi.query("INR?")))
    
    def waveform(self, channel_id:int) -> Waveform:
        return Waveform()

    
    def initialize(self) -> None:
        self.scpi.write("CHDR OFF")
        return