// app/components/HomePageClient.js
"use client";  // 設定為客戶端組件

import React, { useState } from "react";
import { Container, Row, Col } from 'react-bootstrap';
import Product_Grid from './Product_Grid';
import Product_Menu from './Product_Menu';
import Pagination_Component from './Pagination_Component';
import Footer from './Footer';
import Navbar from './Navbar';
import config from '../config';

const HomePageClient = ({ products, productTags }) => {
    const [filteredProducts, setFilteredProducts] = useState(products);
    let endpoint = config.apiBaseUrl;

    // 處理標籤選擇，根據選擇的標籤從伺服器端獲取產品
    const handleTagSelect = async (tagId) => {
        console.log(tagId);
        try {
            const response = await fetch(`${endpoint}/frontstage/v1/product_by_tag/${tagId}`, { cache: 'no-store' });
            if (!response.ok) {
                throw new Error('Failed to fetch products');
            }
            const filteredProducts = await response.json();
            setFilteredProducts(filteredProducts);
        } catch (err) {
            console.error("無法加載指定標籤的產品清單", err);
            setFilteredProducts([]);
        }
    };

    return (
        <>
            <Navbar />
            <Container>
                {/* Banner */}
                <Row>
                    <Col>1 of 2</Col>
                </Row>
                {/* Menu */}
                <Product_Menu productTags={productTags} onTagSelect={handleTagSelect} />
                {/* Product Grid */}
                <Product_Grid initialProducts={filteredProducts} />
                <Pagination_Component />
                <Footer />
            </Container>
        </>
    );
};

export default HomePageClient;
