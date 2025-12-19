import ipaddress
from sqlalchemy.orm import Session
# Modellerini import et (ServerList'i de ekledik)
from backend.models.users import IpPool, ServerList


def init_db_ips(session: Session):
    """
    Veritabanına Server ve o Server'a ait IP havuzunu ekler.
    """

    # VPN Yapılandırma Listesi 
    # (Buraya birden fazla sunucu ve subnet ekleyebilirsin)
    vpn_configs = [
        {
            "server_name": "De_Almanya_1",
            "server_country": "DE",
            "ip_address":"18.195.50.202",
            "cidr": "10.0.0.0/24",  # DÜZELTİLDİ: 10.8 değil, sunucunun çalıştığı 10.0 bloğu
            "gateway": "10.0.0.1",  # VPN sunucusunun kendi IP'si (Havuza eklenmez)
            "is_premium": True,
            "public_key":"NJlfmmc1LJ2fitN7QauM9PS4AhbfMcGm7o+F5sYREm8="
        },{
            "server_name": "Sw_İsviçre_1",
            "server_country": "SW",
            "ip_address": "13.62.228.126",
            "cidr": "10.0.0.0/24",  # DÜZELTİLDİ: 10.8 değil, sunucunun çalıştığı 10.0 bloğu
        "gateway": "10.0.0.1",  # VPN sunucusunun kendi IP'si (Havuza eklenmez)
            "is_premium": True,
            "public_key":"2KgkqdFXos5FZtKcf9DLVYr8u5ckpwuEQyG1whX9glQ="
        },
        # İleride 2. sunucuyu eklemek istersen buraya obje eklemen yeterli:
        # { "server_name": "US_NewYork_1", "cidr": "10.9.0.0/24", "gateway": "10.9.0.1", "is_premium": True }
    ]

    for config in vpn_configs:
        print(f"--- {config['server_name']} İşleniyor ---")

        # 1. Önce Server veritabanında var mı kontrol et
        server = session.query(ServerList).filter_by(server_name=config['server_name']).first()

        if not server:
            # Server yoksa oluştur
            print(f"Server oluşturuluyor: {config['server_name']}")
            server = ServerList(
                server_name=config['server_name'],
                is_premium=config['is_premium'],
                public_key = config["public_key"],
                server_country = config["server_country"],
                ip_address =  config["ip_address"],

            )
            session.add(server)
            session.commit()
            session.refresh(server)  # ID'yi almak için refresh yapıyoruz
        else:
            print(f"Server zaten mevcut: {config['server_name']} (ID: {server.id})")

        # 2. IP Havuzunu Oluştur
        network = ipaddress.IPv4Network(config['cidr'])
        ips_to_add = []

        # Bu sunucu için zaten IP var mı? (Basit bir kontrol)
        # Daha detaylı kontrol istersen tek tek bakılabilir ama ilk kurulum için bu yeterli.
        existing_ip_count = session.query(IpPool).filter_by(server_id=server.id).count()

        if existing_ip_count > 0:
            print(f"Bu sunucu için zaten {existing_ip_count} IP var. Pas geçiliyor.")
            continue

        print(f"IP'ler hazırlanıyor ({config['cidr']})...")

        for ip in network.hosts():
            ip_str = str(ip)

            # Gateway (Sunucu IP'si) havuza eklenmez
            if ip_str == config['gateway']:
                continue

            # IpPool nesnesini oluştururken server_id'yi EKLE
            ips_to_add.append(
                IpPool(
                    ip_address=ip_str,
                    is_available=True,
                    server_id=server.id  # <-- KRİTİK KISIM: IP'yi sunucuya bağlıyoruz
                )
            )

        # Hepsini tek seferde kaydet
        if ips_to_add:
            session.bulk_save_objects(ips_to_add)
            session.commit()
            print(f"{len(ips_to_add)} adet IP, {config['server_name']} sunucusuna eklendi!")

    session.close()


if __name__ == "__main__":
    # Session oluşturma kodun burada olmalı
    # Örn: from backend.db.base import SessionLocal
    # session = SessionLocal()
    # init_db_ips(session)
    pass