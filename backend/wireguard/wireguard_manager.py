
import paramiko
import os
from pathlib import Path
class WireGuardSSHManager():
    def __init__(self,ip_address,key_filename):
        current_dir = Path(__file__).resolve().parent
        self.key_path = current_dir.parent / "key" / key_filename
        self.key_path = str(self.key_path)
        self.host = ip_address
        self.port = "22"
        self.username = "ubuntu"
         # SSH Private Key dosya yolu
        self.wg_interface = "wg0"

    def add_peer (self,client_public_key:str,client_ip_adress:str):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=self.host,port=self.port,username=self.username,key_filename=self.key_path,timeout=10)
            command = f"sudo wg set {self.wg_interface} peer '{client_public_key}' allowed-ips {client_ip_adress} && sudo wg-quick save {self.wg_interface}"
            print(f"Komut çalışıyor {command}")

            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(" WireGuard Peer başarıyla eklendi.")
                return True
            else:
                # Hata varsa logla
                error_msg = stderr.read().decode()
                print(f" HATA OLUŞTU: {error_msg}")
                return False

        except Exception as e:
            print(f" SSH Bağlantı Hatası: {e}")
            return False
        finally:
        # Ne olursa olsun bağlantıyı kapat
            ssh.close()

    def remove_peer(self, client_public_key: str):
        """
        Verilen Public Key'e sahip peer'ı WireGuard arayüzünden siler ve kaydeder.
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # 1. SSH Bağlantısını Aç
            ssh.connect(hostname=self.host, port=self.port, username=self.username, key_filename=self.key_path,
                        timeout=10)

            # 2. Silme Komutunu Hazırla
            # wg set wg0 peer <KEY> remove -> Kullanıcıyı atar
            # wg-quick save wg0 -> Config dosyasını günceller (Kalıcılık için şart)
            command = f"sudo wg set {self.wg_interface} peer '{client_public_key}' remove && sudo wg-quick save {self.wg_interface}"

            print(f"Silme komutu çalışıyor: {command}")

            # 3. Komutu Çalıştır
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()

            # 4. Sonucu Kontrol Et
            if exit_status == 0:
                print(f"WireGuard Peer ({client_public_key}) başarıyla silindi ve kaydedildi.")
                return True
            else:
                error_msg = stderr.read().decode()
                print(f"HATA (Peer Silinemedi): {error_msg}")
                return False

        except Exception as e:
            print(f"SSH Bağlantı Hatası (Remove Peer): {e}")
            return False

        finally:
            # 5. Bağlantıyı Kapat
            ssh.close()
