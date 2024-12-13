from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from controls.backstage.cms import router as backstage_router
from controls.backstage.product_backstage import router as backstage_product_router
from controls.backstage.user_backstage import router as backstage_user_router
from controls.backstage.order_backstage import router as backstage_order_router
from controls.backstage.terms_backstage import router as backstage_term_router
from controls.frontstage.product_frontstage import router as frontstage_product_router
from controls.frontstage.order_frontstage import router as frontstage_order_router
from controls.frontstage.user_frontstage import router as frontstage_user_router
from controls.frontstage.cart_frontstage import router as frontstage_cart_router
from controls.frontstage.terms_frontstage import router as frontstage_term_router


app = FastAPI()

# 設定 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 允許的前端來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有標頭
)

app.include_router(backstage_product_router, prefix="/backstage/v1")
app.include_router(backstage_user_router, prefix="/backstage/v1")
app.include_router(backstage_order_router, prefix="/backstage/v1")
app.include_router(backstage_term_router, prefix="/backstage/v1")
app.include_router(frontstage_product_router, prefix="/frontstage/v1")
app.include_router(frontstage_order_router, prefix="/frontstage/v1")
app.include_router(frontstage_user_router, prefix="/frontstage/v1")
app.include_router(frontstage_cart_router, prefix="/frontstage/v1")
app.include_router(frontstage_term_router, prefix="/frontstage/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)