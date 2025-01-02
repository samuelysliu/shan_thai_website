from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import PaymentCallback

# 寫入 PaymentCallback 紀錄
def create_payment_callback(
    db: Session,
    merchant_id: str,
    merchant_trade_no: str,
    store_id: str,
    rtn_code: int,
    rtn_msg: str,
    trade_no: str,
    trade_amt: int,
    payment_date=None,
    payment_type: str = "",
    payment_type_charge_fee: int = 0,
    platform_id: str = None,
    trade_date=None,
    simulate_paid: int = 1,
    check_mac_value: str = "",
    bank_code: str = None,
    v_account: str = None,
    expire_date=None,
):
    try:
        new_callback = PaymentCallback(
            merchant_id=merchant_id,
            merchant_trade_no=merchant_trade_no,
            store_id=store_id,
            rtn_code=rtn_code,
            rtn_msg=rtn_msg,
            trade_no=trade_no,
            trade_amt=trade_amt,
            payment_date=payment_date,
            payment_type=payment_type,
            payment_type_charge_fee=payment_type_charge_fee,
            platform_id=platform_id,
            trade_date=trade_date,
            simulate_paid=simulate_paid,
            check_mac_value=check_mac_value,
            bank_code=bank_code,
            v_account=v_account,
            expire_date=expire_date,
        )
        db.add(new_callback)
        db.commit()
        db.refresh(new_callback)
        return new_callback
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")
        return None


# 讀取特定 PaymentCallback 紀錄
def get_payment_callback_by_trade_no(db: Session, trade_no: str):
    try:
        return db.query(PaymentCallback).filter(PaymentCallback.trade_no == trade_no).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
