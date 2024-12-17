import { jwtDecode } from "jwt-decode";

export const isTokenExpired = (token) => {
  if (!token) return true; // 如果沒有 Token 視為過期
  try {
    const { exp } = jwtDecode(token); // 解析 Token 的過期時間
    if (exp * 1000 < Date.now()) {
      return true; // Token 過期了
    }
    return false; // Token 還有效
  } catch (error) {
    console.error("Failed to decode token:", error);
    return true; // 無法解析視為過期
  }
};
