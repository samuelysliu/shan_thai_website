// app/components/HomePageClient.js
"use client";  // 設定為客戶端組件

import React, { useState, useEffect } from "react";
import { Container } from 'react-bootstrap';
import Product_Grid from './product_components/Product_Grid';
import Product_Menu from './product_components/Product_Menu';
import Pagination_Component from './Pagination_Component';
import Footer from './Footer';
import Navbar from './Navbar';
import config from '../config';

const HomePageClient = ({ products, productTags }) => {
    const [filteredProducts, setFilteredProducts] = useState(products);
    const endpoint = config.apiBaseUrl;

    const [currentPage, setCurrentPage] = useState(1); // 當前頁
    const productsPerPage = 30; // 每頁顯示 30 項
    const totalProducts = filteredProducts.length;

    // 計算當前頁顯示的產品
    const startIndex = (currentPage - 1) * productsPerPage;
    const paginatedProducts = filteredProducts.slice(startIndex, startIndex + productsPerPage);

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
            setCurrentPage(1); // 重置為第一頁
        } catch (err) {
            console.error("無法加載指定標籤的產品清單", err);
            setFilteredProducts([]);
        }
    };

    // 處理頁碼點擊
    const handlePageChange = (page) => setCurrentPage(page);

    return (
        <>
            <Navbar />
            <Container className="app-container">
                {/* Banner */}
                {/* Menu */}
                <Product_Menu productTags={productTags} onTagSelect={handleTagSelect} />
                {/* Product Grid */}
                <Product_Grid initialProducts={paginatedProducts} />
                <Pagination_Component
                    totalProducts={totalProducts}
                    productsPerPage={productsPerPage}
                    currentPage={currentPage}
                    onPageChange={handlePageChange}
                />
            </Container>
            <Footer />
        </>
    );
};

export default HomePageClient;
