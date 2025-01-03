const api_url = {
  production: "https://yielding-dove-samuelysliu-ce6a81f4.koyeb.app",
  uat: "https://classical-trish-samuelysliu-dbbd4671.koyeb.app",
  local: "http://10.103.178.9:8000"
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

const merchantId = {
  production: "",
  uat: "3002599",
  local: "3002599"
}

const hashKey = {
  production: "",
  uat: "spPjZn66i0OhqJsQ",
  local: "spPjZn66i0OhqJsQ"
}

const hashIv = {
  production: "",
  uat: "hT5OJckN45isQTTs",
  local: "hT5OJckN45isQTTs"
}


const config = {
  apiBaseUrl: api_url[process.env.NEXT_PUBLIC_ENV],
  gaId: gaId[process.env.NEXT_PUBLIC_ENV],
  googleClientId: googleClientId[process.env.NEXT_PUBLIC_ENV],
  cashFlowEndpoint: cashFlowEndpoint[process.env.NEXT_PUBLIC_ENV],
  merchantId: merchantId[process.env.NEXT_PUBLIC_ENV],
  hashKey: hashKey[process.env.NEXT_PUBLIC_ENV],
  hashIv: hashIv[process.env.NEXT_PUBLIC_ENV]
};
export default config;