from controls.cash_flow import check_order
from controls.logistic import check_logistic_status
import asyncio

def check_cashflow_order_scheduler():
    print("check_cashflow_order start")
    check_order()
    print("check_cashflow_order end")
    
async def check_logisitic_order_scheduler():
    print("check_logistic_status start")
    await check_logistic_status()
    print("check_logistic_status end")
    
asyncio.run(check_logisitic_order_scheduler())
check_cashflow_order_scheduler()