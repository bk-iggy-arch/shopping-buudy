import streamlit as st
import os
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込みを実行
load_dotenv()

# APIキーの設定
api_key_value = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key_value)

# 【AI解析関数】うちなーぐちで商品と予算を判定する
def analyze_item_with_ai_okinawa(image_data_input, current_budget_amount):
    generative_model_instance = genai.GenerativeModel('models/gemini-2.5-flash')
    
    ai_instruction_prompt = f"""
    あなたは沖縄の子供向けのお買い物支援バディです。
    買い物予算は {current_budget_amount} 円です。
    1. 商品名 2. 値段 3. 支払いの提案と予算相談 を、
    親しみやすい「うちなーぐち」で答えてね。
    予算オーバーなら「こわいさー！😱💦」とユーモアを交えて相談して。
    """
    
    ai_analysis_response = generative_model_instance.generate_content([ai_instruction_prompt, image_data_input])
    return ai_analysis_response.text

# アプリのタイトル
st.title("🌺 AIお買い物バディ")

# 予算入力
budget_input_value = st.number_input("今日の予算はいくらねー？ (円)", min_value=0, value=3000, step=100)

# --- 💡 ここからが「わかりやすさ」の改良ポイント ---

# 1. 英語の表記を隠して、日本語で案内するための「見た目」を作る（CSS）
st.markdown("""
    <style>
    /* 標準の「Browse files」ボタンや英語テキストを目立たなくし、独自の案内を強調する */
    .stFileUploader section {
        background-color: #fff9e6; /* 優しい黄色 */
        border: 2px dashed #ffb300; /* オレンジの点線 */
        border-radius: 15px;
    }
    .stFileUploader label {
        display: none; /* 標準のラベルを隠す */
    }
    /* 自作の案内メッセージのスタイル */
    .guide-text {
        color: #d32f2f; /* 目立つ赤色 */
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        padding: 10px;
        background-color: #ffeb3b; /* 注意を引く黄色 */
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    <div class="guide-text">👇 ここを押して、写真を撮ってね！</div>
    """, unsafe_allow_html=True)

# 2. ファイルアップロード（中身はそのまま、見た目だけCSSで装飾される）
uploaded_image_data = st.file_uploader("写真を選んでね", type=["jpg", "jpeg", "png"])

# --- 処理ロジック ---
if uploaded_image_data:
    st.write("📸 画像を見てるさぁ。ちょっと待っててね...")
    opened_image_object = PIL.Image.open(uploaded_image_data)
    st.image(opened_image_object, caption="選んだ画像", use_container_width=True)
    
    final_okinawa_answer = analyze_item_with_ai_okinawa(opened_image_object, budget_input_value)
    
    st.success("✨ わかったさぁ！")
    st.write(final_okinawa_answer)
