"use client";

import React from "react";
import Cart from "@/app/components/order_components/Cart";
import ClientProvider from "@/app/components/Client_Provider";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import { Container } from "react-bootstrap";

export default function CartPage() {
    return (
        <ClientProvider>
            <Navbar />
            <Container>
                <Cart />
            </Container>
            <Footer />
        </ClientProvider>
    );
}
