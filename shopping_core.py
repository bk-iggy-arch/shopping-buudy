import os
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# 1. 環境設定
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_shopping_item(image_path):
    # 成功したモデル名を使用
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # 画像の読み込み
    img = PIL.Image.open(image_path)
    
    # 障害児教育の知見を活かしたプロンプト
    prompt = """
    あなたは買い物支援バディです。画像から情報を抜き出し、以下の形式で回答してください。
    
    1. 商品名: (一番目立つ名前)
    2. 値段: (税込み価格を数値のみ)
    3. 出すお金: 100円玉を「●枚」出そうね
    
    ※「出すお金」は、商品の値段をカバーできる最小限の100円玉の枚数を計算してください。
    例：158円なら2枚、98円なら1枚。
    余計な解説は省き、子供がパッと見てわかる言葉だけで答えてください。
    """

    # 解析の実行
    response = model.generate_content([prompt, img])
    return response.text

# 2. 実行テスト
if __name__ == "__main__":
    # ここにテスト用の画像ファイル名を指定してください
    test_image = "sample_tag.jpg" 
    
    if os.path.exists(test_image):
        print(f"📸 画像 '{test_image}' を解析中...")
        result = analyze_shopping_item(test_image)
        print("\n--- 解析結果 ---")
        print(result)
    else:
        print(f"⚠️ エラー: {test_image} が見つかりません。画像をフォルダに置いてください。")
