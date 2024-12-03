// pages/index.js
import React from "react";
import { Container, Row, Col } from 'react-bootstrap';
import Product_Grid from './components/Product_Grid';
import Product_Menu from './components/Product_Menu';
import Pagination_Component from './components/Pagination_Component';
import Footer from './components/Footer';
import Navbar from './components/Navbar';

import ClientProvider from "./components/Client_Provider";

import config from './config';


// 使用 getServerSideProps 進行 SSR 數據加載，提前讀取產品清單，以利SEO
const fetchProducts = async () => {
  let endpoint = config.apiBaseUrl;
  try {
    const response = await fetch(endpoint + "/frontstage/v1/product", { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return await response.json();
  } catch (err) {
    console.error("無法加載產品清單", err);
    return [];
  }
}


const HomePage = async () => {
  const products = await fetchProducts(); // 服務端獲取產品列表

  return (
    <ClientProvider>
      <Navbar />
      <Container>
        {/* Banner */}
        <Row>
          <Col>1 of 2</Col>
        </Row>
        {/* Menu */}
        <Product_Menu />
        {/* product */}
        <Product_Grid initialProducts={products} />
        <Pagination_Component />
        <Footer />
      </Container>
    </ClientProvider>
  );
};

export default HomePage;
