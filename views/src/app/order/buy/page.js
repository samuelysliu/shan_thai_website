"use client";

import React from "react";
import ClientProvider from "@/app/components/Client_Provider";
import OrderConfirm from "@/app/components/order_components/Order_Confirm";
import { Container } from "react-bootstrap";
import NavBar from "@/app/components/Navbar";
import { useSearchParams } from "next/navigation";

const BuyPage = () => {
  const searchParams = useSearchParams();
  const cvsStoreName = searchParams.get("name"); 
  const cvsStoreId = searchParams.get("id");
  const logitsticSubType = searchParams.get("type");
  let transportationMethodUrl = "";

  if(logitsticSubType === "UNIMARTC2C")
    transportationMethodUrl = "seven";
  else if(logitsticSubType === "FAMIC2C")
    transportationMethodUrl = "family";

  return (
    <ClientProvider>
      <NavBar />
      <Container>
        <OrderConfirm cvsStoreName={cvsStoreName} cvsStoreId={cvsStoreId} transportationMethodUrl={transportationMethodUrl} />
      </Container>

    </ClientProvider>
  );
};

export default BuyPage;
