"use client";

import React from "react";
import { Container, Accordion } from "react-bootstrap";

const FAQ = () => {
  // FAQ 數據，可以根據需要自行更改
  const faqData = [
    {
      question: "Q: 我如何創建帳號？",
      answer: "A: 您可以通過點擊首頁右上角的“註冊”按鈕來創建帳號。"
    },
    {
      question: "Q: 我忘記了密碼該怎麼辦？",
      answer: "A: 您可以點擊“忘記密碼”鏈接，並按照步驟重置您的密碼。"
    },
    {
      question: "Q: 訂單完成後多久可以收到貨品？",
      answer: "A: 通常情況下，訂單在2-5個工作日內可以送達，具體時間取決於您的地點和運輸方式。"
    }
    // 可根據需求添加更多的 FAQ 條目
  ];

  return (
    <Container className="my-4">
      <h2 className="text-center mb-4">常見問題 FAQ</h2>
      <Accordion defaultActiveKey="0">
        {faqData.map((item, index) => (
          <Accordion.Item eventKey={index.toString()} key={index}>
            <Accordion.Header>{item.question}</Accordion.Header>
            <Accordion.Body>{item.answer}</Accordion.Body>
          </Accordion.Item>
        ))}
      </Accordion>
    </Container>
  );
};

export default FAQ;
