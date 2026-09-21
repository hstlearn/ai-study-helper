# ============================================================
# core.py
# 핵심 비즈니스 로직.
# ============================================================

import os
import time
import tempfile
import datetime
from PIL import Image
from google import genai
from google.genai import types

from prompts import DEFAULT_PROMPT

# ========== 모델 풀 ==========
MODEL_POOL = [
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-3.5-flash-lite',
    'gemini-3.1-flash-lite'
]

# ========== 데모 모드 일일 한도 ==========
DAILY_LIMIT = 50
_daily_count = {"date": None, "count": 0}

def _check_and_increment_demo():
    today = datetime.date.today().isoformat()
    if _daily_count["date"] != today:
        _daily_count["date"] = today
        _daily_count["count"] = 0
    if _daily_count["count"] >= DAILY_LIMIT:
        return False
    _daily_count["count"] += 1
    return True

# ========== 핵심 처리 함수 ==========
def process_images(api_key, custom_prompt, uploaded_files, output_name, output_language="한국어"):
    using_demo = not (api_key and api_key.strip())
    effective_key = api_key.strip() if not using_demo else os.getenv("DEMO_API_KEY")

    if using_demo and not _check_and_increment_demo():
        return "❌ 오늘의 데모 체험 횟수가 모두 소진되었습니다. 개인 API 키를 입력해주세요.", None, None

    if not effective_key:
        return "❌ API 키가 없습니다. 관리자에게 문의하세요.", None, None
    if not uploaded_files:
        return "❌ 이미지를 업로드해주세요.", None, None

    log_text = f"🚀 {len(uploaded_files)}장의 이미지를 받았습니다.\n"
    client = genai.Client(api_key=effective_key)

    base_prompt = custom_prompt if custom_prompt.strip() else DEFAULT_PROMPT
    final_prompt = f"【중요】최종 출력은 반드시 【{output_language}】로 작성하세요.\n\n{base_prompt}"

    markdown_content = "# 한국 자산운용사 대비 학습 노트\n\n---\n\n"

    for idx, file_obj in enumerate(uploaded_files, start=1):
        filename = os.path.basename(file_obj.name)
        log_text += f"📸 [{idx}/{len(uploaded_files)}] {filename} ... "
        success = False
        for model_name in MODEL_POOL:
            try:
                img = Image.open(file_obj.name)
                response = client.models.generate_content(
                    model=model_name,
                    contents=[img, final_prompt],
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                markdown_content += f"## 📝 {filename}\n\n{response.text}\n\n---\n\n"
                log_text += f"✅ ({model_name})\n"
                success = True
                break
            except Exception as e:
                # ★ 完整显示报错，不截断
                log_text += f"❌ [{model_name}] {type(e).__name__}: {str(e)}\n"
                print(f"===== 模型 {model_name} 报错 =====")
                print(f"类型: {type(e).__name__}")
                print(f"详情: {e}")
                break
        if not success:
            log_text += "❌ 모든 모델 실패\n"
            markdown_content += f"## 📝 {filename}\n\n❌ 처리 실패\n\n---\n\n"
        time.sleep(0.3)

    log_text += f"\n🎉 모든 처리 완료 (출력 언어: {output_language})"

    base = output_name.strip() if output_name.strip() else "output"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8', prefix=f"{base}_") as tmp:
        tmp.write(markdown_content)
        tmp_path = tmp.name

    return log_text, markdown_content,tmp_path