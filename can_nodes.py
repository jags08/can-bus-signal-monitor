import can
import cantools
import time
import random

# Simulate 3 ECUs broadcasting on a virtual CAN bus
bus = can.interface.Bus(interface='virtual', channel='vcan0')

# ECU definitions: (CAN ID, signal name, base value, noise range, cycle time in seconds)
ecus = [
    (0x100, "wheel_speed",     60.0,  5.0,  0.01),   # 10ms cycle
    (0x200, "brake_pressure",   0.0,  2.0,  0.02),   # 20ms cycle
    (0x300, "accel_pedal",     30.0,  3.0,  0.05),   # 50ms cycle
]

print("Virtual CAN bus started. Broadcasting ECU signals... (Ctrl+C to stop)")

try:
    while True:
        for can_id, name, base, noise, cycle in ecus:
            value = base + random.uniform(-noise, noise)
            # Pack value as a float into 8 bytes
            data = bytearray(8)
            data[0:4] = int(value * 100).to_bytes(4, byteorder='big', signed=True)
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            bus.send(msg)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nBus stopped.")
    bus.shutdown()
