"use client";

import React from 'react';
import { Pagination } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function PaginationComponent({ totalProducts, productsPerPage, currentPage, onPageChange, type }) {
  const router = useRouter();
  const totalPages = Math.ceil(totalProducts / productsPerPage);

  // 處理分頁跳轉
  const handlePageClick = (page) => {
    onPageChange(page); // 回傳父組件
    if(type !== "backstage")
      router.push(`/?page=${page}`); // 更新網址參數
  };

  // 動態生成頁碼
  const paginationItems = Array.from({ length: totalPages }, (_, index) => {
    const page = index + 1;
    return (
      <Pagination.Item
        key={page}
        active={page === currentPage}
        onClick={() => handlePageClick(page)}
      >
        {page}
      </Pagination.Item>
    );
  });

  return (
    <Pagination className="justify-content-center my-4">
      <Pagination.Prev
        onClick={() => currentPage > 1 && handlePageClick(currentPage - 1)}
        disabled={currentPage === 1}
      />
      {paginationItems}
      <Pagination.Next
        onClick={() => currentPage < totalPages && handlePageClick(currentPage + 1)}
        disabled={currentPage === totalPages}
      />
    </Pagination>
  );
}
