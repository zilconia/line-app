import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE DevelopersのWebhook URLに設定する文字列を取得します
YOUR_CHANNEL_ACCESS_TOKEN = "pyVEnT8mvOP5vxarGh3879qwCpOs5GLXGjzLsw5wkdVIZYLg3B0AIpK8aDFmWWfNKX+vxLOTmzlnf1J3rj76C4nFQRWc0DPKvBY90xJFvO0MsDRfMVqnLhIBasjigqmO9gqhGb+pblkJYonXH82voAdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "2b242b648b0a9bdea6716f0547665ae6"
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# Webhookからのリクエストを受信するためのエンドポイントを作成します
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# MessageEventの場合の処理を実行する関数を定義します
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
