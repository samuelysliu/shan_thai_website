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
import axios from "axios";
import { useSelector } from "react-redux";

const HomePageClient = () => {
    const [filteredProducts, setFilteredProducts] = useState([0]);
    const endpoint = config.apiBaseUrl;

    const [productTags, setProductTags] = useState([]);

    // 取得用戶資料
    const { token } = useSelector((state) => state.user);

    const [currentPage, setCurrentPage] = useState(1); // 當前頁
    const productsPerPage = 30; // 每頁顯示 30 項
    const totalProducts = filteredProducts.length;

    // 計算當前頁顯示的產品
    const startIndex = (currentPage - 1) * productsPerPage;
    const paginatedProducts = filteredProducts.slice(startIndex, startIndex + productsPerPage);

    // 取得標籤內的產品內容
    const getProductList = async (tagId) => {
        setFilteredProducts([0]);
        try {
            let response = "";
            if (tagId === -1) {
                response = await axios.get(
                    `${endpoint}/frontstage/v1/product`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`, // 加入 Authorization header
                        },
                    }
                );
            } else {
                response = await axios.get(
                    `${endpoint}/frontstage/v1/product_by_tag/${tagId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`, // 加入 Authorization header
                        },
                    }
                );
            }
            setFilteredProducts(response.data);
            setCurrentPage(1); // 重置為第一頁;
        } catch (err) {
            console.error("無法取得產品清單", err);
            setFilteredProducts([]);
        }
    };

    // 取得產品標籤列表
    const getProductTagList = async () => {
        try {
            let response = await axios.get(
                `${endpoint}/frontstage/v1/product_tag`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`, // 加入 Authorization header
                    },
                }
            );
            setProductTags(response.data);
        } catch (err) {
            console.error("無法取得標籤清單", err);
            setFilteredProducts([]);
        }

    };

    useEffect(() => {
        getProductList(-1);
        getProductTagList();
    }, []);



    // 處理頁碼點擊
    const handlePageChange = (page) => setCurrentPage(page);

    return (
        <>
            <Navbar />
            <Container className="app-container">
                {/* Banner */}
                {/* Menu */}
                <Product_Menu productTags={productTags} onTagSelect={getProductList} />
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
