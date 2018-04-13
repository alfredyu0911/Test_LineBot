from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('VPE+CQA/7xT/Gw7+AuQglKL7lHNyC+64k30AnkYlU///83YpPvE6vuyrBoU5oxvsCgNU6VMw/WlDBOHYrZnisRoIfP+qPVEBnAgEkDO29/mgM/RUNBwHwMPHLW1XdtVbIlzU6vcSgtfuPwKtuBqvyAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e4013cf04ebc446549c202098e9562a8')

@app.route('/')
def index():
    return "<p>Hello World!</p>"

# 監聽所有來自 /callback 的 Post Request
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
    if event.message.text==u"Hi":
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(u"How are you"))
    else:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(u"i'm sorry that i can't recognize this message"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
