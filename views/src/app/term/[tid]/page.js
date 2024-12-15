import React from "react";
import Term from "@/app/components/Term";
import config from "@/app/config";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";


// 提前讀取條款，以利SEO
const fetchTermDetail = async (tid) => {
  const endpoint = config.apiBaseUrl;
  try {
    const response = await fetch(`${endpoint}/frontstage/v1/term_by_id/${tid}`);
    if (!response.ok) {
      throw new Error('Failed to fetch term');
    }
    return await response.json();
  } catch (err) {
    console.error("無法加載條款", err);
    return [];
  }
}

const termPage = async ({ params }) => {
  const { tid } = params; // 從路由參數中取得產品 ID
  const term = await fetchTermDetail(tid); // 伺服器端獲取產品數據


  return (
    <ClientProvider>
      <NavBar />
      <Container>
        <Term term={term}></Term>
      </Container>
    </ClientProvider>
  );
};

export default termPage;
