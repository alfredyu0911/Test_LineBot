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

subscription_key = "f9cbd50a4b6e4696addd5c589279362c"
assert subscription_key
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://how-old.net/Images/faces2/main007.jpg'

import requests
from IPython.display import HTML

headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

def annotate_image(image_url):
    response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    faces = response.json()
    
    image_file = BytesIO(requests.get(image_url).content)
    image = Image.open(image_file)
    
    plt.figure(figsize=(8,8))
    ax = plt.imshow(image, alpha=0.6)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(origin, fr["width"], \
                              fr["height"], fill=False, linewidth=2, color='b')
                              ax.axes.add_patch(p)
                              plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]), \
                                       fontsize=20, weight="bold", va="bottom")
    plt.axis("off")

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()
HTML("<font size='5'>Detected <font color='blue'>%d</font> faces in the image</font>"%len(faces))

%matplotlib inline
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib import patches
from io import BytesIO

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

plt.figure(figsize=(8,8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]), fontsize=20, weight="bold", va="bottom")
_ = plt.axis("off")

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('VPE+CQA/7xT/Gw7+AuQglKL7lHNyC+64k30AnkYlU///83YpPvE6vuyrBoU5oxvsCgNU6VMw/WlDBOHYrZnisRoIfP+qPVEBnAgEkDO29/mgM/RUNBwHwMPHLW1XdtVbIlzU6vcSgtfuPwKtuBqvyAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e4013cf04ebc446549c202098e9562a8')

@app.route('/')
def index():
    annotate_image("https://how-old.net/Images/faces2/main001.jpg")
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
                                   TextSendMessage(u"received undefine message"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
