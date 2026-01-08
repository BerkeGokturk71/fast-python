from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.premium import router_premium
from backend.api.server_list import router_server_list
from backend.crud.ip_address_create import init_db_ips
from backend.db.base import Base
from backend.db.session import engine, SessionLocal
from backend.api.auth import router_auth
from backend.api.vpn_conn import router_vpn


@asynccontextmanager
async def lifespan(app: FastAPI):
    #await RedisClient.connect()
    #print("Redis connected")
    Base.metadata.create_all(bind=engine)

    # 1. Uygulama Başlarken (Startup)
    db = SessionLocal()  # Özel bir oturum açıyoruz
    try:
        print("--- Veritabanı Başlatılıyor ---")
        init_db_ips(db)  # Fonksiyonunu burada çağırıyoruz
        print("--- IP Havuzu Kontrolü Tamamlandı ---")
    except Exception as e:
        print(f"Başlangıç hatası: {e}")
    finally:
        db.close()  # İşimiz bitince bu özel oturumu kapatıyoruz

    yield  # Uygulama burada çalışmaya başlar (Requestleri dinler)
    #await RedisClient.close()
    #print("Redis closed")
    # 2. Uygulama Kapanırken (Shutdown)
    print("Uygulama kapatılıyor...")
app = FastAPI(title="Wireguard",lifespan=lifespan)

app.include_router(router=router_auth)
app.include_router(router=router_vpn)
app.include_router(router=router_server_list)
app.include_router(router=router_premium)