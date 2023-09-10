import random
import requests
from bs4 import BeautifulSoup


def get_lottory():
    numbers = sorted(random.sample(list(range(1, 50)), 6))
    spec_number = random.randint(1, 50)
    numbers = ",".join(map(str, numbers)) + f"特別號:{spec_number}"

    print(numbers)
    return numbers


def get_big_lottory():
    url = "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        trs = soup.find("table", class_="table_org td_hm").find_all("tr")
        numbers = trs[4].text.strip().split()[1:]
        big_lottory = ",".join(numbers[:-1]) + f"特別號{numbers[-1]}"
        date = "，".join(trs[1].text.strip().split()[:2])
        result = f"期數/日期:\n{date}\n號碼{big_lottory}"
        return result
    except Exception as e:
        print(e)
    return "查詢失敗，請稍後查詢..."


# def get_invoice_matching():
#     url = "https://invoice.etax.nat.gov.tw/index.html"
#     try:
#         resp = requests.get(url)
#         soup = BeautifulSoup(resp.text, "lxml")
#         trs = soup.find("table", class_="etw-table-bgbox etw-tbig").find_all("tr")
#         numbers = trs[4].text.strip().split()[1:]
#         big_lottory = ",".join(numbers[:-1]) + f"特別號{numbers[-1]}"
#         date = "，".join(trs[1].text.strip().split()[:2])
#         result = f"期數/日期:\n{date}\n號碼{big_lottory}"
#         return result
#     except Exception as e:
#         print(e)
#     return "查詢失敗，請稍後查詢..."


get_lottory

if __name__ == "__main":
    get_lottory()
