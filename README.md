# PDF to Audiobook Converter (Neural Voice)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Build Status](https://img.shields.io/github/actions/workflow/status/USERNAME/pdf-to-audiobook/ci.yml?branch=main)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker Image Size](https://img.shields.io/badge/docker%20image-slim-blue)

## ������ Tổng quan (Overview)

**PDF to Audiobook Converter** là một công cụ dòng lệnh (CLI Tool) được thiết kế để tự động hóa quy trình chuyển đổi tài liệu PDF phi cấu trúc thành sách nói (Audiobook) chất lượng cao.

Dự án sử dụng sức mạnh của **Microsoft Edge Neural TTS** (thông qua giao thức WebSocket) để tạo ra giọng đọc tự nhiên, có ngữ điệu (prosody) và cảm xúc, vượt trội so với các giải pháp Offline truyền thống.

### Tính năng chính (Key Features)
* **Neural Speech Synthesis:** Sử dụng engine AI mới nhất của Microsoft (hỗ trợ Tiếng Việt: Nam Minh, Hoài My và đa ngôn ngữ).
* **Intelligent Text Normalization:** Thuật toán tiền xử lý thông minh giúp hàn gắn các từ bị ngắt dòng (hyphenation), loại bỏ Header/Footer tự động dựa trên tọa độ (CropBox).
* **Zero-Cost:** Không cần API Key, không giới hạn ký tự (theo cơ chế streaming).
* **Containerized:** Hỗ trợ Docker để triển khai nhanh trên mọi môi trường (Linux/Windows/MacOS).

---

## ������ Kiến trúc (Architecture)

Dự án được thiết kế theo mô hình **Modular**, tuân thủ nguyên lý *Separation of Concerns (SoC)*:

```text
pdf-to-audiobook/
├── src/
│   ├── main.py            # Orchestrator & CLI Interface
│   ├── text_processor.py  # PDF Extraction & Regex Normalization
│   └── tts_engine.py      # Async Edge TTS Client
├── tests/                 # Unit Testing (Pytest)
├── .github/workflows/     # CI Pipeline (Linting & Testing)
├── Dockerfile             # Container definition
└── requirements.txt       # Dependencies
