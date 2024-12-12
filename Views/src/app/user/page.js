"use client";

import React from "react";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";

const UserProfilePage = () => {
  return (
    <ClientProvider>
        <NavBar />
        <Container>
        <OrderConfirm />
        </Container>
    </ClientProvider>
  );
};

export default UserProfilePage;
