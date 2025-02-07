from controls.tools import format_to_utc8 as timeformat
import os
from dotenv import load_dotenv
import requests
from controls.tools import get_now_time, string_to_postgreSQL_time
import hashlib
import urllib.parse
import modules.dbConnect as db_connect
import modules.logistics_order_crud as logistics_order_db
import modules.order_crud as order_db

load_dotenv()
environment = os.getenv("ENVIRONMENT")
endpoint = os.getenv("WEBSITE_URL")

if environment == "production":
    logistic_endpoint = "https://logistics.ecpay.com.tw/Express/Create"
    logistic_check_endpoint = "https://logistics.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V5"
    merchant_id = "3437729"
    hash_key = "WsN2DCIPXSIwZWen"
    hash_iv = "dfTmttwLSzjiZNqx"
else:
    logistic_endpoint = "https://logistics-stage.ecpay.com.tw/Express/Create"
    logistic_check_endpoint = "https://logistics-stage.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V5"
    merchant_id = "2000933"
    hash_key = "XBERn1YOvpM9nfZc"
    hash_iv = "h1ONHk4P4yqbl5LK"


def create_checkMacValue(params: dict):
    # 1. 按字母順序對參數進行排序
    sorted_params = "&".join(f"{key}={params[key]}" for key in sorted(params.keys()))

    # 2. 在參數前后添加 HashKey 和 HashIV
    to_encode = f"HashKey={hash_key}&{sorted_params}&HashIV={hash_iv}"

    # 3. URL Encode 並替換空格為 '+'
    url_encoded_string = urllib.parse.quote(to_encode, safe="").lower()
    url_encoded_string = url_encoded_string.replace("%20", "+")
    url_encoded_string = url_encoded_string.replace("%2d", "-")
    url_encoded_string = url_encoded_string.replace("%5f", "_")
    url_encoded_string = url_encoded_string.replace("%2e", ".")
    url_encoded_string = url_encoded_string.replace("%21", "!")
    url_encoded_string = url_encoded_string.replace("%2a", "*")
    url_encoded_string = url_encoded_string.replace("%28", "(")
    url_encoded_string = url_encoded_string.replace("%29", ")")

    # 4. 使用 MD5 進行加密
    hashed_value = hashlib.md5(url_encoded_string.encode("utf-8")).hexdigest()

    # 5. 將加密結果轉為大寫
    return hashed_value.upper()


# 建立超商領貨的物流單
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
        print(f"訂單 {oid} 貨到付款金額超過 2 萬元")
        return {"detail": "error", "reason": ""}
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
        print(f"function create_store_logistic_order 有非法呼叫，帶 store_type 為 {store_type}")
        return {"detail": "error", "reason": ""}

    form_data = {
        "MerchantID": merchant_id,
        "MerchantTradeNo": oid,  # 廠商交易編號
        "MerchantTradeDate": trade_date,  # 廠商交易時間
        "LogisticsType": "CVS",  # 物流類型，CVS：超商取貨
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
        "ServerReplyURL": f"{endpoint}/backstage/v1/logistics_callback",  # Server端回覆網址
        "ReceiverStoreID": store_id,  # 收件人門市代號
    }

    form_data["CheckMacValue"] = create_checkMacValue(form_data)
    db = db_connect.SessionLocal()
    try:
        # 發送 POST 請求至物流商 API
        response = requests.post(logistic_endpoint, data=form_data)
        response_content = response.text

        if response_content.startswith("1|"):
            # 處理正確的回應
            _, data_string = response_content.split("|", 1)
            response_data = dict(item.split("=") for item in data_string.split("&"))

            # 儲存物流訂單記錄
            logistics_order_db.create_logistics_order(
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

            return {"detail": "success", "reason": ""}

        else:
            # 處理錯誤的回應
            error_message = response_content.split("|", 1)[1]
            print(f"Logistics API error: {error_message}")
            return {"detail": "failed", "reason": error_message}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"detail": "failed", "reason": str(e)}


