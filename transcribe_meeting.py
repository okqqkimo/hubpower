#!/usr/bin/env python3
"""
會議錄音轉逐字稿工具
使用 OpenAI Whisper 進行語音辨識，輸出帶時間戳記的逐字稿。

使用方式:
  1. pip install openai-whisper
  2. python transcribe_meeting.py <音訊檔案路徑>

輸出: transcript_output.txt（帶時間戳記的逐字稿，已去贅詞）

請將 transcript_output.txt 的內容貼回 Claude 進行人物分類與會議紀錄。
"""

import re
import sys

import whisper


FILLER_WORDS = [
    "嗯", "啊", "呃", "欸", "喔", "哦", "那個", "就是說", "就是",
    "然後呢", "對對對", "對對", "對啊", "是啊", "好啊",
    "怎麼說呢", "你知道嗎", "我跟你說", "基本上",
]


def format_time(seconds):
    total_seconds = int(seconds)
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def remove_fillers(text):
    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        text = text.replace(filler, "")
    text = re.sub(r"[，、]{2,}", "，", text)
    text = re.sub(r"^[，、。]+|[，、]+$", "", text)
    return text.strip()


def transcribe(audio_path, model_name="medium"):
    print(f"載入模型 {model_name}（首次使用會自動下載）...")
    model = whisper.load_model(model_name)

    print(f"開始轉錄: {audio_path}")
    result = model.transcribe(audio_path, language="zh", verbose=False)

    output_lines = []
    for seg in result["segments"]:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        raw_text = seg["text"].strip()
        cleaned = remove_fillers(raw_text)
        if cleaned:
            output_lines.append(f"[{start}-{end}] {cleaned}")

    output = "\n".join(output_lines)

    output_file = "transcript_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n轉錄完成！已儲存至 {output_file}")
    print(f"共 {len(output_lines)} 個段落")
    print("\n--- 完整內容 ---")
    print(output)
    print("\n請將以上內容（或 transcript_output.txt 檔案內容）貼回 Claude")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe_meeting.py <音訊檔案路徑> [模型名稱]")
        print("模型: tiny, base, small, medium (預設), large")
        print("中文建議使用 medium 或 large")
        sys.exit(1)

    audio_path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "medium"
    transcribe(audio_path, model_name)
