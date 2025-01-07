import config from "../config";

// 生成英數字混合長度為10的字串
export const generateRandomString = (length = 10) => {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }
    return result;
};

// 生成金流商需要的 CheckMacValue 函數
export const createCheckMacValue = (params) => {
    const hashKey = config.hashKey;
    const hashIv = config.hashIv;

    // 1. 將傳入的參數按字母順序排序
    const sortedParams = Object.keys(params)
        .sort()
        .map((key) => `${key}=${params[key]}`)
        .join("&");

    // 2. 在參數前后添加 HashKey 和 HashIV
    const toEncode = `HashKey=${hashKey}&${sortedParams}&HashIV=${hashIv}`;

    // 3. URL Encode 並替換空格為 '+'
    const urlEncodedString = encodeURIComponent(toEncode)
        .replace(/%20/g, "+")
        .toLowerCase();

    // 4. 使用 SHA256 進行加密
    const crypto = require("crypto");
    const hash = crypto.createHash("sha256");
    hash.update(urlEncodedString);
    const hashedValue = hash.digest("hex");

    // 5. 將加密結果轉為大寫
    return hashedValue.toUpperCase();
};

// 生成物流商需要的 CheckMacValue 函數
export const createLogisticCheckMacValue = (params) => {
    const hashKey = config.logisticHashKey;
    const hashIv = config.logisticHashIv;

    // 1. 將傳入的參數按字母順序排序
    const sortedParams = Object.keys(params)
        .sort()
        .map((key) => `${key}=${params[key]}`)
        .join("&");

    // 2. 在參數前后添加 HashKey 和 HashIV
    const toEncode = `HashKey=${hashKey}&${sortedParams}&HashIV=${hashIv}`;

    // 3. URL Encode 並替換空格為 '+'
    const urlEncodedString = encodeURIComponent(toEncode)
        .replace(/%20/g, "+")
        .toLowerCase();

    // 4. 使用 SHA256 進行加密
    const crypto = require("crypto");
    const hash = crypto.createHash("md5");
    hash.update(urlEncodedString);
    const hashedValue = hash.digest("hex");

    // 5. 將加密結果轉為大寫
    return hashedValue.toUpperCase();
};

// 取得使用者裝置類型
export const userDevice = () => {
    const userAgent = navigator.userAgent.toLowerCase();
    if (/mobile|android|iphone|ipad|tablet/i.test(userAgent)) {
        return "mobile";
    } else {
        return "desktop";
    }
}