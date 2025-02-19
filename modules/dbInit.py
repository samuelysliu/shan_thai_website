from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship
from modules.dbConnect import engine, Base
from sqlalchemy.sql import func

class Banner(Base):
    __tablename__ = "banner"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    buttonText_cn = Column(String(255))
    buttonText_en = Column(String(255))
    buttonLink = Column(String)
    bannerImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(Text)
    content_en = Column(Text)
    aboutImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    title_cn = Column(String(255))
    title_en = Column(String(255))
    teamImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    address_cn = Column(String(255))
    address_en = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class ExternalLink(Base):
    __tablename__ = "external_link"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    iconImageUrl = Column(String)
    show = Column(Boolean)
    externalLink = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Product(Base):
    __tablename__ = "product"

    pid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ptid = Column(Integer, ForeignKey("product_tag.ptid"))
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(Text)
    content_en = Column(Text)
    price = Column(Integer, default=0)
    specialPrice = Column(Integer, default=None, nullable=True)
    remain = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    productImageUrl = Column(String)
    launch = Column(Boolean, default=True)
    isDelete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    #orders = relationship("Order", back_populates="product")
    order_details = relationship("OrderDetail", back_populates="product")  # 新增關聯
    carts = relationship("Cart", back_populates="product")
    product_tag = relationship("ProductTag", back_populates="product")
    
    # 新增與 ProductImage 的關聯
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    
class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)
    image_url = Column(String, nullable=False)

    # 關聯到 Product
    product = relationship("Product", back_populates="images")


    
class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    sex = Column(String(255), nullable=True)
    star = Column(Integer, default=0)
    identity = Column(String(255), nullable=True)
    note =Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)  # 新增出生年月日欄位
    mbti = Column(String(4), nullable=True)  # 新增 MBTI 欄位
    phone = Column(String(20), nullable=True)  # 新增聯絡電話欄位
    address = Column(Text, nullable=True)  # 新增常用地址欄位
    referral_code = Column(String(20), unique=True, nullable=True)  # 推薦碼欄位
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    carts = relationship("Cart", back_populates="users")
    orders = relationship("Order", back_populates="users")
    user_verifications = relationship("UserVerify", back_populates="user")  # 新增與 UserVerify 的關聯
    shan_thai_tokens = relationship("ShanThaiToken", back_populates="user", cascade="all, delete-orphan")
    
    referrals_as_referrer = relationship(
        "UserReferral", foreign_keys="[UserReferral.referrer_uid]", back_populates="referrer", cascade="all, delete-orphan"
    )
    referrals_as_referred = relationship(
        "UserReferral", foreign_keys="[UserReferral.referred_uid]", back_populates="referred", cascade="all, delete-orphan"
    )


class UserVerify(Base):
    __tablename__ = "user_verify"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)  # 與 User 表格關聯
    verification_code = Column(String(10), nullable=False)  # 驗證碼
    expires_at = Column(DateTime, nullable=False)  # 驗證碼過期時間
    created_at = Column(DateTime, default=func.now())  # 建立時間

    # 建立與 User 的反向關聯
    user = relationship("User", back_populates="user_verifications")
    
# 用戶關聯表
class UserReferral(Base):
    __tablename__ = "user_referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referrer_uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    referred_uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    # 關聯到 User
    referrer = relationship("User", foreign_keys=[referrer_uid], back_populates="referrals_as_referrer")
    referred = relationship("User", foreign_keys=[referred_uid], back_populates="referrals_as_referred")

    

class ShanThaiToken(Base):
    __tablename__ = "shan_thai_token"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)  # 關聯用戶表
    balance = Column(Integer, default=0, nullable=False)  # 用戶紅利點數餘額
    created_at = Column(DateTime, default=func.now())  # 建立時間
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 更新時間

    # 建立與 User 的反向關聯
    user = relationship("User", back_populates="shan_thai_tokens")

class Order(Base):
    __tablename__ = "orders"
    
    oid = Column(String(10), primary_key=True)  # 訂單 ID
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)  # 用戶 ID
    totalAmount = Column(Integer, default=0)  # 訂單總金額
    discountPrice = Column(Integer, default=0)  # 訂單優惠價
    useDiscount = Column(Boolean, default=False) # 是否使用優惠價
    zipCode = Column(String(10), nullable=True)
    address = Column(String, nullable=False)  # 收貨地址
    recipientName = Column(String, nullable=False)  # 收件人姓名
    recipientPhone = Column(String(15), nullable=False)  # 收件人電話
    recipientEmail = Column(String, nullable=False)  # 收件人 Email
    orderNote = Column(String, nullable=True)  # 訂單備註
    transportationMethod = Column(String(50))  # 運輸方式
    paymentMethod = Column(String(50), nullable=False, default="匯款")  # 付款方式
    status = Column(String(50))  # 訂單狀態
    created_at = Column(DateTime, default=func.now())  # 訂單建立時間
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 訂單更新時間

    # 關聯其他資料庫
    users = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")  # 關聯訂單明細表
    payment_callbacks = relationship("PaymentCallback", back_populates="order", cascade="all, delete-orphan")
    logistics_orders = relationship("LogisticsOrder", back_populates="order", cascade="all, delete-orphan")  # 關聯物流訂單
    
