
# 🌩️ ESP2Cloud: End-to-End IoT with ESP32 & AWS

A complete Internet of Things (IoT) system that collects real-time sensor data from an ESP32 device using MicroPython, sends it via a TCP socket to a Python gateway on a laptop, and forwards it to AWS IoT Core using MQTT over TLS. The data is stored in **Timestream** and visualized in **Grafana**.

---

## 📦 Features

- 🔌 ESP32 MicroPython TCP Client
- 💻 Python TCP Server on Laptop
- 🔐 MQTT over TLS to AWS IoT Core
- 🗃️ AWS Rule for Timestream integration
- 📊 Real-time dashboards with Grafana
- 🔁 Secure, scalable, and reliable data flow

---

## 🔧 System Architecture

```mermaid
graph LR
    ESP32[ESP32 (Sensor Data)]
    Laptop[Laptop (Python TCP Server)]
    AWS[AWS IoT Core (MQTT over TLS)]
    DB[AWS Timestream (Time-series DB)]
    Grafana[Grafana (Visualization)]

    ESP32 -- TCP Socket --> Laptop
    Laptop -- MQTT + TLS --> AWS
    AWS -- Rule --> DB
    DB -- Query --> Grafana
```

---

## 🚀 Getting Started

### 1. 🧠 Prerequisites

- ESP32 with MicroPython firmware
- Laptop with Python 3.x installed
- AWS IoT Core set up with:
  - IoT Thing, certificate, and policy
  - IoT Rule to forward MQTT data to Timestream
- AWS Timestream database and table
- Grafana (hosted or local setup)

---

### 2. 🧱 Project Structure

```
.
├── esp32_client/                    # MicroPython code for ESP32
│   ├── config.py
│   ├── data_pusher.py              # TCP socket client code
│   ├── input_reader.py
│   ├── main.py
│   ├── sensor.py
│   └── wifi_client.py              # Wi-Fi setup code
├── gateway/                        # Python server & MQTT publisher
│   ├── gateway.py
│   └── mqtt.py
├── cloud/                          # Optional Flask-based MQTT viewer
│   ├── api_server.py
│   ├── server.py
│   └── mqtt.py
├── iotcerts/                       # AWS IoT certificates
│   ├── root-CA.crt
│   ├── device-cert.pem.crt
│   └── private.pem.key
├── ESP32_GENERIC-20250415-v1.25.0.bin
├── Architecture of system.png
├── circuit diagram.png
├── .env                            # Environment variables (not committed)
├── cp.bat                          # Copy files to ESP32
├── flash_esp.bat                   # Flash MicroPython to ESP32
└── README.md
```

---

## 📡 ESP32 Setup

1. Install MicroPython tools:

```bash
pip install esptool
pip install mpremote
```

2. Flash MicroPython to ESP32:

```bash
flash_esp.bat
```

3. Upload project files to ESP32:

```bash
cp.bat
```

4. Run the socket client on ESP32:

```bash
mpremote connect COM5 run esp32_client/main.py
```

> 🔧 Update `HOST`, `PORT`, and Wi-Fi credentials in `config.py`.

---

## 🖥️ Laptop: TCP Server + MQTT Publisher

1. Install Python libraries:

```bash
pip install paho-mqtt
```

2. Run the Python TCP server and MQTT publisher:

```bash
python gateway/gateway.py
```

Make sure to configure:

- Your **AWS IoT endpoint**
- Path to AWS **certificates**
- MQTT **topic**, **QoS**, and **port 8883**

---

## 🖥️ Optional: MQTT Subscriber (Localhost UI)

1. Install Flask dependencies:

```bash
pip install Flask 
pip install Flask-Cors
```

2. Run Flask API server (for debug/testing):

```bash
python cloud/api_server.py
```

---

## 🔐 Security

- ✅ TLS v1.2 encryption between Laptop and AWS IoT Core
- ✅ Amazon Root CA and valid device certificates used
- ✅ ESP32 TCP client is confined to local Wi-Fi network

---

## 📊 Visualization with Grafana

- AWS Timestream stores structured sensor data
- Grafana queries Timestream using SQL-like language
- Dashboards reflect near real-time sensor values

---

## ❌ Challenges Faced

- 📶 ESP32 Wi-Fi instability leading to socket drops
- 🔡 Manual encoding/decoding of JSON via TCP
- 🔐 AWS TLS handshake and certificate mismatches
- 📦 Data formatting issues for Timestream ingestion

---

## 🧠 Future Improvements

- 🔁 Add buffering and retry on ESP32
- 🔄 Enable bi-directional MQTT for remote control
- 🕒 Sync ESP32 time using NTP
- 🍓 Migrate Python server to Raspberry Pi for 24/7 operation

---

## 🛠 Tools & Technologies Used

| Component        | Technology              |
|------------------|--------------------------|
| Device Firmware  | MicroPython              |
| TCP/IP Client    | socket, _thread (ESP32)  |
| TCP Server       | Python socket            |
| MQTT             | Eclipse Paho + TLS       |
| AWS Cloud        | IoT Core + Timestream    |
| Visualization    | Grafana                  |
| Optional UI      | Flask + Flask-Cors       |

---

## 📦 Dependencies

Install all PC-side libraries via `pip`:

```bash
pip install esptool mpremote paho-mqtt Flask Flask-Cors
```

Note: ESP32 libraries like `machine`, `network`, `_thread`, `socket` (MicroPython) do **not** require `pip install`.

---

## 📸 System Diagrams

![System Architecture](Architecture of system.png)

![Circuit Diagram](circuit%20diagram.png)

---
