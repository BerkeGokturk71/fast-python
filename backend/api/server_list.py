from fastapi import APIRouter,Depends,status
from fastapi.security import OAuth2PasswordBearer
from backend.db.session import get_db
from backend.models.users import  ServerList

from sqlalchemy.orm import Session
router_server_list = APIRouter(prefix="/server_list", tags=["VPN ServerList"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router_server_list.get(path="/status")
def server_list( db:Session = Depends(get_db)):
    servers = db.query(ServerList).all()
    result_data = []

    for server in servers:
        result_data.append({
            "id":server.id,
            "server_name": server.server_name,
            "is_premium": server.is_premium,
            # Eğer veritabanında bu alan boşsa hata vermesin, varsayılan "TR" yazsın
            "server_country": server.server_country if server.server_country else "TR"
        })

    # 3. Listeyi dön (FastAPI bunu otomatik JSON yapar)
    return result_data
