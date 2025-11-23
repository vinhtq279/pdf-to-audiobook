# src/main.py
import argparse
import asyncio
import sys
import os

# Import modules nội bộ
# Lưu ý: Khi chạy dạng module (-m), python sẽ tự hiểu path
from src.text_processor import extract_text_from_pdf
from src.tts_engine import generate_audio

DEFAULT_VOICE = "vi-VN-NamMinhNeural"

def main():
    # 1. Cấu hình CLI Arguments
    parser = argparse.ArgumentParser(description="Professional PDF to Audiobook Converter")
    
    parser.add_argument("input_pdf", help="Đường dẫn file PDF")
    parser.add_argument("-o", "--output", default="audiobook.mp3", help="File đầu ra")
    parser.add_argument("--start", type=int, default=1, help="Trang bắt đầu")
    parser.add_argument("--end", type=int, default=None, help="Trang kết thúc")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Mã giọng đọc Edge TTS")
    parser.add_argument("--rate", type=int, default=0, help="Tốc độ đọc (+/- %)")

    args = parser.parse_args()

    # 2. Kiểm tra file đầu vào
    if not os.path.exists(args.input_pdf):
        print(f"[!] Lỗi: Không tìm thấy file {args.input_pdf}")
        sys.exit(1)

    # 3. Pipeline xử lý
    # Bước A: Trích xuất & Làm sạch
    clean_content = extract_text_from_pdf(args.input_pdf, args.start - 1, args.end)
    
    if not clean_content:
        print("[!] Không có dữ liệu văn bản để xử lý.")
        sys.exit(1)
        
    # Bước B: Chuyển đổi TTS (Async)
    asyncio.run(generate_audio(
        text=clean_content,
        output_file=args.output,
        voice=args.voice,
        rate_pct=args.rate
    ))

if __name__ == "__main__":
    main()
