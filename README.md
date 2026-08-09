# SubScraper

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight, asynchronous Python engine designed to scrape V2Ray subscription endpoints, extract VLESS/Trojan nodes, validate latency, and export sorted, active configurations with corresponding QR codes.

---

## 📷 QR Code Quick Scans

| Normal TCP Pass | SNI-Spoof Pass |
| :---: | :---: |

<img src=qrcode/tcp_pass_normal.png width="300" alt="TCP Pass Normal QR Code">
<img src=qrcode/tcp_pass_spoof.png width="300" alt="TCP Pass Sni Spoof QR Code">

---

## 📅 Last Updated

**2026-08-09**

---

## 🚀 Key Features

* **Async Pipeline:** Fetches and evaluates multiple subscription feeds simultaneously using `asyncio` and `aiohttp`.
* **Multi-Protocol Extraction:** Parses and normalizes `vless://` and `trojan://` URIs, including Base64-encoded payload handling.
* **Latency Benchmarking:** Performs direct TCP socket and HTTP handshake validation to discard dead nodes and rank active ones by speed.
* **SNI Spoofing Segregation:** Filters and classifies configurations based on standard vs. SNI-spoofed routing paths.
* **Automated QR Generation:** Generates high-contrast QR codes directly into the `qrcode/` directory for instant mobile scanning.
