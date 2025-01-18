import modules.order_crud as order_db
import modules.product_crud as product_db
from controls.tools import format_to_utc8 as timeformat


# 取消訂單要先恢復庫存
async def cancel_order(oid, db):
    order_details = order_db.get_order_details_by_oid(db, oid)
    for order_detail in order_details:
        product = product_db.get_product_by_id(db, order_detail.pid)
        if not product:
            return {
                "detail": f"Product ID {order_detail.pid} not found for restocking",
                "data": "",
            }

        # 更新庫存
        update_data = {"remain": product.remain + order_detail.productNumber}
        product_updated = product_db.update_partial_product(
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
