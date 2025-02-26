import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.reward_setting_crud as reward_setting_db
import modules.shan_thai_token_crud as shan_thai_token_db
from controls.tools import format_to_utc8 as timeformat


# 取消訂單要先恢復庫存
async def cancel_order(oid, db):
    order_details = order_db.get_order_details_by_oid(db, oid)
    for order_detail in order_details:
        product = await product_db.get_product_by_id(db, order_detail.pid)

        if not product:
            return {
                "detail": f"Product ID {order_detail.pid} not found for restocking",
                "data": "",
            }

        # 更新庫存
        update_data = {"remain": product["remain"] + order_detail.productNumber}
        product_updated = await product_db.update_partial_product(
            db, order_detail.pid, update_data
        )
        if not product_updated:
            return {
                "detail": f"Failed to update product remain for Product ID {order_detail.pid}",
                "data": "",
            }

    # 更新訂單狀態成為取消
    update_data = {"status": "已取消"}
    if not update_data:
        return {
            "detail": "No fields to update",
            "data": "",
        }

    updated_order = order_db.update_order(db, oid=oid, updates=update_data)

    if not updated_order:
        return {
            "detail": "Order not found",
            "data": "",
        }
    updated_order.created_at = timeformat(updated_order.created_at.isoformat())
    updated_order.updated_at = timeformat(updated_order.updated_at.isoformat())

    return {
        "detail": "success",
        "data": updated_order,
    }


# 當訂單完成根據訂單金額發送善泰幣
async def order_back_shan_thai_token(db, uid, useDiscount, discountPrice, totalAmount):
    reward_detail = reward_setting_db.get_reward_by_name(db, "order back")
    user_token = shan_thai_token_db.get_token_by_uid(
        db, uid
    )  # 取得用戶目前餘額
    user_token_balance = user_token.balance
    if (
        reward_detail["reward_type"] == "ratio"
    ):  # 如果是比例類型的反饋，則需要根據訂單優惠價
        if useDiscount:  # 確認這筆訂單有沒有優惠價
            order_amount = discountPrice
        else:
            order_amount = totalAmount
        user_token_balance = user_token_balance + round(
            order_amount * reward_detail["reward"] / 100
        )  # 四捨五入到整數
    else:
        user_token_balance = user_token_balance + reward_detail["reward"]
    shan_thai_token_db.update_token_balance(db, uid, user_token_balance)