import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE DevelopersのWebhook URLに設定する文字列を取得します
TOKEN = "pyVEnT8mvOP5vxarGh3879qwCpOs5GLXGjzLsw5wkdVIZYLg3B0AIpK8aDFmWWfNKX+vxLOTmzlnf1J3rj76C4nFQRWc0DPKvBY90xJFvO0MsDRfMVqnLhIBasjigqmO9gqhGb+pblkJYonXH82voAdB04t89/1O/w1cDnyilFU="
#input("LineBotのトークンを入力：")
SECRET = "2b242b648b0a9bdea6716f0547665ae6"#input("チャネルシークレットを入力：")
line_bot_api = LineBotApi(TOKEN)
handler = WebhookHandler(SECRET)

# 安全装置（他のボットにこのボットが反応しないようにする）
def is_bot_sender(event):
    sender_id = event.source.user_id
    bot_id = line_bot_api.get_profile(sender_id).user_id

    if sender_id == bot_id:
        return True
    return False

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
    # メッセージ送信者がボットである場合、処理を行わない
    if is_bot_sender(event):
        return

    received_text = event.message.text
    reply_text = received_text

    # イベントのタイプに応じて返信先を設定
    if event.source.type == 'user':
        # 1対1のトーク
        reply_destination = event.source.user_id
    elif event.source.type == 'group':
        # グループチャット
        reply_destination = event.source.group_id
    else:
        return

    line_bot_api.reply_message(
        event.reply_token,
        # メッセージを送信（直前のメッセージをそのまま送信）
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
