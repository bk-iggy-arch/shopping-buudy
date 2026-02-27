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
    あなたは中高生向けのお買い物支援バディです。画像から情報を抜き出し、以下の形式で回答してください。
    
    1. 商品名: (赤い背景の「特売」などは無視し、具体的な型番や固有名詞を特定してください)
    2. 値段: (税込み価格を数値のみ)
    3. 支払いの提案: (以下のルールで)
       - 1万円、5千円、千円、500円、100円、50円、10円を組み合わせて、お釣りが少なくなる最もスマートな出し方を提案して。
       - 例: 11,880円なら「1万円札1枚、千円札2枚を出して、お釣りは120円だよ」
    
    ※中高生が使うので、幼稚すぎない丁寧な言葉遣いで。
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
