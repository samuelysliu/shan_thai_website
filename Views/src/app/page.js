// pages/index.js
"use client";

import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import Product_Grid from './components/Product_Grid';
import Product_Menu from './components/Product_Menu';
import Pagination_Component from './components/Pagination_Component';
import Footer from './components/Footer';
import Navbar from './components/Navbar';

import { Provider } from "react-redux";
import { store } from "./redux/store";


const HomePage = () => {
  return (
    <>
      <Navbar />
      <Container>
        {/* Banner */}
        <Row>
          <Col>1 of 2</Col>
        </Row>
        {/* Menu */}
        <Product_Menu />
        {/* product */}
        <Provider store={store}>
          <Product_Grid />
        </Provider>
        <Pagination_Component />
        <Footer />

      </Container>
    </>
  );
};

export default HomePage;
