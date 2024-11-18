"use client";

import React from "react";
import Cart from "@/app/components/Cart";
import { Provider } from "react-redux";
import { store } from "@/app/redux/store";

export default function CartPage() {
    return (
        <Provider store={store}>
            <Cart />
        </Provider>
    );
}
