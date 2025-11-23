# src/tts_engine.py
import edge_tts
from pathlib import Path

async def generate_audio(text, output_file, voice, rate_pct=0, volume_pct=0):
    """
    Gửi request tới Edge Neural TTS service.
    Input: text, config parameters.
    Output: Audio file (.mp3)
    """
    print(f"[*] Khởi tạo kết nối tới Edge Cloud (Voice: {voice})...")
    
    # Format tham số theo chuẩn của edge-tts (VD: +10%)
    tts_rate = f"{rate_pct:+d}%"
    tts_volume = f"{volume_pct:+d}%"
    
    try:
        communicate = edge_tts.Communicate(text, voice, rate=tts_rate, volume=tts_volume)
        
        print(f"[*] Đang streaming dữ liệu về: {output_file}")
        await communicate.save(output_file)
        
        abs_path = Path(output_file).absolute()
        print(f"[+] Thành công! File: {abs_path}")
        return True
        
    except Exception as e:
        print(f"[!] Lỗi kết nối API TTS: {e}")
        return False
