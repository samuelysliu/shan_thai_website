const api_url = {
  production: "https://yielding-dove-samuelysliu-ce6a81f4.koyeb.app",
  uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
  local: "http://localhost:8000"
}

const gaId = {
  production: "G-SE5TV10X0K",
  uat: "G-7362PCKYH6",
  local: "G-7362PCKYH6"
}

const googleClientId = {
  production: "979016396209-meutophgongc1r1rkp8kh6a5jq0l0gqc.apps.googleusercontent.com",
  uat: "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com",
  local: "979016396209-tiqj9l71t819ueh8f4blrsoklr5daije.apps.googleusercontent.com"
}

const cashFlowEndpoint = {
  production: "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5",
  uat: "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5",
  local: "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
}

const storeMapEndpoint = {
  production: "https://logistics.ecpay.com.tw/Express/map",
  uat: "https://logistics-stage.ecpay.com.tw/Express/map",
  local: "https://logistics-stage.ecpay.com.tw/Express/map"
}

const sevenPrintEndpoint = {
  production: "https://logistics.ecpay.com.tw/Express/PrintUniMartC2COrderInfo",
  uat: "https://logistics-stage.ecpay.com.tw/Express/PrintUniMartC2COrderInfo",
  local: "https://logistics-stage.ecpay.com.tw/Express/PrintUniMartC2COrderInfo"
}

const familyPrintEndpoint = {
  production: "https://logistics.ecpay.com.tw/Express/PrintFAMIC2COrderInfo",
  uat: "https://logistics-stage.ecpay.com.tw/Express/PrintFAMIC2COrderInfo",
  local: "https://logistics-stage.ecpay.com.tw/Express/PrintFAMIC2COrderInfo"
}

const deliveryPrintEndpoint = {
  production: "https://logistics.ecpay.com.tw/helper/printTradeDocument",
  uat: "https://logistics-stage.ecpay.com.tw/helper/printTradeDocument",
  local: "https://logistics-stage.ecpay.com.tw/helper/printTradeDocument"
}

const merchantId = {
  production: "3437729",
  uat: "3002599",
  local: "3002599"
}

const hashKey = {
  production: "WsN2DCIPXSIwZWen",
  uat: "spPjZn66i0OhqJsQ",
  local: "spPjZn66i0OhqJsQ"
}

const hashIv = {
  production: "dfTmttwLSzjiZNqx",
  uat: "hT5OJckN45isQTTs",
  local: "hT5OJckN45isQTTs"
}

const logisticHashKey = {
  production: "WsN2DCIPXSIwZWen",
  uat: "XBERn1YOvpM9nfZc",
  local: "XBERn1YOvpM9nfZc"
}

const logisticHashIv = {
  production: "dfTmttwLSzjiZNqx",
  uat: "h1ONHk4P4yqbl5LK",
  local: "h1ONHk4P4yqbl5LK"
}

const config = {
  apiBaseUrl: api_url[process.env.NEXT_PUBLIC_ENV],
  gaId: gaId[process.env.NEXT_PUBLIC_ENV],
  googleClientId: googleClientId[process.env.NEXT_PUBLIC_ENV],
  cashFlowEndpoint: cashFlowEndpoint[process.env.NEXT_PUBLIC_ENV],
  merchantId: merchantId[process.env.NEXT_PUBLIC_ENV],
  hashKey: hashKey[process.env.NEXT_PUBLIC_ENV],
  hashIv: hashIv[process.env.NEXT_PUBLIC_ENV],
  storeMapEndpoint: storeMapEndpoint[process.env.NEXT_PUBLIC_ENV],
  sevenPrintEndpoint: sevenPrintEndpoint[process.env.NEXT_PUBLIC_ENV],
  familyPrintEndpoint: familyPrintEndpoint[process.env.NEXT_PUBLIC_ENV],
  deliveryPrintEndpoint: deliveryPrintEndpoint[process.env.NEXT_PUBLIC_ENV],
  logisticHashKey: logisticHashKey[process.env.NEXT_PUBLIC_ENV],
  logisticHashIv: logisticHashIv[process.env.NEXT_PUBLIC_ENV]
};
export default config;