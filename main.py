from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from controls.backstage.product_backstage import router as backstage_product_router
from controls.backstage.user_backstage import router as backstage_user_router
from controls.backstage.order_backstage import router as backstage_order_router
from controls.backstage.terms_backstage import router as backstage_term_router
from controls.backstage.token_backstage import router as backstage_token_router
from controls.backstage.reward_setting_backstage import router as backstage_reward_router
from controls.frontstage.product_frontstage import router as frontstage_product_router
from controls.frontstage.order_frontstage import router as frontstage_order_router
from controls.frontstage.user_frontstage import router as frontstage_user_router
from controls.frontstage.cart_frontstage import router as frontstage_cart_router
from controls.frontstage.terms_frontstage import router as frontstage_term_router
from controls.frontstage.token_frontstage import router as frontstage_token_router
from controls.cash_flow import check_order
from controls.logistic import check_logistic_status
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()
environment = os.getenv("ENVIRONMENT")

if environment == "uat":
    domain = "https://shan-thai-website.vercel.app"
elif environment == "production":
    domain = "https://www.shan-thai-team.com"
else:
    domain = "*"


# 設定 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=[domain],  # 允許的前端來源
    allow_credentials=True,
    allow_methods=["*"],  # 限制 HTTP 方法
    allow_headers=["*"],  # 明確指定允許的標頭
)

app.include_router(backstage_product_router, prefix="/backstage/v1")
app.include_router(backstage_user_router, prefix="/backstage/v1")
app.include_router(backstage_order_router, prefix="/backstage/v1")
app.include_router(backstage_term_router, prefix="/backstage/v1")
app.include_router(backstage_token_router, prefix="/backstage/v1")
app.include_router(backstage_reward_router, prefix="/backstage/v1")
app.include_router(frontstage_product_router, prefix="/frontstage/v1")
app.include_router(frontstage_order_router, prefix="/frontstage/v1")
app.include_router(frontstage_user_router, prefix="/frontstage/v1")
app.include_router(frontstage_cart_router, prefix="/frontstage/v1")
app.include_router(frontstage_term_router, prefix="/frontstage/v1")
app.include_router(frontstage_token_router, prefix="/frontstage/v1")

@app.get("/")
async def health_check():
    return {"status": "ok"}


def check_cashflow_order_scheduler():
    print("check_cashflow_order start")
    check_order()
    print("check_cashflow_order end")
    
def check_logisitic_order_scheduler():
    print("check_logistic_status start")
    check_logistic_status()
    print("check_logistic_status end")


if environment == "production":
    # 初始化排程器
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_cashflow_order_scheduler, "interval", minutes=360)
    scheduler.add_job(check_logisitic_order_scheduler, "interval", minutes=60)
    scheduler.start()

"""
# 轉移圖片程式
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.dbConnect import Base, engine  # 確保這裡引入了正確的 Base 和 engine
from modules.dbInit import Product, ProductImage  # 確保這裡引入了 Product 和 ProductImage 模型

# 創建資料庫會話
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def migrate_product_images():
    try:
        # 獲取所有產品
        products = session.query(Product).all()

        for product in products:
            # 獲取產品的圖片 URL
            if product.productImageUrl:
                # 假設 productImageUrl 是一個以逗號分隔的字符串，將其分割成列表
                image_urls = product.productImageUrl.split(',')
                
                for url in image_urls:
                    # 創建新的 ProductImage 實例
                    product_image = ProductImage(pid=product.pid, image_url=url.strip())
                    session.add(product_image)

        # 提交事務
        session.commit()
        print("圖片遷移完成！")
    except Exception as e:
        print(f"發生錯誤：{e}")
        session.rollback()  # 如果發生錯誤，回滾事務
    finally:
        session.close()  # 關閉會話
migrate_product_images()
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
