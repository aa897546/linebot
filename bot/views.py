from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from crawler.main import get_big_lottory  # , get_invoice_matching

# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    StickerSendMessage,
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return HttpResponse(f"{now}<h1>歡迎使用機械怪物!</h1>")


# Create your views here.
@csrf_exempt  # 安全跨域請求機制
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                if text == "1":
                    message = TextSendMessage(text="早安")
                elif text == "2":
                    message = TextSendMessage(text="午安")
                elif "樂透" in text:
                    numbers = get_big_lottory()
                    message = TextSendMessage(text=numbers)
                elif "塔科夫" in text:
                    message = TextSendMessage(
                        text="https://escapefromtarkov.fandom.com/zh/wiki/Escape_from_Tarkov_Wiki?variant=zh-tw"
                    )
                elif "漫畫" in text:
                    message = TextSendMessage(text="https://m.manhuagui.com/")
                elif "捷運" in text:
                    if "台北" in text:
                        image_url = (
                            "https://www.travelking.com.tw/tourguide/mrt/images/map.png"
                        )
                    elif "桃園" in text:
                        image_url = (
                            "https://www.taoyuan-airport.com/api/uploads/img/mrt.jpg"
                        )
                    elif "台中" in text:
                        image_url = "https://jrhouse.net/wp-content/uploads/2021/04/2016%E5%B9%B4%E5%BA%95%E9%80%9A%E8%BB%8A%E7%9A%84%E5%8F%B0%E4%B8%AD%E5%B1%B1%E7%B7%9A%E9%90%B5%E8%B7%AF%E9%AB%98%E6%9E%B6%E6%8D%B7%E9%81%8B%E5%8C%96.png"
                    elif "台南" in text:
                        image_url = (
                            "https://calife.com.tw/wp-content/uploads/2019/01/photo.jpg"
                        )
                    elif "高雄" in text:
                        image_url = "https://upload.wikimedia.org/wikipedia/commons/5/56/%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B6%B2%E5%9C%96_%282020%29.png"
                    image_url = (
                        "https://www.travelking.com.tw/tourguide/mrt/images/map.png"
                    )
                    message = ImageSendMessage(
                        original_content_url=image_url, preview_image_url=image_url
                    )
                elif "台北車站" in text:
                    message = LocationSendMessage(
                        title="台北車站",
                        address="100台北市中正區鄭州路8號",
                        latiture=25.047778,
                        longiture=121.517222,
                    )
                # elif "發票" in text:
                #     message = get_invoice_matching()
                else:
                    message = TextSendMessage(text="我不知道你在說甚麼")
                # print(event.message.text)
                # if event.message.text=='hello':
                line_bot_api.reply_message(
                    event.reply_token,
                    # TextSendMessage(text='hello world')
                    message
                    # StickerMessage()
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
