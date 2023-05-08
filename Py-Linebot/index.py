import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE DevelopersのWebhook URLに設定する文字列を取得します
TOKEN = input("LineBotのトークンを入力：")
SECRET = input("チャネルシークレットを入力：")
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
    # 送信元のメッセージに返信する機能
    line_bot_api.reply_message(
        event.reply_token,
        # メッセージを送信（直前のメッセージをそのまま送信）
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