# 建立宅配的物流單
def create_home_logistic_order(
    oid: str,
    trade_date: str,
    order_amount: int,
    product: str,
    product_weight: int,
    user_name: str,
    user_phone: str,
    zip_code: str,
    address: str,
    user_email: str,
):
    try:
        form_data = {
            "MerchantID": merchant_id,
            "MerchantTradeNo": oid,  # 廠商交易編號
            "MerchantTradeDate": trade_date,  # 廠商交易時間
            "LogisticsType": "HOME",  # 物流類型，CVS：超商取貨； HOME:宅配
            "LogisticsSubType": "POST",  # 物流子類型，TCAT:黑貓；POST:中華郵政
            "GoodsAmount": order_amount,  # 商品金額
            "GoodsName": product,  # 商品名稱
            "GoodsWeight": product_weight,
            "SenderName": "康敬豪",  # 寄件人姓名
            "SenderCellPhone": "0965105947",  # 寄件人手機
            "SenderZipCode": "242",  # 寄件人郵遞區號
            "SenderAddress": "新北市新莊區龍安路487巷2弄7號4樓",  # 寄件人地址
            "ReceiverName": user_name,  # 收件人姓名
            "ReceiverCellPhone": user_phone,  # 收件人手機
            "ReceiverZipCode": zip_code,  # 收件人郵遞區號
            "ReceiverAddress": address,  # 收件人地址
            "ReceiverEmail": user_email,  # 收件人email,
            "Temperature": "0001",
            "ServerReplyURL": f"{endpoint}/backstage/v1/logistics_callback",  # Server端回覆網址
        }

        form_data["CheckMacValue"] = create_checkMacValue(form_data)
        db = db_connect.SessionLocal()
        response = requests.post(logistic_endpoint, data=form_data)
        response_content = response.text

        if response_content.startswith("1|"):
            # 處理正確的回應
            _, data_string = response_content.split("|", 1)
            response_data = dict(item.split("=") for item in data_string.split("&"))
            # 儲存物流訂單記錄
            logistics_order_db.create_logistics_order(
                db=db,
                merchant_trade_no=oid,
                rtn_code=response_data["RtnCode"],
                allpay_logistics_id=response_data["AllPayLogisticsID"],
                rtn_msg=response_data.get("RtnMsg", ""),
                logistics_type=response_data["LogisticsType"],
                logistics_sub_type=response_data["LogisticsSubType"],
                goods_amount=response_data["GoodsAmount"],
                update_status_date=string_to_postgreSQL_time(
                    response_data["UpdateStatusDate"]
                ),
                receiver_name=response_data["ReceiverName"],
                receiver_cell_phone=response_data["ReceiverCellPhone"],
                receiver_email=response_data["ReceiverEmail"],
                receiver_address=response_data["ReceiverAddress"],
                cvs_payment_no=response_data["CVSPaymentNo"],
                cvs_validation_no=response_data["CVSValidationNo"],
                booking_note=response_data["BookingNote"],
            )

            return {"detail": "success", "reason": ""}

        else:
            # 處理錯誤的回應
            error_message = response_content.split("|", 1)[1]
            print(f"Logistics API error: {error_message}")
            return {"detail": "failed", "reason": error_message}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"detail": "failed", "reason": str(e)}


# 查詢物流狀態
def check_logistic_status():
    db = db_connect.SessionLocal()
    try:
        order_list = order_db.get_order_by_status(db, "待出貨")
        
        # 逐一去呼叫 API 確定物流狀態
        for order in order_list:
            params = dict(
                {
                    "MerchantID": merchant_id,  # 特店編號(由綠界提供
                    "MerchantTradeNo": order["oid"],  # 特店交易編號
                    "TimeStamp": get_now_time("unix"),
                }
            )
            print(order["oid"])
            chcek_mac_value = create_checkMacValue(params)
            params["CheckMacValue"] = chcek_mac_value

            # API 回傳為字串，需要做解析轉成 dict
            response = requests.post(logistic_check_endpoint, data=params)
            response_dict = dict(item.split("=") for item in response.text.split("&") if "=" in item)
            
            # 取得目標欄位
            RtnCode = response_dict.get("LogisticsStatus", "")
            
            if RtnCode == "2030" or RtnCode == "3024":
                update_data = {"status": "已出貨"}
            elif RtnCode == "2073" or RtnCode == "3018":
                update_data = {"status": "已送達"}
            elif RtnCode == "2067" or RtnCode == "3022":
                update_data = {"status": "已完成"}
            elif RtnCode == "2074" or RtnCode == "3020":
                update_data = {"status": "已取消"}

            updated_order = order_db.update_order(db, oid=order["oid"], updates=update_data)
            if not updated_order:
                print({order["oid"]} + f" 訂單更新物流狀態為 {update_data} 更新失敗")
                
    except Exception as e:
        print(f"System Log: logistic.py check_logistic_status function {e}")
    finally:
        db.close()