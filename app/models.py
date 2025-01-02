from sqlalchemy import Boolean, Column, Integer, String, Double, Date, DateTime
from sqlalchemy.orm import relationship
#1.用Base类来创建 SQLAlchemy 模型
from .database import Base
 
# CREATE TABLE `share_history` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `day` date DEFAULT NULL,
#   `code` varchar(16) DEFAULT NULL,
#   `start` double DEFAULT NULL,
#   `close` double DEFAULT NULL,
#   `high` double DEFAULT NULL,
#   `low` double DEFAULT NULL,
#   `trading_volume` bigint(20) DEFAULT NULL COMMENT '成交量',
#   `trading_value` double DEFAULT NULL COMMENT '成交额',
#   `amplitude` double DEFAULT NULL COMMENT '振幅',
#   `percent` double DEFAULT NULL COMMENT '涨跌幅',
#   `price_diff` double DEFAULT NULL,
#   `turnover_ratio` double DEFAULT NULL COMMENT '换手',
#   `name` varchar(16) DEFAULT NULL,
#   `origin` varchar(4) DEFAULT NULL,
#   `cdate` date DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `idx_code_day` (`code`,`day`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=16235177 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class ShareHistory(Base):
    __tablename__ = "share_history"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date)
    code = Column(String)
    name = Column(String)
    origin = Column(String)
    start = Column(Double)
    close = Column(Double)
    high = Column(Double)
    low = Column(Double)
    trading_volume = Column(Integer)
    trading_value = Column(Double)
    amplitude = Column(Double)
    percent = Column(Double)
    price_diff = Column(Double)
    turnover_ratio = Column(Double)
    cdate = Column(DateTime)
 
# class Item(Base):
#     __tablename__ = "items"
 
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
 
#     owner = relationship("User", back_populates="items"