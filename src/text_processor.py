# src/text_processor.py
import re
import sys
import pdfplumber

def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    """
    Trích xuất văn bản thô từ PDF và loại bỏ header/footer.
    """
    full_text = []
    print(f"[*] Đang phân tích PDF (Layout Analysis): {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            if end_page is None or end_page > total_pages:
                end_page = total_pages
            
            # Validation logic
            if start_page < 0 or start_page >= total_pages:
                raise ValueError("Trang bắt đầu không hợp lệ.")

            for i in range(start_page, end_page):
                page = pdf.pages[i]
                
                # Heuristic: Crop 5% top và 10% bottom
                width, height = page.width, page.height
                bbox = (0, height * 0.05, width, height * 0.90)
                
                cropped_page = page.within_bbox(bbox)
                text = cropped_page.extract_text()
                
                if text:
                    full_text.append(text)
                
                # Feedback visual trên CLI
                sys.stdout.write(f"\r[-] Processing page: {i+1}/{end_page}")
                sys.stdout.flush()
                
    except Exception as e:
        print(f"\n[!] Lỗi khi đọc PDF: {e}")
        return None

    print("\n[*] Hoàn tất trích xuất. Đang chuẩn hóa dữ liệu...")
    return normalize_text("\n".join(full_text))

def normalize_text(raw_text):
    """
    Làm sạch văn bản dùng RegEx để tối ưu cho TTS.
    """
    if not raw_text: return ""
    
    # 1. Hàn gắn từ bị ngắt dòng (Hyphenation restoration)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', raw_text)
    
    # 2. Xóa newline giữa câu (Sentence reconstruction)
    text = text.replace('\n', ' ')
    
    # 3. Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
