import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. 環境変数の読み込み
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ エラー: .envファイルに GEMINI_API_KEY が見つかりません。")
else:
    genai.configure(api_key=api_key)
    print("📡 利用可能なモデルを探索中...")
    
    try:
        # サーバーから利用可能なモデルの一覧を取得
        models = [m.name for m in genai.list_models() 
                 if 'generateContent' in m.supported_generation_methods]
        
        if not models:
            print("❌ エラー: 生成モデルが見つかりません。APIキーの権限を確認してください。")
        else:
            print(f"✅ 発見したモデル: {models}")
            
            # リストの先頭にあるモデルでテスト実行
            target = models[0]
            print(f"🚀 モデル '{target}' で接続テストを開始します...")
            
            model = genai.GenerativeModel(target)
            response = model.generate_content("通信テスト成功。短く挨拶して。")
            
            print("\n✨ 運命の瞬間：通信成功！")
            print(f"AIの応答: {response.text}")
            print(f"💡 今後の開発には、モデル名 '{target}' を使用します。")

    except Exception as e:
        print(f"\n❌ 致命的なエラーが発生しました:\n{e}")
