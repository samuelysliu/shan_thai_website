import React from "react";
import Product_Detail from "@/app/components/product_components/Product_Detail";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";

const ProductDetailPage = async ({ params }) => {
  const { pid } = await params; // 從路由參數中取得產品 ID

  return (
    <ClientProvider>
      <Navbar />
      <Container>
        <Product_Detail pid={pid}></Product_Detail>
      </Container>
      <Footer />
    </ClientProvider>
  );
};

export default ProductDetailPage;
