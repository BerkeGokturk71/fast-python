import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.db.base import Base  # Senin base dosyanın yolu


class Users(Base):
    __tablename__ = "users"

    # Sadece ID Primary Key olmalı
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Diğerleri benzersiz (Unique) olmalı
    username = Column(String, nullable=False, unique=True, index=True)
    mail = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_premium = Column(Boolean,nullable=True,default=False)
    # Public Key
    public_key = Column(String, nullable=True)
    # İlişkiler
    tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")

    # uselist=False -> Bire-Bir ilişki (Bir kullanıcının bir IP'si olur)
    vpn_ip = relationship("IpPool", back_populates="user", uselist=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    refresh_token = Column(String, nullable=True, unique=True)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    device_name = Column(String, nullable=True)

    # back_populates, Users tablosundaki değişken adıyla ("tokens") aynı değilse hata alırsın,
    # ama burada Users tarafında "tokens" demiştik, o yüzden buraya "user" diyelim ki karışmasın.
    user = relationship("Users", back_populates="tokens")


class IpPool(Base):
    __tablename__ = "ip_pool"

    id = Column(Integer, primary_key=True, index=True)

    # IP adresini String tutmak (Örn: "10.0.0.5") kullanımı kolaylaştırır.
    # unique=True yaptık ki aynı IP iki kere havuza girmesin.
    ip_address = Column(String, nullable=False,  index=True)

    is_available = Column(Boolean, default=True, index=True)

    # Hangi kullanıcıya atandı?
    user_id = Column(String, ForeignKey("users.id"), nullable=True, unique=True)

    # İlişki: Users tablosundaki değişken adı "vpn_ip" olduğu için burası da user'a gitmeli
    user = relationship("Users", back_populates="vpn_ip")
    server_id = Column(Integer,ForeignKey("server_list.id"),nullable=False)

    server = relationship("ServerList",back_populates="ips")
class ServerList(Base):
    __tablename__ = "server_list"
    id = Column(Integer,primary_key=True,index=True)
    server_name = Column(String,nullable=False,index=True)
    is_premium = Column(Boolean,nullable=False,default=False)
    server_country = Column(String, nullable=True, default="TR")
    public_key = Column(String,nullable=False)
    ip_address = Column(String,nullable=False)
    ips = relationship("IpPool",back_populates="server",cascade="all,delete")