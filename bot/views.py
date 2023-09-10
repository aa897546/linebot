from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from crawler.main import get_big_lottory  # , get_invoice_matching
from crawler.train import get_stations, get_train_data2

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

menu_str = ""
train_str = ""
stations = {}


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return HttpResponse(f"{now}<h1>歡迎使用機械怪物!</h1>")


def get_menu():
    global menu_str, stations
    if menu_str == "":
        stations = get_stations()
        menu = {i + 1: station for i, station in enumerate(stations)}
        count = 0

        for k, v in menu.items():
            menu_str += "{:2}.{:4}".format(k, v)
            count += 1
            if count % 4 == 0:
                menu_str += "\n"
    # return menu_str


# Create your views here.
@csrf_exempt  # 安全跨域請求機制
def callback(request):
    global menu_str, stations
    get_menu()
    print(menu_str)

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
                print(text)
                if text == "1":
                    text = menu_str
                if text == "2":
                    text = get_train_data2(
                        stations["臺北"], stations["基隆"], "2023/9/10", "00:00", "23:59"
                    )
                    print(text)
                if text == "3":
                    text = get_train_data2(
                        stations["臺北"], stations["基隆"], "2023/9/10", "00:00", "23:59"
                    )
                    print(text)
                message = TextSendMessage(text=text)
                try:
                    line_bot_api.reply_message(event.reply_token, message)
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
