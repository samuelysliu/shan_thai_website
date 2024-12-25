"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Container, Alert } from "react-bootstrap";
import axios from "axios";
import config from "@/app/config";

const VerifyPage = ({ code }) => {
    console.log(code)
    const endpoint = config.apiBaseUrl;

    const router = useRouter();
    const [status, setStatus] = useState(null); // 成功或失敗的狀態
    const [message, setMessage] = useState(""); // 提示訊息

    const hasFetched = useRef(false);

    // 提取驗證碼並進行驗證
    const verifyCode = async () => {
        try {
            const response = await axios.get(`${endpoint}/frontstage/v1/verify/${code}`);
            if (response.detail === "User registered successfully") {
                setStatus("success");
                setMessage("驗證成功！即將跳轉至首頁...");
            } else {
                setStatus("danger");
                setMessage("驗證碼已過期或無效！即將跳轉至首頁...");
            }
        } catch (error) {
            setStatus("danger");
            setMessage("驗證碼已過期或無效！即將跳轉至首頁...");
        } finally {
            // 3 秒後跳轉回首頁
            setTimeout(() => {
                router.push("/");
            }, 3000);
        }
    };

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
        verifyCode();
    }, [code, router]);

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
            {status && (
                <Alert variant={status} className="text-center">
                    {message}
                </Alert>
            )}
        </Container>
    );
};

export default VerifyPage;
