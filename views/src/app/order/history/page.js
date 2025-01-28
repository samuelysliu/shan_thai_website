"use client";

import React from "react";
import OrderHistory from "@/app/components/order_components/Order_History";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";

const OrderHistoryPage = () => {
  return (
    <ClientProvider>
      <NavBar />
      <Container>
        <OrderHistory />
      </Container>
    </ClientProvider>
  );
};

export default OrderHistoryPage;
