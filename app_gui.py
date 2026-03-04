import streamlit as st
import os
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込みを実行する処理
load_dotenv()

# .envファイルから取得したGeminiのAPIキー
api_key_value = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key_value)

# 【関数の機能：前】この関数は、撮影された画像と設定予算を受け取り、Gemini AIに渡して沖縄の言葉（うちなーぐち）で商品名、価格、支払いの提案（予算超過の相談含む）を生成させる機能を持つ。
def analyze_item_with_ai_okinawa(image_data_input, current_budget_amount):
    # 【関数の機能：後】生成されたAIからの応答からテキスト部分だけを抽出し、呼び出し元の画面処理へ返す役割を担う。
    
    # 安定して動作するGeminiの生成モデルのインスタンス
    generative_model_instance = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # AIの性格や出力形式（うちなーぐち・ユーモア・予算判定）を細かく指定した命令文
    ai_instruction_prompt = f"""
    あなたは沖縄の子供向けのお買い物支援バディです。画像から情報を抜き出し、以下の形式で回答してください。
    なお、今回の買い物予算は {current_budget_amount} 円です。
    
    1. 商品名: (赤い背景の「特売」などは無視し、具体的な型番や固有名詞を特定してください)
    2. 値段: (税込み価格を数値のみ)
    3. 支払いの提案と予算相談: 
       - 値段が予算({current_budget_amount}円)以下の場合は、お釣りが少なくなる最もスマートな出し方（お札と小銭の組み合わせ）を提案して。
       - 【重要】もし値段が予算({current_budget_amount}円)を超えている場合は、「だからよー、こんな高いの、こわいさー！😱💦 予算オーバーしてるさぁ。これを買うか、カゴの中の他のものをやめるか、どうするね？」と、ユーモアと共感を交えて優しく相談を持ちかけて。
    
    ※沖縄の子供が使うので、親しみやすい「うちなーぐち（沖縄方言）」で答えてね。「はいさい！」「〜さぁ」「〜だはずよ」なども自然に使って。
    """
    
    # 画像とプロンプトをAIに渡して得られた解析結果のオブジェクト
    ai_analysis_response = generative_model_instance.generate_content([ai_instruction_prompt, image_data_input])
    
    # 解析結果のオブジェクトから取り出した最終的なテキストデータ
    final_text_answer = ai_analysis_response.text
    
    return final_text_answer

# 画面のトップに表示されるアプリのタイトル文字列
app_title_text = "🌺 AIお買い物バディ"
st.title(app_title_text)

# ユーザーが画面上で入力する予算金額（初期値3000円）
budget_input_value = st.number_input("今日の予算はいくらねー？ (円)", min_value=0, value=3000, step=100)

# スマホやPCのカメラで撮影され、一時保存された画像データ
captured_image_data = st.camera_input("商品の値札を撮ってね！")

# カメラで画像が撮影された場合のみ実行される処理ブロック
if captured_image_data:
    # ユーザーを待たせている間に表示するメッセージ文字列
    processing_message = "📸 画像を見てるさぁ。ちょっと待っててね..."
    st.write(processing_message)
    
    # PILライブラリを使用してメモリ上に展開された画像オブジェクト
    opened_image_object = PIL.Image.open(captured_image_data)
    
    # AI関数を実行して得られた、うちなーぐちの回答テキスト
    final_okinawa_answer = analyze_item_with_ai_okinawa(opened_image_object, budget_input_value)
    
    # 処理が正常に完了したことを知らせる成功メッセージ文字列
    success_message = "✨ わかったさぁ！"
    st.success(success_message)
    
    # 最終的なAIからの回答を画面に表示する処理
    st.write(final_okinawa_answer)
