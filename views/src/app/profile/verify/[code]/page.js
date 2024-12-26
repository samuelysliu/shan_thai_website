import React from "react";
import ClientProvider from "@/app/components/Client_Provider";
import { Container } from "react-bootstrap";
import VerifyPage from "@/app/components/user_components/Verify_Page";

const UserVerifyPage = async ({ params }) => {
  const { code } = await params; // 從路由參數中取得產品 ID
  return (
    <ClientProvider>
      <Container>
        <VerifyPage code={code} />
      </Container>
    </ClientProvider>
  );
};

export default UserVerifyPage;
