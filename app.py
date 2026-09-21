# ============================================================
# app.py
# 界面层 + 程序入口。
# 在 VSCode 里直接运行这个文件。
# ============================================================



import gradio as gr
from core import process_images

# ★ 让 Gradio 把当前目录当作静态资源目录，hero.png 才能被读取
gr.set_static_paths(paths=["."])

# ========== 自定义 CSS（毛玻璃 + 暗色科技风） ==========
CUSTOM_CSS = """
<style>
    /* 全局背景 */
    .gradio-container {
        background: radial-gradient(ellipse at top, #0a0a1a, #0d0d20) !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        min-height: 100vh !important;
    }   


    /* 隐藏 Home 标签页上面那条多余的横线 */
    .gradio-container hr {
        display: none !important;
    }


    /* 主卡片 - 毛玻璃效果 */
    .main-panel {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6) !important;
        margin: 20px !important;
    }
    /* 标题 */
    .title-main {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 4px !important;
    }
    .title-sub {
        color: #b0c4de !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        border-left: 3px solid #4f46e5 !important;
        padding-left: 14px !important;
        margin-top: 0 !important;
    }
    /* 输入框 */
    .input-field {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        color: #e0e0e0 !important;
        font-size: 0.95rem !important;
        transition: border 0.2s !important;
    }
    .input-field:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
    }
    /* 按钮 */
    .primary-btn {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35) !important;
        transition: transform 0.15s, box-shadow 0.2s !important;
        width: 100% !important;
    }
    .primary-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5) !important;
    }
    /* 日志区 - 暗色终端风格 */
    .log-box {
        background: rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 0.82rem !important;
        color: #b0c4de !important;
        max-height: 400px !important;
        overflow-y: auto !important;
    }
    /* 隐藏 Gradio 水印 */
    footer {
        display: none !important;
    }
    /* 首页专用样式 */
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px 20px;
    }
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -1px !important;
        margin-bottom: 16px !important;
        line-height: 1.2 !important;
    }
    .hero-subtitle {
        color: #b0c4de !important;
        font-size: 1.2rem !important;
        font-weight: 400 !important;
        max-width: 700px !important;
        margin: 0 auto 40px auto !important;
        line-height: 1.6 !important;
    }
    .hero-image {
        max-width: 500px !important;
        width: 60% !important;
        margin: 0 auto !important;
        border-radius: 24px !important;
        box-shadow: 0 30px 80px rgba(124, 58, 237, 0.35) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        display: block !important;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        max-width: 1000px;
        margin: 60px auto 40px auto;
        padding: 0 20px;
    }
    .feature-card {
        background: rgba(255,255,255,0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        text-align: left !important;
        transition: transform 0.2s, border-color 0.2s !important;
    }
    .feature-card:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(124, 58, 237, 0.5) !important;
    }
    .feature-icon {
        font-size: 2rem !important;
        margin-bottom: 12px !important;
    }
    .feature-title {
        color: #e0e0e0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    .feature-desc {
        color: #b0c4de !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }
</style>
"""

