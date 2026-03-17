import can
import time
import random
import csv
import threading
from datetime import datetime

log = []
running = True

LIMITS = {
    0x100: ("wheel_speed",    0.0, 120.0),
    0x200: ("brake_pressure", 0.0,  80.0),
    0x300: ("accel_pedal",    0.0, 100.0),
}

ecus = [
    (0x100, 60.0, 5.0),
    (0x200,  0.0, 2.0),
    (0x300, 30.0, 3.0),
]

def broadcaster():
    bus = can.interface.Bus(interface='virtual', channel='test')
    print("Broadcaster started...")
    try:
        while running:
            for can_id, base, noise in ecus:
                value = base + random.uniform(-noise, noise)
                data = bytearray(8)
                data[0:4] = int(value * 100).to_bytes(4, byteorder='big', signed=True)
                msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
                bus.send(msg)
            time.sleep(0.01)
    finally:
        bus.shutdown()

def detector():
    bus = can.interface.Bus(interface='virtual', channel='test')
    print("Fault detector started... (Ctrl+C to stop and save log)")
    try:
        while running:
            msg = bus.recv(timeout=0.1)
            if msg is None or msg.arbitration_id not in LIMITS:
                continue

            raw = int.from_bytes(msg.data[0:4], byteorder='big', signed=True)
            value = raw / 100.0
            name, min_val, max_val = LIMITS[msg.arbitration_id]

            fault = None
            if value < min_val or value > max_val:
                fault = "OUT_OF_RANGE"

            entry = {
                "time": datetime.now().isoformat(),
                "ecu": hex(msg.arbitration_id),
                "signal": name,
                "value": round(value, 2),
                "fault": fault if fault else "OK"
            }

            if fault:
                print(f"[FAULT] {entry}")

            log.append(entry)
    finally:
        bus.shutdown()

t1 = threading.Thread(target=broadcaster)
t2 = threading.Thread(target=detector)
t1.start()
t2.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopping...")
    running = False
    t1.join()
    t2.join()
    with open("signal_log.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["time","ecu","signal","value","fault"])
        writer.writeheader()
        writer.writerows(log)
    print(f"Saved {len(log)} entries to signal_log.csv")
