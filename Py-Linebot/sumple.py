from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

token="jUoJ1XL6FZNlq/IXD7nuFOymzdqCVCOO+VhEp70csUsFrHxsvTqsjSdTf/l1YwPjKX+vxLOTmzlnf1J3rj76C4nFQRWc0DPKvBY90xJFvO2+3xhWwAng1jrGqBZOx7lmFupp704EvTjKhZWrMQxGDwdB04t89/1O/w1cDnyilFU="
secret="794dd836d5cb9682dc11b6c60896cf7a"

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ[token]
YOUR_CHANNEL_SECRET = os.environ[secret]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)