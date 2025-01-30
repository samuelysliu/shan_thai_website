"use client";

import React from "react";
import { Container, Accordion } from "react-bootstrap";

const FAQ = () => {
  // FAQ 數據，可以根據需要自行更改
  const faqData = [
    {
      question: "Q: 可以使用哪種付款方式",
      answer: "A: 可以選擇貨到付款、信用卡以及轉帳。如果是宅配，則不能貨到付款。"
    },
    {
      question: "Q: 我忘記了密碼該怎麼辦？",
      answer: "A: 您可以點擊“忘記密碼”鏈接，並按照步驟重置您的密碼。"
    },
    {
      question: "Q: 訂單完成後多久可以收到貨品？",
      answer: "A: 通常情況下，訂單在 7 個工作日內可以送達，具體時間取決於您的地點和運輸方式。"
    }
    // 可根據需求添加更多的 FAQ 條目
  ];

  return (
    <Container className="my-4">
      <h2 className="text-center mb-4">常見問題</h2>
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
