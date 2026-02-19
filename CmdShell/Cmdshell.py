import pyodbc
import pandas as pd
import concurrent.futures

# Dosya isimleri (Kendi yollarınızı korudum)
girdi_dosyasi = r'D:\GitHub\Algoritmalar\XpcmdShell\sunucular.txt'
cikti_dosyasi = r'D:\GitHub\Algoritmalar\XpcmdShell\Wsonuclar.xlsx'

# Sunucu listesini oku
try:
    with open(girdi_dosyasi, 'r', encoding='utf-8') as dosya:
        sunucular = [satir.strip() for satir in dosya.readlines() if satir.strip()]
except FileNotFoundError:
    print(f"Hata: '{girdi_dosyasi}' bulunamadı!")
    exit()

def sunucu_kontrol_et(sunucu):
    print(f"[{sunucu}] kontrol ediliyor...")
    
    # Varsayılan değerler
    vendor, name, serial = "HATA", "HATA", "HATA"
    
    try:
        # BAĞLANTI AYARLARI (Şifreyi güncelleyebilirsiniz)
        conn_str = (
            r'DRIVER={SQL Server};'
            f'SERVER={sunucu};'
            r'DATABASE=master;'
            r'UID=db user;'
            r'PWD=db pass;'
        )
        
        # Express sürümlerde donmaları önlemek için 5 saniyelik zaman aşımı
        conn = pyodbc.connect(conn_str, timeout=5, autocommit=True)
        cursor = conn.cursor()
        
        # 1. AŞAMA: xp_cmdshell'i aktif et
        cursor.execute("EXEC sp_configure 'show advanced options', 1; RECONFIGURE WITH OVERRIDE;")
        cursor.execute("EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE WITH OVERRIDE;")
        
        # 2. AŞAMA: Donanım bilgilerini Modern PowerShell komutu ile çek
        # Veriyi tek satırda 'SERI@MODEL@MARKA' formatında istiyoruz
        ps_command = 'powershell.exe -NoProfile -Command "Get-CimInstance -ClassName Win32_ComputerSystemProduct | ForEach-Object { \\\"$($_.IdentifyingNumber)@$($_.Name)@$($_.Vendor)\\\" }"'
        
        cursor.execute(f"EXEC xp_cmdshell '{ps_command}'")
        sonuclar = cursor.fetchall()
        
        # 3. AŞAMA: Güvenlik için ayarları tekrar kapat
        cursor.execute("EXEC sp_configure 'xp_cmdshell', 0; RECONFIGURE WITH OVERRIDE;")
        cursor.execute("EXEC sp_configure 'show advanced options', 0; RECONFIGURE WITH OVERRIDE;")
        
        cursor.close()
        conn.close()
        
        # 4. AŞAMA: Dönen veriyi ayrıştır (Parse)
        for satir in sonuclar:
            # satir[0] null değilse ve içinde ayırıcı '@' varsa bu bizim aradığımız satırdır
            if satir[0] and '@' in satir[0]:
                parcalar = satir[0].split('@')
                if len(parcalar) >= 3:
                    serial = parcalar[0].strip()
                    name = parcalar[1].strip()
                    vendor = parcalar[2].strip()
                    break # Doğru veriyi bulduk, döngüden çık
                
    except Exception as e:
        # Hata detayını temizleyerek konsola bas
        hata_mesaji = str(e).replace('\n', ' ')
        print(f"  [X] {sunucu} hatası: {hata_mesaji[:60]}...")
        vendor, name, serial = "BAĞLANTI/YETKİ HATASI", "BAĞLANTI/YETKİ HATASI", "BAĞLANTI/YETKİ HATASI"

    return {
        "Sunucu (IP)": sunucu,
        "Seri No": serial,
        "Model": name,
        "Marka": vendor
    }

# --- ANA ÇALIŞTIRMA BLOĞU ---
if __name__ == '__main__':
    tablo_verileri = []
    
    MAX_WORKER_SAYISI = 20 
    print(f"\nİşlem {MAX_WORKER_SAYISI} iş parçacığı ile başlatıldı. Lütfen bekleyin...\n")

    # Paralel işlem (Multi-threading)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER_SAYISI) as executor:
        for sonuc in executor.map(sunucu_kontrol_et, sunucular):
            tablo_verileri.append(sonuc)

    # --- EXCEL DOSYASINI OLUŞTUR ---
    if tablo_verileri:
        df = pd.DataFrame(tablo_verileri)
        df.to_excel(cikti_dosyasi, index=False)
        print(f"\nİşlem tamamlandı! Sonuçlar '{cikti_dosyasi}' dosyasına kaydedildi.")
    else:
        print("\nİşlenecek veri bulunamadı.")