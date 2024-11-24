// pages/index.js
"use client";

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Product_Grid from './components/Product_Grid';
import Product_Menu from './components/Product_Menu';
import Pagination_Component from './components/Pagination_Component';
import Footer from './components/Footer';
import Navbar from './components/Navbar';

import { Provider } from "react-redux";
import { store, persistor } from "./redux/store";
import { PersistGate } from "redux-persist/integration/react";


const HomePage = () => {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <Navbar />
        <Container>
          {/* Banner */}
          <Row>
            <Col>1 of 2</Col>
          </Row>
          {/* Menu */}
          <Product_Menu />
          {/* product */}
          <Product_Grid />
          <Pagination_Component />
          <Footer />
        </Container>
      </PersistGate>
    </Provider>
  );
};

export default HomePage;
