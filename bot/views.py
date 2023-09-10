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
menu, stations = {}, {}
step = 0
startStation, endStation, rideDate, startTime, endTime = "", "", "", "", ""


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    return HttpResponse(f"{now}<h1>歡迎使用機械怪物!</h1>")


def get_menu():
    global menu, menu_str, stations
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
    global menu, menu_str, stations, step, startStation, endStation, rideDate, startTime, endTime
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
                try:
                    if text == "exit":
                        text = "感謝您的使用!(start:重新查詢)"
                        step = 0
                    if text == "start" and step == 0:
                        text = menu_str + "\n請輸入起始站點:"
                        step += 1
                    elif step == 1:
                        startStation = menu[eval(text)]
                        text = f"起始站: {startStation} \n請輸入終止站:"
                        step += 1
                    elif step == 2:
                        endStation = menu[eval(text)]
                        text = f"起始站:{startStation} 終止站: {endStation} \n請輸入乘車日期:(.:今日)"
                        step += 1
                    elif step == 3:
                        print(step)
                        if text == ".":
                            rideDate = datetime.now().strftime("%Y/%m/%d")
                        else:
                            rideDate = text
                        text = f"起始站:{startStation} 終止站: {endStation} \n乘車日期: {rideDate} \n請輸入查詢起始時間:(.:現在時間)"
                        step += 1
                    elif step == 4:
                        if text == ".":
                            startTime = datetime.now().strftime("%H:%M")
                        else:
                            startTime = text
                        text = f"起始站:{startStation} 終止站: {endStation}\n乘車日期: {rideDate} \n起始時間: {startTime} \n請輸入查詢終止時間:(.:23:59)"
                        step += 1
                    elif step == 5:
                        if text == ".":
                            endTime = "23:59"
                        else:
                            endTime = text
                        text = get_train_data2(
                            stations[startStation],
                            stations[endStation],
                            rideDate,
                            startTime,
                            endTime,
                        )
                        print(text)
                        text += "\n感謝您的使用!(start:重新查詢)"
                        step = 0
                except Exception as e:
                    print(e)
                    text = "輸入不正確,請重新輸入"

                message = TextSendMessage(text=text)

                try:
                    line_bot_api.reply_message(event.reply_token, message)
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
