from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import modules.product_crud as product_db
import modules.dbConnect as db_connect
from fastapi.responses import Response
from datetime import datetime
router = APIRouter()
get_db = db_connect.get_db
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=128, ttl=600)  # 快取 600 秒 (10 分鐘)

# 取得所有上架產品的資訊
@router.get("/product")
async def get_all_product(db: Session = Depends(get_db)):
    products = product_db.get_product_launch(db)
    
    if products is None:
        print(
            "System Log: product_frontstage get_all_product function database query failed"
        )
        raise HTTPException(status_code=500, detail="Database query failed")
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    # 不含圖片
    formatted_products = [
        {
            "pid": product.pid,
            "ptid": product.ptid,
            "title_cn": product.title_cn,
            "title_en": product.title_en,
            "content_cn": product.content_cn,
            "content_en": product.content_en,
            "price": product.price,
            "specialPrice": product.specialPrice,
            "remain": product.remain,
            "sold": product.sold,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }
        for product in products
    ]
    return formatted_products


# 取得指定產品的所有圖片
@router.get("/product_images/{pid}")
async def get_product_images(pid: int, db: Session = Depends(get_db)):
    if pid in cache:
        return cache[pid]
    
    products = product_db.get_product_image_by_id(db, pid)

    product_list = [product.image_url for product in products]

    if products is None:
        print(
            "System Log: product_frontstage get_product_images function database query failed"
        )
        raise HTTPException(status_code=500, detail="Database query failed")

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    cache[pid] = {"pid": pid, "productImages": product_list}
    
    return {"pid": pid, "productImages": product_list}


# 取得特定產品詳情
@router.get("/product_by_pid/{pid}")
async def get_product_by_pid(pid: int, db: Session = Depends(get_db)):
    product = await product_db.get_product_by_id(db, pid)
    if product is None:
        print(
            "System Log: product_frontstage get_product_by_pid function database query failed"
        )
        raise HTTPException(status_code=500, detail="Database query failed")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 取得所有標籤類別底下的產品
@router.get("/product_by_tag/{ptid}")
async def get_products_by_tag(ptid: int, db: Session = Depends(get_db)):
    if ptid == -1:
        products = product_db.get_product_launch(db)
    else:
        product_list = product_db.get_products_by_tag(db, ptid)
        products = []
        for i in product_list:
            if i["launch"]:
                products.append(i)

    if products is None:
        print(
            "System Log: product_frontstage get_products_by_tag function database query failed"
        )
        raise HTTPException(status_code=500, detail="Database query failed")
    if not products:
        return []

    # 不含圖片
    formatted_products = [
        {
            "pid": product["pid"],
            "ptid": product["ptid"],
            "title_cn": product["title_cn"],
            "title_en": product["title_en"],
            "content_cn": product["content_cn"],
            "content_en": product["content_en"],
            "price": product["price"],
            "specialPrice": product["specialPrice"],
            "remain": product["remain"],
            "sold": product["sold"],
            "created_at": product["created_at"],
            "updated_at": product["updated_at"],
        }
        for product in products
    ]

    return formatted_products


# 取得所有標籤
@router.get("/product_tag")
async def get_product_tag(db: Session = Depends(get_db)):
    product_tags = product_db.get_all_product_tags(db)

    if product_tags is None:
        print(
            "System Log: product_frontstage get_product_tag function database query failed"
        )
        raise HTTPException(status_code=500, detail="Database query failed")

    if not product_tags:
        print("Product tag not found")
        return []
    return product_tags


# 生成產品Sitemap用於SEO
@router.get("/sitemap-products.xml")
async def get_products_sitemap(db: Session = Depends(get_db)):
    """
    生成所有產品的Sitemap XML
    用於Google Search Console爬蟲發現所有商品頁面
    """
    try:
        products = product_db.get_product_launch(db)
        
        if not products:
            products = []
        
        # 生成XML
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for product in products:
            updated_at = product.get("updated_at", datetime.now())
            if isinstance(updated_at, datetime):
                updated_at_str = updated_at.strftime("%Y-%m-%d")
            else:
                updated_at_str = updated_at
            
            sitemap_xml += '  <url>\n'
            sitemap_xml += f'    <loc>https://www.shan-thai-team.com/product/{product["pid"]}</loc>\n'
            sitemap_xml += f'    <lastmod>{updated_at_str}</lastmod>\n'
            sitemap_xml += '    <changefreq>weekly</changefreq>\n'
            sitemap_xml += '    <priority>0.8</priority>\n'
            sitemap_xml += '  </url>\n'
        
        sitemap_xml += '</urlset>'
        
        return Response(content=sitemap_xml, media_type="application/xml")
    
    except Exception as e:
        print(f"Error generating product sitemap: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate sitemap")
