# can-bus-signal-monitor

## Overview
A Python-based CAN bus signal monitoring and fault detection tool that simulates 
an AUTOSAR-inspired ECU communication layer across 3 virtual ECUs. Signals are 
broadcast at realistic automotive cycle times, monitored for faults in real-time, 
logged to CSV, and visualised on an interactive dashboard.

Built to demonstrate CAN bus communication and signal plausibility checking in an 
open-source environment, complementing hands-on work with dSPACE SystemDesk and 
VEOS at TU Chemnitz.

## Technical Architecture
- **can_nodes.py** — simulates 3 ECUs (wheel speed, brake pressure, accel pedal) 
  broadcasting on a shared virtual CAN bus using threading
- **fault_detector.py** — legacy single-process detector (see can_nodes.py for 
  integrated version)
- **dashboard.py** — Streamlit + Plotly dashboard visualising signal values and 
  fault events in real-time from logged CSV data

## Key Results
- 16,520 CAN signals logged across 3 ECUs in under 2 minutes
- 2,825 fault events detected at a 17.1% fault rate
- 3 fault detection classes: OUT_OF_RANGE, TIMEOUT, IMPLAUSIBILITY
- Signals broadcast at 10–50ms cycle times, matching real AUTOSAR timing specs

## How to Run

### 1. Install dependencies
pip install python-can cantools pandas streamlit plotly pytest

### 2. Generate signal log
python3 can_nodes.py
# Let run for 10–15 seconds, then Ctrl+C

### 3. Launch dashboard
streamlit run dashboard.py

## Relevance to Automotive Software Development
The fault detection logic mirrors signal plausibility checks required under ISO 26262 
runtime monitoring. The multi-ECU threading architecture reflects the parallel 
communication patterns handled by an AUTOSAR Runtime Environment (RTE).

## Future Work
- Inject faults programmatically to simulate real ECU failure scenarios
- Extend to a full DBC file-based signal database using cantools
- Add ASIL-tagged fault severity levels to the detection logic