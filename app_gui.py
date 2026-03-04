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
# --- 💡 視覚的な「白い四角」を強調するデザイン改良 ---

st.markdown("""
    <style>
    /* 1. ファイルアップロードの枠全体を「大きな白い四角」にする */
    .stFileUploader section {
        background-color: #ffffff !important; /* 真っ白にする */
        border: 4px solid #ffb300 !important; /* 太いオレンジの枠線で囲む */
        border-radius: 20px !important;
        padding: 20px !important;
        min-height: 150px !important; /* 高さを出して押しやすくする */
    }

    /* 2. 中にある英語のテキスト（Drag and drop...）を完全に消す */
    .stFileUploader section div div {
        display: none !important;
    }
    .stFileUploader section span {
        display: none !important;
    }

    /* 3. 代わりに、枠の真ん中にデカデカと日本語を表示する */
    .stFileUploader section::before {
        content: "📸 この白い四角を\\A押してね！"; /* \\A は改行コード */
        white-space: pre;
        display: block;
        text-align: center;
        color: #333333;
        font-weight: bold;
        font-size: 24px;
        margin-top: 20px;
    }

    /* 4. 標準の小さなボタン（Browse files）を透明にして、枠のどこを押しても反応するようにする */
    .stFileUploader button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0; /* 透明にする */
        cursor: pointer;
    }
    </style>
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
