from controls.tools import format_to_utc8 as timeformat
import os
from dotenv import load_dotenv
import jwt
import requests

load_dotenv()
environment= os.getenv("ENVIRONMENT")
endpoint = os.getenv("WEBSITE_URL")

if environment == "production":
    cash_flow_endpoint = "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5"
    merchant_id = "3002599"
    hash_key = "spPjZn66i0OhqJsQ"
    hash_iv = "hT5OJckN45isQTTs"
else:
    cash_flow_endpoint = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
    merchant_id = "3002599"
    hash_key = "spPjZn66i0OhqJsQ"
    hash_iv = "hT5OJckN45isQTTs"
    server_url = "http://192.168.1.110"


# 建立金流訂單
def create_cash_flow_order(payment_methods: str, order_id: str, order_date: str, order_amount: int):
    MerchantID = merchant_id    # 特店編號
    MerchantTradeNo = order_id  # 特店訂單編號  
    MerchantTradeDate = order_date  #yyyy/MM/dd HH:mm:ss
    PaymentType = "aio"
    TotalAmount = order_amount  #交易金額
    TradeDesc = "善泰團隊聖物" #交易描述
    ItemName = "善泰團隊聖物"  #商品名稱，如果商品名稱有多筆，需在金流選擇頁一行一行顯示商品名稱的話，商品名稱請以符號#分隔
    ReturnURL = f"{server_url}/frontstage/v1/cash_flow_order"    #付款完成通知回傳網址
    ChoosePayment = payment_methods #Credit：信用卡及銀聯卡、ATM：自動櫃員機
    EncryptType = 1 #固定填入1，使用SHA256加密
    ClientBackURL = f"{endpoint}/order/history" 
    CheckMacValue = create_checkMacValue(MerchantID, MerchantTradeNo, MerchantTradeDate, TotalAmount, TradeDesc, ItemName, ReturnURL, ChoosePayment, ClientBackURL)    #檢查碼

    form_data = {
        "MerchantID": MerchantID,
        "MerchantTradeNo": MerchantTradeNo,
        "MerchantTradeDate": MerchantTradeDate,
        "PaymentType": PaymentType,
        "TotalAmount":TotalAmount,
        "TradeDesc": TradeDesc,
        "ItemName": ItemName,
        "ReturnURL": ReturnURL,
        "ChoosePayment": ChoosePayment,
        "CheckMacValue": CheckMacValue,
        "EncryptType": EncryptType,
        "ClientBackURL": ClientBackURL,   
    }
    
    requests.post(cash_flow_endpoint, data=form_data)
    
    
def create_checkMacValue(MerchantID, MerchantTradeNo, MerchantTradeDate, TotalAmount, TradeDesc, ItemName, ReturnURL, ChoosePayment, ClientBackURL):
    SECRET_KEY = "shan_thai_project"
    ALGORITHM = "SHA256"
    
    to_encode = (
        f"HashKey={hash_key}&MerchantID={MerchantID}&MerchantTradeNo={MerchantTradeNo}" 
        f"&MerchantTradeDate={MerchantTradeDate}&PaymentType=aio&TotalAmount={TotalAmount}&TradeDesc={TradeDesc}" 
        f"ItemName={ItemName}&ReturnURL={ReturnURL}&ChoosePayment={ChoosePayment}&ClientBackURL={ClientBackURL}"
        f"&EncryptType=1&HashIV={hash_iv}"
    )
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)