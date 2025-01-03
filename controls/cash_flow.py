from controls.tools import get_now_time, string_to_postgreSQL_time
import os
from dotenv import load_dotenv
import hashlib
import urllib.parse
import modules.payment_callback_curd as payment_callback_db
import requests

load_dotenv()
environment = os.getenv("ENVIRONMENT")
endpoint = os.getenv("WEBSITE_URL")

if environment == "production":
    order_check_endpoint = "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5"
    merchant_id = "3002599"
    hash_key = "spPjZn66i0OhqJsQ"
    hash_iv = "hT5OJckN45isQTTs"
else:
    order_check_endpoint = (
        "https://payment-stage.ecpay.com.tw/Cashier/QueryTradeInfo/V5"
    )
    merchant_id = "3002599"
    hash_key = "spPjZn66i0OhqJsQ"
    hash_iv = "hT5OJckN45isQTTs"


def create_checkMacValue(params: dict):
    # 1. 按字母順序對參數進行排序
    sorted_params = "&".join(f"{key}={params[key]}" for key in sorted(params.keys()))

    # 2. 在參數前后添加 HashKey 和 HashIV
    to_encode = f"HashKey={hash_key}&{sorted_params}&HashIV={hash_iv}"

    # 3. URL Encode 並替換空格為 '+'
    url_encoded_string = (
        urllib.parse.quote(to_encode, safe="").replace("%20", "+").lower()
    )

    # 4. 使用 SHA256 進行加密
    hashed_value = hashlib.sha256(url_encoded_string.encode("utf-8")).hexdigest()

    # 5. 將加密結果轉為大寫
    return hashed_value.upper()


def check_order(order_id):
    params = dict(
        {
            "MerchantID": merchant_id,  # 特店編號(由綠界提供
            "MerchantTradeNo": order_id,  # 特店交易編號
            "TimeStamp": get_now_time("unix"),
        }
    )
    chcek_mac_value = create_checkMacValue(params)
    params["CheckMacValue"] = chcek_mac_value

    response = requests.post(order_check_endpoint, data=params)
    return response.json()
    
    

def create_payment_callback_record(
    db,
    MerchantID,
    MerchantTradeNo,
    StoreID,
    RtnCode,
    RtnMsg,
    TradeNo,
    TradeAmt,
    PaymentDate,
    PaymentType,
    PaymentTypeChargeFee,
    PlatformID,
    TradeDate,
    SimulatePaid,
    CheckMacValue,
    BankCode,
    vAccount,
    ExpireDate
):
    try:
        PaymentDate = string_to_postgreSQL_time(PaymentDate)
        TradeDate = string_to_postgreSQL_time(TradeDate)
        ExpireDate = string_to_postgreSQL_time(ExpireDate)

        new_record = payment_callback_db.create_payment_callback(
            db=db,
            merchant_id=MerchantID,
            merchant_trade_no=MerchantTradeNo,
            store_id=StoreID,
            rtn_code=RtnCode,
            rtn_msg=RtnMsg,
            trade_no=TradeNo,
            trade_amt=TradeAmt,
            payment_date=PaymentDate,
            payment_type=PaymentType,
            payment_type_charge_fee=PaymentTypeChargeFee,
            platform_id=PlatformID,
            trade_date=TradeDate,
            simulate_paid=SimulatePaid,
            check_mac_value=CheckMacValue,
            bank_code=BankCode,
            v_account=vAccount,
            expire_date=ExpireDate,
        )

        if not new_record:
            print("Failed to create payment callback record")

    except:
        print("Failed to create payment callback record")
