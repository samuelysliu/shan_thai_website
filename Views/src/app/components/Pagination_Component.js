"use client";

import React from 'react';
import { Pagination } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

export default function Pagination_Component() {
  const router = useRouter();

  const handleNavLink = (path) => {
    router.push(path);
  };

  return (
    <Pagination className="justify-content-center my-4">
      <Pagination.Prev onClick={() => handleNavLink('/')} />
      <Pagination.Item onClick={() => handleNavLink('/')}>{1}</Pagination.Item>
      <Pagination.Item onClick={() => handleNavLink('/')}>{2}</Pagination.Item>
      <Pagination.Item onClick={() => handleNavLink('/')}>{3}</Pagination.Item>
      <Pagination.Item onClick={() => handleNavLink('/')}>{4}</Pagination.Item>
      <Pagination.Ellipsis />
      <Pagination.Item onClick={() => handleNavLink('/')}>{50}</Pagination.Item>
      <Pagination.Next onClick={() => handleNavLink('/')} />
    </Pagination>
  );
}
