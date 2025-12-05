// src/app/lib/seo-helpers.js

/**
 * 生成產品的結構化數據 (JSON-LD)
 */
export const generateProductSchema = (product) => {
  const imageArray = Array.isArray(product.productImageUrl) 
    ? product.productImageUrl 
    : [product.productImageUrl || ""];

  return {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": product.title_cn,
    "description": product.content_cn ? product.content_cn.replace(/<[^>]*>/g, '').substring(0, 160) : "南傳聖物",
    "image": imageArray,
    "brand": {
      "@type": "Brand",
      "name": "善泰團隊"
    },
    "offers": {
      "@type": "Offer",
      "url": `https://www.shan-thai-team.com/product/${product.pid}`,
      "priceCurrency": "TWD",
      "price": product.price.toString(),
      "availability": product.remain > 0 
        ? "https://schema.org/InStock" 
        : "https://schema.org/OutOfStock",
      "seller": {
        "@type": "Organization",
        "name": "善泰團隊"
      }
    },
    "aggregateRating": product.rating ? {
      "@type": "AggregateRating",
      "ratingValue": product.rating.value,
      "reviewCount": product.rating.count
    } : undefined
  };
};

/**
 * 生成麵包屑導航結構化數據
 */
export const generateBreadcrumbSchema = (items) => {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": items.map((item, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "name": item.name,
      "item": item.url
    }))
  };
};

/**
 * 生成常見問題結構化數據
 */
export const generateFAQSchema = (faqs) => {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(faq => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };
};
