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
import GPT,Rinna
# LineAPI の値をAPI_key.pyからインポート
from API_key import Token, Secret

# 
app = Flask(__name__)

# 安全装置（他のボットにこのボットが反応しないようにする）
def is_bot_sender(event):
    sender_id = event.source.user_id
    bot_id = line_bot_api.get_profile(sender_id).user_id
    if sender_id == bot_id:
        return True
    return False

# 入力内容の記録用
def json_memo(userId,memo):
    # ファイルネーム
    fp="Line_log.json"
    if not(os.path.exists(fp)):
        with open(fp,"w",encoding="utf-8") as f:
            json.dump({},f,ensure_ascii = False,indent=4)
            f.truncate()
    with open(fp,"r+",encoding="utf-8") as f:
        f.seek(0)
        data = json.load(f)
        data[str(len(data))]={"UserID":userId,"message":memo}
        f.seek(0)
        json.dump(data,f,ensure_ascii = False,indent=4)
        f.truncate()
        # デバッグ表示
        # pprint(data,width=40)

# LINE DevelopersのWebhook URLに設定する文字列を取得します
TOKEN = Token
SECRET = Secret
line_bot_api = LineBotApi(TOKEN)
handler = WebhookHandler(SECRET)

# Webhookからのリクエストを受信するためのエンドポイントを作成します
@app.route("/callback", methods=["POST"])
def callback():
    # リクエストの署名確認
    signature = request.headers["X-Line-Signature"]
    # Lineアプリ側のメッセージを取得（str型として取得）
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    # リクエストによるアプリの動作結果を返す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# MessageEventの場合の処理を実行する関数を定義します
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    """
    # イベントのタイプに応じて返信先を設定
    if event.source.type == 'user':
        # 1対1のトーク
        reply_destination = event.source.user_id
    elif event.source.type == 'group':
        # グループチャット
        reply_destination = event.source.group_id
    else:
        return
    """
    # コンソールへの出力（確認用）
    print(f"トークType：{event.source.type}")
    print(f"ユーザーID：{event.source.user_id}")
    print(f"Message：{event.message.text}")
    if event.source.type == 'group':
        print(f"\nルームID：{event.source.group_id}\n")
    
    json_memo(event.source.user_id,event.message.text)

    
    line_bot_api.reply_message(
        event.reply_token,
        # メッセージを送信（直前のメッセージをそのまま送信）
        TextSendMessage(text=event.message.text)# input("返信内容を入力")
    )
    
    """# ChatGPT による返信機能
    level,message = GPT.main(event.message.text)
    #message=event.message.text
    print(f"\n危険度：{level}\n返信内容：{message}\n")
    # プッシュ通知をする機能
    if message != None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))
        )
    """
    """# Rinna による返信機能
    message = Rinna.main(event.message.text)
    print(f"\n返信内容：{message}\n")
    # プッシュ通知をする機能
    if message != None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))
        )
    """

# index.py 自体を起動したら実行される。
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
