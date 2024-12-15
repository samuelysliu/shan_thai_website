"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Provider } from "react-redux";
import { store } from "../redux/store";
import Loader from "../components/Loader";
import AlertToast from "../components/Alert_Toast";
import { startLoading, stopLoading } from "../redux/slices/loadingSlice";

export default function ClientWrapper({ children }) {
  const router = useRouter();

  useEffect(() => {
    const handleStart = () => store.dispatch(startLoading());
    const handleComplete = () => store.dispatch(stopLoading());

    router.events.on("routeChangeStart", handleStart);
    router.events.on("routeChangeComplete", handleComplete);
    router.events.on("routeChangeError", handleComplete);

    return () => {
      router.events.off("routeChangeStart", handleStart);
      router.events.off("routeChangeComplete", handleComplete);
      router.events.off("routeChangeError", handleComplete);
    };
  }, [router]);

  return (
    <Provider store={store}>
      <Loader />
      <AlertToast />
      {children}
    </Provider>
  );
}
