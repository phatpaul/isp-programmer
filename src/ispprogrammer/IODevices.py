import logging
import time
from serial import Serial

kTimeout = 1

_log = logging.getLogger("ispprogrammer")


class IODevice:
    """Generic for a byte IO device"""

    def read_byte(self):
        pass

    def read_all(self):
        pass

    def write(self, arr: bytes):
        pass

    def flush(self):
        pass

    def SetBaudrate(self, baudrate: int) -> None:
        pass

    def GetBaudrate(self):
        pass

    def ReadLine(self):
        pass

    def disconnect(self):
        pass


class MockUart(IODevice):
    """Mock IO device for testing"""

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600):
        self.baudrate = baudrate
        self.port = port

    def disconnect(self):
        pass

    def read_byte(self):
        return 0x00

    def read_all(self):
        return bytes(0x00)

    def SetBaudrate(self, baudrate: int) -> None:
        self.baudrate = baudrate

    def GetBaudrate(self):
        return self.baudrate


class UartDevice(IODevice):
    """Serial IO device wrapper around pyserial"""

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 9600,
        timeout: float = kTimeout,
        isp_entry=False,
    ):
        _log.debug("connect serial")
        # Create the Serial object without port to avoid automatic opening
        self.uart = Serial(port=None, baudrate=baudrate, xonxoff=False, timeout=timeout)

        # Disable RTS and DRT to avoid automatic reset to ISP mode
        self.uart.rts = 0
        self.uart.dtr = 0

        # Select and open the port after RTS and DTR are set to zero
        self.uart.port = port
        self.uart.open()

        if isp_entry:
            self.isp_mode()

        self.flush()

    # put the chip in isp mode by resetting it using RTS and DTR signals
    # this is of course only possible if the signals are connected
    def isp_mode(self):
        self.set_reset_pin_level(0)
        time.sleep(.1)
        self.set_reset_pin_level(1)
        self.set_isp_entry_pin_level(1)
        time.sleep(.1)
        self.set_reset_pin_level(0)
        time.sleep(.1)
        self.set_isp_entry_pin_level(0)

    def set_reset_pin_level(self, level):
        # reset pin is on dtr
        self.uart.dtr = level

    def set_isp_entry_pin_level(self, level):
        # ISP entry pin is on rts
        self.uart.rts = level

    def disconnect(self):
        _log.debug("disconnect serial")
        try:
            self.uart.close()
            del self.uart
        except AttributeError:
            pass

    def __del__(self):
        self.disconnect()

    def read(self, *args, **kwargs):
        return self.uart.read(*args, **kwargs)

    def flush(self, *args, **kwargs):
        return self.uart.flush(*args, **kwargs)

    def read_byte(self, *args, **kwargs):
        return self.uart.read_byte(*args, **kwargs)

    def read_all(self, *args, **kwargs):
        return self.uart.read_all(*args, **kwargs)

    def write(self, arr: bytes):
        assert isinstance(arr, bytes)
        self.uart.write(arr)

    def SetBaudrate(self, baudrate: int) -> None:
        self.uart.baudrate = baudrate

    def GetBaudrate(self) -> int:
        return self.uart.baudrate

    def ReadLine(self):
        line = self.uart.readline()
        try:
            return bytes(line).decode("utf-8")
        except UnicodeDecodeError:
            raise TimeoutError
