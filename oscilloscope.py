import pyvisa as visa

class TriggerStatus:
    def __init__(self, internal_state_register:int) -> None:
        self.ready = bool((internal_state_register & 8192) !=0 )
        self.triggered = bool((internal_state_register & 1) !=0 )
        return

class Oscilloscope:
    def __init__(self, connection_string: str) -> None:
        self.scpi = self.resource_manager.open_resource(connection_string)
        self.scpi.read_termination = '\n'
        self.scpi.write_termination = '\n'
        self.setup()
        
    def write(self, string: str) -> str:
        return self.scpi.write(string)

    def query(self, string: str) -> str:
        return self.scpi.query(string)

    def read(self, string: str) -> str:
        return self.scpi.read(string)
    
    def trigger_status(self) -> dict:
        return TriggerStatus(int(self.scpi.query("INR?")))
    
    def setup(self) -> None:
        self.write("CHDR OFF")
        return