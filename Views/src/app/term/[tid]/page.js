import React from "react";
import Term from "@/app/components/Term";


// 提前讀取產品清單，以利SEO
const fetchTermDetail = async (tid) => {
  let endpoint = config.apiBaseUrl;
  try {
    const response = await fetch(`${endpoint}/frontstage/v1/term_by_id/${tid}`);
    if (!response.ok) {
      throw new Error('Failed to fetch term');
    }
    return await response.json();
  } catch (err) {
    console.error("無法加載產品清單", err);
    return [];
  }
}

const termPage = async ({ params }) => {
  const { tid } = params; // 從路由參數中取得產品 ID
  const term = await fetchTermDetail(tid); // 伺服器端獲取產品數據


  return (
    <>
      <Term term={term}></Term>
    </>
  );
};

export default termPage;