# ============================================================
# 页面一：首页 (Home)
# ============================================================
with gr.Blocks(
    title="AI 학습 도우미",
    theme=gr.themes.Soft(),
    analytics_enabled=False,
    css=CUSTOM_CSS,
    fill_width=True
) as demo:

    gr.HTML("""
    <div class="hero-section">
        <div class="hero-title">AI 학습 도우미</div>
        <div class="hero-subtitle">
            이미지 한 장으로 끝내는 한국 자격증 공부.<br>
            번역, 해설, 핵심 정리를 AI가 한 번에.
        </div>
        <img class="hero-image" src="/gradio_api/file=hero.png" alt="AI Learning Workspace">
    </div>
    """)

    gr.HTML("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <div class="feature-title">이미지 일괄 처리</div>
            <div class="feature-desc">여러 장의 교재/기출 문제 스크린샷을 한 번에 업로드하고 처리하세요.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">다국어 번역 & 해설</div>
            <div class="feature-desc">한국어, 중국어, 영어 등 10개 언어로 번역과 함께 상세 해설을 제공합니다.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Markdown 노트 출력</div>
            <div class="feature-desc">번역 + 해설 결과를 깔끔한 Markdown 파일로 다운로드하세요.</div>
        </div>
    </div>
    """)

# ============================================================
# 页面二：翻译工具 (Translator)
# ============================================================
with demo.route("번역 도구", "/translator"):

    gr.HTML("""
    <div style="text-align: left; margin-bottom: 24px;">
        <div class="title-main"> AI 학습 도우미</div>
        <div class="title-sub">AI 이미지 번역 및 해설기</div>
    </div>
    """)

    with gr.Row(elem_classes="main-panel"):
        # ===== 左列：配置区 =====
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ 설정")
            gr.Markdown("#### 처리 설정")

            api_key_input = gr.Textbox(
                label="Gemini API Key (선택 사항)",
                placeholder="비워두시면 데모 모드로 체험하실 수 있습니다",
                type="password",
                elem_classes="input-field"
            )
            gr.Markdown("<span style='color:#8a9ab0;font-size:0.8rem;'>✅ 비워두시면 데모 모드로 바로 체험 가능합니다 (하루 50회 한정). 개인 키를 입력하시면 무제한 사용 가능합니다.</span>")

            language_input = gr.Dropdown(
                choices=["한국어", "中文", "English", "日本語", "Français", "Deutsch", "Español", "Italiano", "Português", "Русский"],
                value="한국어",
                label="출력 언어"
            )

            prompt_input = gr.Textbox(
                label="사용자 지정 프롬프트 (선택 사항)",
                placeholder="예: 이미지의 텍스트를 번역하고 자세히 설명해 주세요...",
                lines=3,
                elem_classes="input-field"
            )

            with gr.Row():
                name_input = gr.Textbox(
                    label="출력 파일 이름",
                    placeholder="my_notes",
                    lines=1,
                    elem_classes="input-field",
                    scale=2
                )
                gr.Markdown("<span style='color:#8a9ab0;font-size:0.8rem;padding-top:24px;'>.md</span>", scale=1)

            file_input = gr.File(
                label="이미지 선택 (다중 선택 가능)",
                file_count="multiple",
                file_types=[".jpg", ".jpeg", ".png", ".webp"],
                elem_classes="input-field"
            )

            gr.Examples(
                examples=[
                    ["examples/01.jpg"],
                    ["examples/02.jpg"]
                ],
                inputs=[file_input],
                label="📌 예시 이미지로 체험하기"
            )

            process_btn = gr.Button("🚀 처리 시작", variant="primary", elem_classes="primary-btn")

        # ===== 右列：日志 + 输出 =====
        with gr.Column(scale=1):
            gr.Markdown("### 📋 ACTIVITY STREAM")
            gr.Markdown("#### 처리 로그")

            output_log = gr.Textbox(
                label="",
                lines=12,
                interactive=False,
                elem_classes="log-box",
                placeholder="처리 로그가 여기에 표시됩니다.\n\n이미지를 선택한 후 '처리 시작'을 클릭하세요."
            )

            output_md = gr.Markdown(
                label="",
                value="결과 대기 중..."
            )

            output_file = gr.File(
                label="📥 Markdown 파일 다운로드",
                interactive=False
            )

            gr.Markdown(
                """
                <div style='color:#6b7a8f;font-size:0.75rem;margin-top:12px;border-top:1px solid rgba(255,255,255,0.05);padding-top:12px;'>
                ⚡ 단일 이미지 처리 실패 시 대기열이 중단되지 않습니다<br>
                🔒 이미지는 Gemini API로만 전송되며 저장되지 않습니다
                </div>
                """
            )

    # 绑定按钮
    process_btn.click(
        fn=process_images,
        inputs=[api_key_input, prompt_input, file_input, name_input, language_input],
        outputs=[output_log, output_md, output_file]
    )

if __name__ == "__main__":
    demo.launch()