class OrderDetail(Base):
    __tablename__ = "order_details"
    
    odid = Column(Integer, primary_key=True, autoincrement=True)  # 訂單明細 ID
    oid = Column(String(10), ForeignKey("orders.oid"), nullable=False)  # 訂單 ID
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)  # 商品 ID
    productNumber = Column(Integer, default=1)  # 商品數量
    price = Column(Integer, nullable=False)  # 單價（記錄當前價格，避免後續商品價格變更影響訂單）
    subtotal = Column(Integer, nullable=False)  # 小計金額
    
    # 關聯其他資料庫
    order = relationship("Order", back_populates="order_details")  # 關聯訂單主表
    product = relationship("Product", back_populates="order_details")  # 關聯商品表

class PaymentCallback(Base):
    __tablename__ = "payment_callbacks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵，自增 ID
    merchant_id = Column(String(50), nullable=True)  # 特店編號
    merchant_trade_no = Column(String(10), ForeignKey("orders.oid", ondelete="CASCADE"), nullable=False)  # 特店交易編號
    store_id = Column(String(50), nullable=True)  # 特店旗下店舖代號
    rtn_code = Column(Integer, nullable=True)  # 交易狀態
    rtn_msg = Column(String(255), nullable=True)  # 交易訊息
    trade_no = Column(String(50), nullable=False)  # 綠界交易編號
    trade_amt = Column(Integer, nullable=True)  # 交易金額
    payment_date = Column(DateTime, nullable=True)  # 付款時間
    payment_type = Column(String(50), nullable=True)  # 付款方式
    payment_type_charge_fee = Column(Integer, default=0)  # 交易手續費
    platform_id = Column(String(50), nullable=True)  # 特約合作平台商代號
    trade_date = Column(DateTime, nullable=True)  # 訂單成立時間
    simulate_paid = Column(Integer, default=1)  # 是否模擬付款
    check_mac_value = Column(String(255), nullable=True)  # 檢查碼
    bank_code = Column(String(50), nullable=True)  # 繳費銀行代碼
    v_account = Column(String(50), nullable=True)  # 繳費虛擬帳號
    expire_date = Column(DateTime, nullable=True)  # 繳費期限
    created_at = Column(DateTime, default=func.now())  # 記錄建立時間
    
    order = relationship("Order", back_populates="payment_callbacks")

# 物流單DB
class LogisticsOrder(Base):
    __tablename__ = "logistics_orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵
    merchant_trade_no = Column(String(20), ForeignKey("orders.oid", ondelete="CASCADE"), nullable=False)  # 對應訂單號碼
    rtn_code = Column(Integer, nullable=False)  # 物流狀態
    rtn_msg = Column(Text, nullable=True)  # 物流狀態說明
    allpay_logistics_id = Column(String(50), nullable=False)  # 綠界物流交易編號
    logistics_type = Column(String(20), nullable=True)  # 物流類型
    logistics_sub_type = Column(String(20), nullable=True)  # 物流子類型
    goods_amount = Column(Integer, nullable=True)  # 商品金額
    update_status_date = Column(DateTime, nullable=True)  # 物流狀態更新時間
    receiver_name = Column(String(50), nullable=True)  # 收件人姓名
    receiver_cell_phone = Column(String(20), nullable=True)  # 收件人手機
    receiver_email = Column(String(100), nullable=True)  # 收件人 Email
    receiver_address = Column(String(255), nullable=True)  # 收件人地址
    cvs_payment_no = Column(String(50), nullable=True)  # 寄貨編號
    cvs_validation_no = Column(String(50), nullable=True)  # 驗證碼
    booking_note = Column(String(100), nullable=True)  # 托運單號
    created_at = Column(DateTime, default=func.now(), nullable=False)  # 記錄建立時間

    # 與訂單的關聯
    order = relationship("Order", back_populates="logistics_orders")

class Term(Base):
    __tablename__ = "terms"

    tid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    version = Column(String(50), nullable=False)  # 版本名稱
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    added_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)  # 是否有效
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    users = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")

class ProductTag(Base):
    __tablename__ = "product_tag"

    ptid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    productTag = Column(String(255), nullable=False)
    
    # 關聯其他資料庫
    product = relationship("Product", back_populates="product_tag")
    
class StoreSelection(Base):
    __tablename__ = "store_selection"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自增 ID
    merchant_trade_no = Column(String(50), unique=True, nullable=False)  # 唯一碼
    logistics_sub_type = Column(String(50), nullable=False)  # 物流子類型
    cvs_store_id = Column(String(50), nullable=False)  # 超商店舖編號
    cvs_store_name = Column(String(255), nullable=False)  # 超商店舖名稱
    cvs_address = Column(String(255), nullable=False)  # 超商店舖地址
    created_at = Column(DateTime, default=func.now())  # 記錄建立時間

# 記錄各項獎勵的Table
class RewardSetting(Base):
    __tablename__ = "reward_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵，自增 ID
    name = Column(String(255), nullable=False)  # 獎勵名稱，必填
    description = Column(Text, nullable=True)  # 獎勵說明，可選填
    reward_type = Column(String(255), nullable=True)  # 獎勵方式，可選填
    reward = Column(Integer, nullable=True, default=0)  # 善泰幣獎勵數量，可選填，預設為 0
    created_at = Column(DateTime, default=func.now(), nullable=False)  # 建立時間
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # 更新時間

#Base.metadata.create_all(bind=engine)