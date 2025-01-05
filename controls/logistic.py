from controls.tools import format_to_utc8 as timeformat
import os
from dotenv import load_dotenv
import requests
from controls.tools import get_now_time
import hashlib
import urllib.parse
import modules.dbConnect as db_connect
import modules.logistics_order_crud as logistics_order_db

load_dotenv()
environment = os.getenv("ENVIRONMENT")
endpoint = os.getenv("WEBSITE_URL")

if environment == "production":
    temp_logistic_endpoint = (
        "https://logistics.ecpay.com.tw/Express/v2/RedirectToLogisticsSelection"
    )
    formal_logistic_endpoint = (
        "https://logistics.ecpay.com.tw/Express/v2/CreateByTempTrade"
    )
    store_logistic_endpoint = "https://logistics.ecpay.com.tw/Express/Create"
    merchant_id = "2000933"
    hash_key = "XBERn1YOvpM9nfZc"
    hash_iv = "h1ONHk4P4yqbl5LK"
    server_url = ""
else:
    temp_logistic_endpoint = (
        "https://logistics-stage.ecpay.com.tw/Express/v2/RedirectToLogisticsSelection"
    )
    formal_logistic_endpoint = (
        "https://logistics-stage.ecpay.com.tw/Express/v2/CreateByTempTrade"
    )
    store_logistic_endpoint = "https://logistics-stage.ecpay.com.tw/Express/Create"
    merchant_id = "2000933"
    hash_key = "XBERn1YOvpM9nfZc"
    hash_iv = "h1ONHk4P4yqbl5LK"
    server_url = ""


def create_checkMacValue(params: dict):
    # 1. 按字母順序對參數進行排序
    sorted_params = "&".join(f"{key}={params[key]}" for key in sorted(params.keys()))

    # 2. 在參數前后添加 HashKey 和 HashIV
    to_encode = f"HashKey={hash_key}&{sorted_params}&HashIV={hash_iv}"

    # 3. URL Encode 並替換空格為 '+'
    url_encoded_string = (
        urllib.parse.quote(to_encode, safe="").replace("%20", "+").lower()
    )

    # 4. 使用 MD5 進行加密
    hashed_value = hashlib.md5(url_encoded_string.encode("utf-8")).hexdigest()

    # 5. 將加密結果轉為大寫
    return hashed_value.upper()


def create_store_logistic_order(
    oid: str,
    trade_date: str,
    store_type: str,
    order_amount: int,
    isCollection: str,
    product: str,
    user_name: str,
    user_phone: str,
    user_email: str,
    store_id: str,
):
    if isCollection == "Y" and order_amount > 20000:
        return "failed"
    if order_amount > 20000:
        order_amount = 20000
    elif order_amount < 1:
        order_amount = 1

    if isCollection == "Y":
        collect_amount = order_amount
    else:
        collect_amount = 0
        
    if store_type == "seven":
        logisticsSubType = "UNIMARTC2C"
    elif store_type == "family":
        logisticsSubType = "FAMIC2C"
    else:
        return "failed"
        

    form_data = {
        "MerchantID": merchant_id,
        "MerchantTradeNo": oid,  # 廠商交易編號
        "MerchantTradeDate": trade_date,  # 廠商交易時間
        "LogisticsType": "CSV",  # 物流類型，CVS：超商取貨
        "LogisticsSubType": logisticsSubType,  # 物流子類型，FAMIC2C：全家店到店；UNIMARTC2C：7-ELEVEN超商交貨便
        "GoodsAmount": order_amount,  # 商品金額
        "CollectionAmount": collect_amount,  # 代收金額
        "IsCollection": isCollection,  # 是否代收貨款，N：不代收貨款，為預設值。Y：代收貨款，則代收貨款金額為商品金額。
        "GoodsName": product,  # 商品名稱
        "SenderName": "康敬豪",  # 寄件人姓名
        "SenderCellPhone": "0965105947",  # 寄件人手機
        "ReceiverName": user_name,  # 收件人姓名
        "ReceiverCellPhone": user_phone,  # 收件人手機
        "ReceiverEmail": user_email,  # 收件人email
        "ServerReplyURL": f"{endpoint}/frontstage/v1/store_logistic_order",  # Server端回覆網址
        "ReceiverStoreID": store_id,  # 收件人門市代號
    }

    form_data["CheckMacValu"] = create_checkMacValue(form_data)

    db = db_connect.SessionLocal()
    try:
        # 發送 POST 請求至物流商 API
        response = requests.post(store_logistic_endpoint, data=form_data)
        response_content = response.text

        if response_content.startswith("1|"):
            # 處理正確的回應
            _, data_string = response_content.split("|", 1)
            response_data = dict(item.split("=") for item in data_string.split("&"))

            # 儲存物流訂單記錄
            new_record = logistics_order_db.create_logistics_order(
                db=db,
                merchant_trade_no=response_data["MerchantTradeNo"],
                rtn_code=int(response_data["RtnCode"]),
                rtn_msg=response_data.get("RtnMsg", ""),
                allpay_logistics_id=response_data["AllPayLogisticsID"],
                logistics_type=response_data["LogisticsType"],
                logistics_sub_type=response_data["LogisticsSubType"],
                goods_amount=int(response_data["GoodsAmount"]),
                update_status_date=response_data.get("UpdateStatusDate"),
                receiver_name=response_data.get("ReceiverName"),
                receiver_cell_phone=response_data.get("ReceiverCellPhone"),
                receiver_email=response_data.get("ReceiverEmail"),
                receiver_address=response_data.get("ReceiverAddress"),
                cvs_payment_no=response_data.get("CVSPaymentNo"),
                cvs_validation_no=response_data.get("CVSValidationNo"),
                booking_note=response_data.get("BookingNote"),
            )

            if not new_record:
                return "failed"

            return "success"

        else:
            # 處理錯誤的回應
            error_message = response_content.split("|", 1)[1]
            print(f"Logistics API error: {error_message}")
            return "failed"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "failed"


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
        "Timestamp": get_now_time(
            "unix"
        )  # 為時間戳(GMT+8)，綠界會利用此參數將當下的時間轉為Unix TimeStamp來驗證此次介接的時間區間
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
        "Timestamp": get_now_time(
            "unix"
        )  # 為時間戳(GMT+8)，綠界會利用此參數將當下的時間轉為Unix TimeStamp來驗證此次介接的時間區間
    }
    Data = {"TempLogisticsID": TempLogisticsID, "MerchantTradeNo": order_id}

    json_data = {"MerchantID": MerchantID, "RqHeader": RqHeader, "Data": Data}

    response = requests.post(url=formal_logistic_endpoint, json=json_data)
    response = response.json()

    if response["Data"]["RtnCode"] == 1:
        return True
    else:
        return False
