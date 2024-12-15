"use client";

import React from "react";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";
import UserProfile from "@/app/components/user_components/User_Profile";

const UserProfilePage = () => {
  return (
    <ClientProvider>
        <NavBar />
        <Container>
        <UserProfile />
        </Container>
    </ClientProvider>
  );
};

export default UserProfilePage;
