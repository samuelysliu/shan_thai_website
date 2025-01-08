"use client";

import React, { useEffect } from "react";

const ClosePage = () => {
    useEffect(() => {
        if (typeof window !== "undefined") {
            window.close();
        }
    }, []);
    return (
        <></>
    );
};

export default ClosePage;
