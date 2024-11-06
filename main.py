from fastapi import FastAPI, HTTPException, APIRouter
import uvicorn
from Controls.backstage.cms import router as backstage_router
from Controls.frontstage.index import router as frontstage_router


app = FastAPI()

app.include_router(backstage_router, prefix="/backstage")
app.include_router(frontstage_router, prefix="/frontstage")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)