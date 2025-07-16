from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('2710TnQJpAcQTaRaTt286shJ9CSuyEAN1vZU+nGu1liOEAbXY3mKtjz/lq3VRg3r9lCYbaQ5sdS2v37d0UeSBdqpX+IGMsHRZi20HaNj5FSRfW8PKaoc+8Igh9lcSZ5bBvUV9+37SuoVdVZn10n/tAdB04t89/1O/w1cDnyilFU=)
LINE_CHANNEL_SECRET = os.getenv('ecdf53bb0c7b861ca0707798e67ac63c)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
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

    os.makedirs("tmp", exist_ok=True)  # フォルダがなければ作る
    with open(f'tmp/{message_id}.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="動物の写真を受け取りました！感情解析はこれから✨")
    )

if __name__ == "__main__":
    app.run(debug=True)

import os

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('2710TnQJpAcQTaRaTt286shJ9CSuyEAN1vZU+nGu1liOEAbXY3mKtjz/lq3VRg3r9lCYbaQ5sdS2v37d0UeSBdqpX+IGMsHRZi20HaNj5FSRfW8PKaoc+8Igh9lcSZ5bBvUV9+37SuoVdVZn10n/tAdB04t89/1O/w1cDnyilFU=)
LINE_CHANNEL_SECRET = os.getenv('ecdf53bb0c7b861ca0707798e67ac63c')
