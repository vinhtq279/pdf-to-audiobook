import asyncio
import argparse
import re
import sys
import pdfplumber
import edge_tts
from pathlib import Path

# --- CẤU HÌNH ---
DEFAULT_VOICE = "vi-VN-NamMinhNeural" # Giọng nam trầm, phù hợp đọc sách
# DEFAULT_VOICE = "vi-VN-HoaiMyNeural" # Giọng nữ, nhẹ nhàng

def extract_and_clean_text(pdf_path, start_page=0, end_page=None):
    """
    Trích xuất và làm sạch văn bản từ PDF.
    Sử dụng kỹ thuật CropBox để loại bỏ Header/Footer.
    """
    full_text = []
    
    print(f"[*] Đang phân tích PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        if end_page is None or end_page > total_pages:
            end_page = total_pages
            
        # Loop qua từng trang
        for i in range(start_page, end_page):
            page = pdf.pages[i]
            
            # KỸ THUẬT CROP HEADER/FOOTER (Heuristic)
            # Giả định header chiếm 10% trên và footer chiếm 10% dưới
            # Bạn có thể điều chỉnh tham số này tùy layout sách
            width, height = page.width, page.height
            bbox = (0, height * 0.05, width, height * 0.90) # Crop bỏ 5% trên và 10% dưới
            
            cropped_page = page.within_bbox(bbox)
            text = cropped_page.extract_text()
            
            if text:
                full_text.append(text)
                
            sys.stdout.write(f"\r[-] Đang xử lý trang: {i+1}/{end_page}")
            sys.stdout.flush()

    print("\n[*] Đã trích xuất xong. Đang Normalization văn bản...")
    return normalize_text("\n".join(full_text))

def normalize_text(raw_text):
    """
    Chuẩn hóa văn bản sử dụng Regular Expressions (Regex).
    Đây là bước quan trọng nhất để giọng đọc tự nhiên.
    """
    # 1. Nối các từ bị ngắt dòng (Hyphenation). VD: "kết\nnối" -> "kết nối"
    # Logic: Nếu dòng kết thúc bằng - thì xóa -, nối liền.
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', raw_text)
    
    # 2. Xóa các ký tự xuống dòng không phải kết thúc đoạn văn.
    # Logic: Thay thế newline bằng dấu cách
    text = text.replace('\n', ' ')
    
    # 3. Xóa các khoảng trắng thừa (Double spaces)
    text = re.sub(r'\s+', ' ', text)
    
    # 4. (Optional) Xóa các ký tự rác nếu PDF kém chất lượng
    # text = re.sub(r'[^\w\s.,?!:;\'"()-]', '', text)
    
    return text.strip()

async def generate_audio(text, output_file, voice, rate, volume):
    """
    Gửi request tới Edge TTS service.
    """
    print(f"[*] Đang kết nối tới Edge Neural TTS (Voice: {voice})...")
    
    # Cấu hình rate (tốc độ) và volume
    # Rate: +0% là bình thường, +10% là nhanh hơn
    tts_rate = f"{rate:+d}%" if rate >= 0 else f"{rate:+d}%"
    tts_volume = f"{volume:+d}%" if volume >= 0 else f"{volume:+d}%"
    
    communicate = edge_tts.Communicate(text, voice, rate=tts_rate, volume=tts_volume)
    
    print(f"[*] Đang stream dữ liệu và ghi xuống file: {output_file}")
    await communicate.save(output_file)
    print(f"[+] Hoàn tất! File đã được lưu tại: {Path(output_file).absolute()}")

if __name__ == "__main__":
    # Thiết kế giao diện CLI (tương tự các tool linux sysadmin)
    parser = argparse.ArgumentParser(description="Tool chuyển đổi PDF sang Audiobook sử dụng AI Neural Voice")
    
    parser.add_argument("input_pdf", help="Đường dẫn file PDF đầu vào")
    parser.add_argument("-o", "--output", default="audiobook.mp3", help="Tên file đầu ra (mặc định: audiobook.mp3)")
    parser.add_argument("--start", type=int, default=1, help="Trang bắt đầu (mặc định: 1)")
    parser.add_argument("--end", type=int, default=None, help="Trang kết thúc (mặc định: Hết sách)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Mã giọng đọc (mặc định: {DEFAULT_VOICE})")
    parser.add_argument("--rate", type=int, default=0, help="Tốc độ đọc (+/- phần trăm, VD: 10 là nhanh hơn 10%)")

    args = parser.parse_args()

    # Điều chỉnh index trang (vì lập trình đếm từ 0, người dùng đếm từ 1)
    try:
        clean_content = extract_and_clean_text(args.input_pdf, args.start - 1, args.end)
        
        if not clean_content:
            print("[!] Lỗi: Không trích xuất được nội dung văn bản. PDF có thể là dạng ảnh (Scanned PDF).")
            sys.exit(1)
            
        asyncio.run(generate_audio(clean_content, args.output, args.voice, args.rate, 0))
        
    except FileNotFoundError:
        print("[!] Lỗi: Không tìm thấy file PDF.")
    except Exception as e:
        print(f"[!] Đã xảy ra lỗi không mong muốn: {e}")
