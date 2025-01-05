from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import StoreSelection


# 新增超商選擇記錄
def create_store_selection(
    db: Session,
    merchant_trade_no: str,
    logistics_sub_type: str,
    cvs_store_id: str,
    cvs_store_name: str,
    cvs_address: str,
):
    try:
        new_selection = StoreSelection(
            merchant_trade_no=merchant_trade_no,
            logistics_sub_type=logistics_sub_type,
            cvs_store_id=cvs_store_id,
            cvs_store_name=cvs_store_name,
            cvs_address=cvs_address,
        )
        db.add(new_selection)
        db.commit()
        db.refresh(new_selection)
        return new_selection
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        return None


# 根據 MerchantTradeNo 查詢超商選擇記錄
def get_store_selection_by_trade_no(db: Session, merchant_trade_no: str):
    try:
        return (
            db.query(StoreSelection)
            .filter(StoreSelection.merchant_trade_no == merchant_trade_no)
            .first()
        )
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        return None
