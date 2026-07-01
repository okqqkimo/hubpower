#!/usr/bin/env python3
"""
會議錄音轉逐字稿工具
使用 OpenAI Whisper 進行語音辨識，輸出帶時間戳記的逐字稿。

使用方式:
  1. pip install openai-whisper
  2. python transcribe_meeting.py <音訊檔案路徑>

輸出: transcript_output.txt（帶時間戳記的逐字稿）
"""

import sys
import whisper
from datetime import timedelta


def format_time(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def transcribe(audio_path, model_name="medium"):
    print(f"載入模型 {model_name}...")
    model = whisper.load_model(model_name)

    print(f"開始轉錄: {audio_path}")
    result = model.transcribe(audio_path, language="zh", verbose=False)

    output_lines = []
    for seg in result["segments"]:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = seg["text"].strip()
        output_lines.append(f"[{start}-{end}] {text}")

    output = "\n".join(output_lines)

    output_file = "transcript_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n轉錄完成！已儲存至 {output_file}")
    print(f"共 {len(result['segments'])} 個段落")
    print("\n--- 預覽 ---")
    print("\n".join(output_lines[:20]))
    if len(output_lines) > 20:
        print(f"\n... 還有 {len(output_lines) - 20} 個段落，請查看 {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe_meeting.py <音訊檔案路徑> [模型名稱]")
        print("模型: tiny, base, small, medium (預設), large")
        print("中文建議使用 medium 或 large")
        sys.exit(1)

    audio_path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "medium"
    transcribe(audio_path, model_name)
