from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage
import os

app = Flask(__name__)

# 正しく環境変数名で取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# デバッグ用ログ出力（あとで消してOK）
print("DEBUG TOKEN:", LINE_CHANNEL_ACCESS_TOKEN)
print("DEBUG SECRET:", LINE_CHANNEL_SECRET)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    os.makedirs("tmp", exist_ok=True)
    with open(f'tmp/{message_id}.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="動物の写真を受け取りました！感情解析はこれから✨")
    )

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    # 追加：ボディ確認（ログ用）
    print("Request body:", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Signature Error")
        abort(400)

    return 'OK'
