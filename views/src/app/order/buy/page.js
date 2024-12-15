"use client";

import React from "react";
import ClientProvider from "@/app/components/Client_Provider";
import OrderConfirm from "@/app/components/order_components/Order_Confirm";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";

const BuyPage = () => {
  return (
    <ClientProvider>
        <NavBar />
        <Container>
        <OrderConfirm />
        </Container>
      
    </ClientProvider>
  );
};

export default BuyPage;
