from controls.tools import format_to_utc8 as timeformat
import os
from dotenv import load_dotenv
import jwt
import requests
from controls.tools import get_now_time

load_dotenv()
environment= os.getenv("ENVIRONMENT")
endpoint = os.getenv("WEBSITE_URL")

if (environment== "production"):
    temp_logistic_endpoint = "https://logistics.ecpay.com.tw/Express/v2/RedirectToLogisticsSelection"
    formal_logistic_endpoint = "https://logistics.ecpay.com.tw/Express/v2/CreateByTempTrade"
    merchant_id = "2000933"
    hash_key = "XBERn1YOvpM9nfZc"
    hash_iv = "h1ONHk4P4yqbl5LK"
    server_url = ""
else:
    temp_logistic_endpoint = "https://logistics-stage.ecpay.com.tw/Express/v2/RedirectToLogisticsSelection"
    formal_logistic_endpoint = "https://logistics-stage.ecpay.com.tw/Express/v2/CreateByTempTrade"ㄕㄛ
    merchant_id = "2000933"
    hash_key = "XBERn1YOvpM9nfZc"
    hash_iv = "h1ONHk4P4yqbl5LK"
    server_url = ""


def create_temp_logistic_order(
    order_amount: int,
    is_collection: str,
    product: str,
    remark: str,
    user_phone: str,
    user_name: str,
):
    if order_amount > 20000:
        order_amount = 20000
    elif order_amount < 1:
        order_amount = 1

    MerchantID = merchant_id  # 特店編號
    RqHeader = {
        "Timestamp": get_now_time("unix")  # 為時間戳(GMT+8)，綠界會利用此參數將當下的時間轉為Unix TimeStamp來驗證此次介接的時間區間
    }
    Data = {
        "TempLogisticsID": 0,  # 新建暫存物流訂單時，此參數請帶0
        "GoodsAmount": order_amount,  # 商品金額範圍為1~20000元
        "IsCollection": is_collection,  # 是否代收貨款，N：不代收貨款，為預設值。Y：代收貨款，帶入Y則物流選擇頁將不會出現宅配選項。
        "GoodsName": product,  # 商品名稱
        "SenderName": "康敬豪",
        "SenderZipCode": "242",
        "SenderAddress": "新北市新莊區龍安路487巷2弄7號4樓",
        "Remark": remark,  # 備註
        "ServerReplyURL": "",  # Server端回覆網址
        "ClientReplyURL": "",  # Client端回覆網址
        "Specification": "",  # 規格，0001: 60cm (預設值)；0002: 90cm；0003: 120cm；0004: 150cm
        "ScheduledPickupTime": "4",  # 預定取件時段
        "ReceiverCellPhone": user_phone,
        "ReceiverName": user_name,
    }

    json_data = {"MerchantID": MerchantID, "RqHeader": RqHeader, "Data": Data}

    response = requests.post(url=temp_logistic_endpoint, json=json_data)
    response = response.json()

    if response["ResultData"]["Data"]["RtnCode"] == 1:
        return True
    else:
        return False

def create_formal_logistic_order(TempLogisticsID: str, order_id: str):
    MerchantID = merchant_id  # 特店編號
    RqHeader = {
        "Timestamp": get_now_time("unix")  # 為時間戳(GMT+8)，綠界會利用此參數將當下的時間轉為Unix TimeStamp來驗證此次介接的時間區間
    }
    Data = {
        "TempLogisticsID": TempLogisticsID,
        "MerchantTradeNo": order_id
    }
    
    json_data = {"MerchantID": MerchantID, "RqHeader": RqHeader, "Data": Data}
    
    response = requests.post(url=formal_logistic_endpoint, json=json_data)
    response = response.json()
    
    if response["Data"]["RtnCode"] == 1:
        return True
    else:
        return False