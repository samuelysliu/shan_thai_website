from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from modules.dbInit import LogisticsOrder


# 新增物流記錄
def create_logistics_order(
    db: Session,
    merchant_trade_no: str,
    rtn_code: int,
    allpay_logistics_id: str,
    rtn_msg: str = None,
    logistics_type: str = None,
    logistics_sub_type: str = None,
    goods_amount: int = None,
    update_status_date: datetime = None,
    receiver_name: str = None,
    receiver_cell_phone: str = None,
    receiver_email: str = None,
    receiver_address: str = None,
    cvs_payment_no: str = None,
    cvs_validation_no: str = None,
    booking_note: str = None,
):
    try:
        new_logistics_order = LogisticsOrder(
            merchant_trade_no=merchant_trade_no,
            rtn_code=rtn_code,
            rtn_msg=rtn_msg,
            allpay_logistics_id=allpay_logistics_id,
            logistics_type=logistics_type,
            logistics_sub_type=logistics_sub_type,
            goods_amount=goods_amount,
            update_status_date=update_status_date,
            receiver_name=receiver_name,
            receiver_cell_phone=receiver_cell_phone,
            receiver_email=receiver_email,
            receiver_address=receiver_address,
            cvs_payment_no=cvs_payment_no,
            cvs_validation_no=cvs_validation_no,
            booking_note=booking_note,
        )
        db.add(new_logistics_order)
        db.commit()
        db.refresh(new_logistics_order)
        return new_logistics_order
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        return None


# 更新物流記錄
def update_logistics_order_by_trade_no(
    db: Session, merchant_trade_no: str, updates: dict
):
    try:
        logistics_order = (
            db.query(LogisticsOrder)
            .filter(LogisticsOrder.merchant_trade_no == merchant_trade_no)
            .first()
        )

        if not logistics_order:
            return None

        for key, value in updates.items():
            if hasattr(logistics_order, key):
                setattr(logistics_order, key, value)

        db.commit()
        db.refresh(logistics_order)
        return logistics_order
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        return None


# 查詢物流記錄
def get_logistics_order_by_trade_no(db: Session, merchant_trade_no: str):
    try:
        return (
            db.query(LogisticsOrder)
            .filter(LogisticsOrder.merchant_trade_no == merchant_trade_no)
            .first()
        )
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        return None
