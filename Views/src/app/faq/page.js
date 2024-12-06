"use client";

import React from "react";
import FAQ from "../components/FAQ";
import Navbar from "../components/Navbar"
import { Container } from "react-bootstrap";
import Footer from "../components/Footer";
import ClientProvider from "../components/Client_Provider";

const FAQPage = () => {
    return (
        <ClientProvider>
            <Navbar />
            <Container>
                <FAQ />
            </Container>
            <Footer />
        </ClientProvider>

    );
};

export default FAQPage;
