"use client";

import React, { useEffect } from "react";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { store, persistor } from "../redux/store";
import Loader from "./Loader";
import { useRouter } from "next/navigation";
import { startLoading, stopLoading } from "../redux/slices/loadingSlice";
import AlertToast from "./Alert_Toast";

const ClientProvider = ({ children }) => {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChangeStart = () => startLoading();
    const handleRouteChangeComplete = () => stopLoading();

    handleRouteChangeStart(); // 當路由開始更改
    handleRouteChangeComplete(); // 當路由完成更改

    return () => {
      handleRouteChangeComplete();
    };
  }, [router]);


  return (
    <Provider store={store}>
      <Loader />
      <AlertToast />
      <PersistGate loading={null} persistor={persistor}>
        {children}
      </PersistGate>
    </Provider>
  );
};

export default ClientProvider;
