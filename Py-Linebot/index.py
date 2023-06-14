# -*- coding: utf-8 -*-
# ライブラリのインポート
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
from pprint import pprint

# GPT.py (Rinna.py) をインポート
import GPT_35 as GPT
# import Rinna
# LineAPI の値をAPI_key.pyからインポート
from API_key import Token, Secret

# Flask のセットアップ
app = Flask(__name__)

# LINE DevelopersのWebhook URLに設定する文字列を取得します
line_bot_api = LineBotApi(Token)
handler = WebhookHandler(Secret)

# 安全装置（他のボットにこのボットが反応しないようにする）
def is_bot_sender(event):
    sender_id = event.source.user_id
    bot_id = line_bot_api.get_profile(sender_id).user_id
    if sender_id == bot_id:
        return True
    return False

# 入力しているユーザーの新規登録
def Log_User(userid):
    file="Line_User.json" # ファイルネーム
    if not(os.path.exists(file)): # 上記ファイルがなかった時の新規作成機能
        with open(file,"w",encoding="utf-8") as f:
            json.dump({},f,ensure_ascii = False,indent=4)
            f.truncate()
    with open(file,"r+",encoding="utf-8") as f: # ファイルに入力内容をを保存する一連の流れ
        f.seek(0)
        data = json.load(f)
        if not(userid in data): # 新規ユーザーが初めて入力した場合に登録する
            data[userid]=chr(ord("a")+len(data)) # "a"の「Unicode コードポイント(int型)」を取得し、dataの配列サイズ分の数値を追加して文字に変換する。
            f.seek(0)
            json.dump(data,f,ensure_ascii = False,indent=4)
            f.truncate()
        return data[userid] # IDに応じたタグの出力

# 入力内容の記録用
def Log_Message(userid,memo):
    # ファイルネーム
    file="Line_log.json"
    # 上記ファイルがなかった時の新規作成機能
    if not(os.path.exists(file)):
        with open(file,"w",encoding="utf-8") as f:
            json.dump({},f,ensure_ascii = False,indent=4)
            f.truncate()
    # ファイルに入力内容をを保存する一連の流れ
    with open(file,"r+",encoding="utf-8") as f:
        f.seek(0)
        data = json.load(f)
        data[str(len(data))]={
            "UserID":userid,
            "message":memo
        }
        if len(data)>100:
            for i in range(100):
                data[f"{i}"]=data.pop(f"{i+1}")
        f.seek(0)
        json.dump(data,f,ensure_ascii = False,indent=4)
        f.truncate()
        # 入力内容の最新5件をreturnで出力する
        m=[]
        for i in range(5):
            m.insert(0,data[f"{len(data)-1-i}"])
            if (len(data))==i+1 and i<=5:
                break
        return m

        # デバッグ表示
        # pprint(data,width=40)
 
# Webhookからのリクエストを受信するためのエンドポイントを作成します
@app.route("/callback", methods=["POST"])
def callback():
    # リクエストの署名確認
    signature = request.headers["X-Line-Signature"]
    # Lineアプリ側のメッセージを取得（str型として取得）
    body = request.get_data(as_text=True)
    # メッセージに対する様々なログが表示される
    # app.logger.info("Request body: " + body)
    # リクエストによるアプリの動作結果を返す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError: # 
        abort(400)
    return "OK"

# 取得したイベントに記載されたユーザーIDを使用してアカウント名を取得する
def Line_name(user_id):
    try:
        # プロフィール情報を取得
        profile = line_bot_api.get_profile(user_id)
        account_name = profile.display_name
        return account_name
    except LineBotApiError as e:
        # エラーハンドリング
        print(e)
        return None

# MessageEventの場合の処理を実行する関数を定義します
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザー情報
    user={
            "name":Line_name(event.source.user_id), # 名前
            "id":event.source.user_id, # ID
            "message":event.message.text # メッセージ
        }
    # メッセージイベントの出力先タイプ（グループ, 個人）
    eve_type=event.source.type

    # コンソールへの出力（確認用）
    print(f"ユーザーネーム：{user['name']}")
    print(f"トークType：{eve_type}")
    print(f"ユーザーID：{user['id']}")
    print(f"Message：{user['message']}")
    if event.source.type == 'group':
        print(f"\nルームID：{event.source.group_id}\n")
    
    # ユーザーのIDとメッセージの保存＋直近のログ5件を出力
    Logs=Log_Message(user["id"],user["message"])
    # Logs のUserIDを短絡的なネームタグ(a,b,c ...)に変換する＋新規ユーザーをネームタグに対応させる。
    for i in range(len(Logs)):
        Logs[i]["UserID"]=Log_User(Logs[i]["UserID"])
        # 入力用の形式に変換する
        Uid, text = Logs[i]["UserID"], Logs[i]["message"]
        Logs[i]=f"{Uid}:{text}"
    
    # # メッセージの返信
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     # メッセージを設定（直前のメッセージをそのまま送信）
    #     TextSendMessage(text=Logs[4])# input("返信内容を入力")
    # )
    
    
    # ChatGPT による返信機能
    message = GPT.main(Logs)
    #print(f"\n危険度：{level}\n返信内容：{message}\n")
    print(f"\n返信内容：{message}\n")
    # プッシュ通知をする機能
    if message != 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    
    """# Rinna による返信機能
    message = Rinna.main(event.message.text)
    print(f"\n返信内容：{message}\n")
    # プッシュ通知をする機能
    if message != None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    """

# index.py 自体を起動したら実行される。
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
