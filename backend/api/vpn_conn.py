from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from backend.db.session import get_db
from backend.app.core.security import verify_access_token
from backend.models.users import IpPool, Users, ServerList
from backend.schemas.user_schema import VpnRegister, VpnConfigResponse
from backend.wireguard.wireguard_manager import WireGuardSSHManager
from sqlalchemy.orm import Session

router_vpn = APIRouter(prefix="/vpn", tags=["VPN Connection"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router_vpn.post(path="/connect", response_model=VpnConfigResponse)
def connect(server: VpnRegister, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print(token)

    token_data = verify_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz veya süresi dolmuş."
        )
    user_identifier = token_data

    user = db.query(Users).filter(Users.username == user_identifier).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    target_server = db.query(ServerList).filter(ServerList.server_name == server.server_name).first()
    if not target_server:
        raise HTTPException(status_code=404, detail="İstenen sunucu bulunamadı.")
    try:
        available_ip = db.query(IpPool).filter(IpPool.is_available==True,IpPool.server_id == target_server.id).with_for_update(skip_locked=True).first()
        if not available_ip:
            raise HTTPException(status_code=503, detail="IP Havuzu dolu! Boş IP kalmadı.")
        user.public_key = server.public_key
        user.vpn_ip = available_ip
        available_ip.is_available = False
        available_ip.user_id = user.id

        ssh_key_filename = f"{target_server.server_country}.pem"

        wg_manager = WireGuardSSHManager(target_server.ip_address,ssh_key_filename)
        success = wg_manager.add_peer(client_ip_adress=f"{available_ip.ip_address}/32",client_public_key=server.public_key)

        if not success:
            raise HTTPException(status_code=500, detail="VPN Sunucusuna erişilemedi.")
        print(success)
        db.commit()
        return VpnConfigResponse(
            status = "success",
            assigned_ip = available_ip.ip_address,
            server_public_key = target_server.public_key,
            endpoint = f"{target_server.ip_address}:51820",
            allowed_ips = "0.0.0.0/0"
        )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router_vpn.post("/disconnect")
def disconnect(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # --- 1. KULLANICIYI BUL (Auth) ---
    token_data = verify_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz veya süresi dolmuş."
        )

    user_identifier = token_data
    user = db.query(Users).filter(Users.username == user_identifier).first()

    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    # --- 2. BAĞLANTI KONTROLÜ ---
    # Kullanıcının üzerinde bir IP yoksa zaten bağlı değildir.
    if not user.vpn_ip:
        return {"status": "info", "message": "Zaten bağlı değilsiniz."}

    try:
        # --- 3. HEDEF SUNUCUYU BULMA (DÜZELTİLEN KISIM) ---
        # Kullanıcının sahip olduğu IP objesini alıyoruz
        ip_record = user.vpn_ip

        # Bu IP hangi sunucuya ait? IpPool tablosundaki server_id'den sunucuyu buluyoruz.
        target_server = db.query(ServerList).filter(ServerList.id == ip_record.server_id).first()

        if not target_server:
            # Veri bütünlüğü hatası (IP var ama Sunucu silinmiş vs.)
            # Yine de DB'den IP'yi boşa çıkaralım ki kullanıcı takılı kalmasın
            ip_record.is_available = True
            ip_record.user_id = None
            db.commit()
            raise HTTPException(status_code=404,
                                detail="IP'nin bağlı olduğu sunucu bulunamadı, ancak yerel kaydınız temizlendi.")

        ssh_key_filename = f"{target_server.server_country}.pem"

        # --- 4. WIREGUARD'DAN SİLME (SSH) ---
        wg_manager = WireGuardSSHManager(target_server.ip_address, ssh_key_filename)

        # Kullanıcının public_key'i varsa sunucudan siliyoruz
        if user.public_key:
            # remove_peer fonksiyonun boolean (True/False) döndüğünü varsayıyorum
            ssh_result = wg_manager.remove_peer(user.public_key)
            if not ssh_result:
                print("Uyarı: Sunucudan silinemedi veya zaten silinmişti.")

        # --- 5. VERİTABANI TEMİZLİĞİ (IP İade) ---
        ip_record.is_available = True  # IP artık boş ve başkası alabilir
        ip_record.user_id = None  # IP ile kullanıcı bağını kopar

        # İsteğe bağlı: Kullanıcının public keyini de sıfırlayabilirsin
        # user.public_key = None

        db.commit()

        return {"status": "success", "message": "Bağlantı başarıyla kesildi."}

    except Exception as e:
        db.rollback()
        print(f"Disconnect Hatası: {e}")
        raise HTTPException(status_code=500, detail="Bağlantı kesilirken bir hata oluştu.")