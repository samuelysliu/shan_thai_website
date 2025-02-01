from controls.tools import get_now_time, string_to_postgreSQL_time
import os
from dotenv import load_dotenv
import hashlib
import urllib.parse
import modules.payment_callback_curd as payment_callback_db
import requests
import modules.dbConnect as db_connect
import modules.order_crud as order_db
from urllib.parse import parse_qs

load_dotenv()
environment = os.getenv("ENVIRONMENT")

if environment == "production":
    order_check_endpoint = "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5"
    atm_number_check_endpoint = "https://payment.ecpay.com.tw/Cashier/QueryPaymentInfo"
    merchant_id = "3437729"
    hash_key = "WsN2DCIPXSIwZWen"
    hash_iv = "dfTmttwLSzjiZNqx"
else:
    order_check_endpoint = (
        "https://payment-stage.ecpay.com.tw/Cashier/QueryTradeInfo/V5"
    )
    atm_number_check_endpoint = (
        "https://payment-stage.ecpay.com.tw/Cashier/QueryPaymentInfo"
    )
    merchant_id = "3002599"
    hash_key = "spPjZn66i0OhqJsQ"
    hash_iv = "hT5OJckN45isQTTs"


def create_checkMacValue(params: dict):
    # 1. 按字母順序對參數進行排序
    sorted_params = "&".join(
        f"{key}={params[key]}" for key in sorted(params.keys(), key=lambda x: str(x))
    )

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

    # 4. 使用 SHA256 進行加密
    hashed_value = hashlib.sha256(url_encoded_string.encode("utf-8")).hexdigest()

    # 5. 將加密結果轉為大寫
    return hashed_value.upper()


def check_order():
    db = db_connect.SessionLocal()
    try:
        order_list = order_db.get_order_by_status(db, "待確認")

        # 逐一將沒有確認付款資訊的訂單去呼叫 API
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
            response = requests.post(order_check_endpoint, data=params)
            # 解析字串為字典
            parsed_data = {
                key: value[0] for key, value in parse_qs(response.text).items()
            }

            # 儲存金流回傳的紀錄
            table_column = [
                "MerchantID",
                "MerchantTradeNo",
                "StoreID",
                "RtnCode",
                "RtnMsg" "TradeNo",
                "TradeAmt",
                "PaymentDate",
                "PaymentType",
                "PaymentTypeChargeFee",
                "PlatformID",
                "TradeDate",
                "SimulatePaid",
                "CheckMacValue",
                "BankCode",
                "vAccount",
                "ExpireDate",
            ]

            for column in table_column:
                if column not in parsed_data:
                    parsed_data[column] = None

            if (
                parsed_data.get("TradeStatus") == "1"
                or parsed_data.get("TradeStatus") == "10200095"
            ):
                create_payment_callback_record(
                    db=db,
                    MerchantID=parsed_data.get("MerchantID"),
                    MerchantTradeNo=parsed_data.get("MerchantTradeNo"),
                    StoreID=parsed_data.get("StoreID"),
                    RtnCode=parsed_data.get("TradeStatus"),
                    RtnMsg=parsed_data.get("RtnMsg"),
                    TradeNo=parsed_data.get("TradeNo"),
                    TradeAmt=parsed_data.get("TradeAmt"),
                    PaymentDate=parsed_data.get("PaymentDate"),
                    PaymentType=parsed_data.get("PaymentType"),
                    PaymentTypeChargeFee=parsed_data.get("PaymentTypeChargeFee"),
                    PlatformID=None,
                    TradeDate=parsed_data.get("TradeDate"),
                    SimulatePaid=1,
                    CheckMacValue=parsed_data.get("CheckMacValue"),
                    BankCode=parsed_data.get("BankCode"),
                    vAccount=parsed_data.get("vAccount"),
                    ExpireDate=parsed_data.get("ExpireDate"),
                )

                # 更改訂單狀態
                if parsed_data.get("TradeStatus") == "1":
                    update_data = {"status": "待出貨"}
                elif parsed_data.get("TradeStatus") == "10200095":
                    update_data = {"status": "已取消"}

                updated_order = order_db.update_order(
                    db, oid=order["oid"], updates=update_data
                )
                if not updated_order:
                    print("訂單" + order["oid"] + f"更新 {update_data} 失敗")

    except Exception as e:
        print(e)
    finally:
        db.close()


def check_order_id(MerchantTradeNo: str):
    params = dict(
        {
            "MerchantID": merchant_id,  # 特店編號(由綠界提供
            "MerchantTradeNo": MerchantTradeNo,  # 特店交易編號
            "TimeStamp": get_now_time("unix"),
        }
    )

    chcek_mac_value = create_checkMacValue(params)
    params["CheckMacValue"] = chcek_mac_value

    # API 回傳為字串，需要做解析轉成 dict
    response = requests.post(order_check_endpoint, data=params)
    # 解析字串為字典
    parsed_data = {key: value[0] for key, value in parse_qs(response.text).items()}
    return parsed_data


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
    ExpireDate,
):
    try:
        PaymentDate = string_to_postgreSQL_time(PaymentDate)
        TradeDate = string_to_postgreSQL_time(TradeDate)
        ExpireDate = string_to_postgreSQL_time(ExpireDate)
        payment_callback_db.create_payment_callback(
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

    except:
        print("Failed to create payment callback record")


# 檢視匯款的帳號
def get_atm_account(oid: str):
    form_data = {
        "MerchantID": merchant_id,
        "MerchantTradeNo": oid,  # 廠商交易編號
        "TimeStamp": get_now_time("unix"),
    }
    form_data["CheckMacValue"] = create_checkMacValue(form_data)

    response = requests.post(atm_number_check_endpoint, data=form_data)
    # 解析字串為字典
    parsed_data = {key: value[0] for key, value in parse_qs(response.text).items()}

    return {
        "tradeAmt": parsed_data["TradeAmt"],
        "bankCode": parsed_data["BankCode"],
        "vAccount": parsed_data["vAccount"],
        "expireDate": parsed_data["ExpireDate"],
    }
