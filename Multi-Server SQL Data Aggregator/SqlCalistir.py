import pandas as pd
import pyodbc
import os
import sys
import warnings

# Gereksiz uyarıları temizlemek için
warnings.filterwarnings('ignore')

# ================= AYARLAR =================

# 1. Kodun kendi bulunduğu klasör yolunu alıyoruz
script_dizini = os.path.dirname(os.path.abspath(__file__))

# 2. Dosya yollarını tanımlıyoruz
IP_DOSYASI = os.path.join(script_dizini, 'sunucu_ipleri.txt')
SQL_DOSYASI = os.path.join(script_dizini, 'sorgu.sql') # SQL'in okunacağı dosya
CIKTI_DOSYASI = os.path.join(script_dizini, 'Tum_Magazalar_Transfer_Durumu.xlsx')
HATA_LOG_DOSYASI = os.path.join(script_dizini, 'Hatali_Baglantilar.txt') 

# Veritabanı Giriş Bilgileri
DB_USER = 'dbuser'          #database kullanıcı adı     
DB_PASS = 'dbpass'          #database şifre
DB_NAME = 'dbname'          #database adı 

def main():
    # --- KONTROLLER ---
    
    # 1. IP Dosyası Kontrolü
    if not os.path.exists(IP_DOSYASI):
        print(f"HATA: IP listesi bulunamadı -> {IP_DOSYASI}")
        #input("Kapatmak için Enter'a basın...")
        return

    # 2. SQL Dosyası Kontrolü
    if not os.path.exists(SQL_DOSYASI):
        print(f"HATA: SQL dosyası bulunamadı -> {SQL_DOSYASI}")
        print("Lütfen 'sorgu.sql' adında bir dosya oluşturup içine sorguyu yapıştırın.")
        #input("Kapatmak için Enter'a basın...")
        return

    # --- DOSYALARI OKUMA ---

    # IP Listesini Oku
    with open(IP_DOSYASI, 'r', encoding='utf-8', errors='ignore') as f:
        ip_listesi = [line.strip() for line in f if line.strip()]

    # SQL Sorgusunu Oku
    try:
        with open(SQL_DOSYASI, 'r', encoding='utf-8') as f:
            SQL_SORGU = f.read()
    except Exception as e:
        print(f"HATA: SQL dosyası okunamadı! Detay: {e}")
        return

    # Hata dosyasını sıfırla
    with open(HATA_LOG_DOSYASI, 'w', encoding='utf-8') as f:
        pass 

    tum_veriler = [] 
    basarili_sayisi = 0
    hata_sayisi = 0

    print(f"Toplam {len(ip_listesi)} sunucu taranacak...")
    print(f"Kullanılan Sorgu Dosyası: sorgu.sql\n")

    for ip in ip_listesi:
        print(f"--> Bağlanılıyor: {ip} ...", end=" ")
        
        try:
            conn_str = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={ip};"
                f"DATABASE={DB_NAME};"
                f"UID={DB_USER};"
                f"PWD={DB_PASS};"
                "Connection Timeout=10;"
            )
            
            with pyodbc.connect(conn_str) as conn:
                df = pd.read_sql(SQL_SORGU, conn)
                
                df.insert(0, 'SUNUCU_IP', ip)
                
                if not df.empty:
                    tum_veriler.append(df)
                    print(f"BAŞARILI ({len(df)} kayıt)")
                else:
                    print("VERİ YOK (OK)")
            
            basarili_sayisi += 1

        except Exception as e:
            print("HATA!")
            # Konsolda hatayı görelim ama dosyaya sadece IP yazacağız
            hata_mesaji = str(e).replace('\n', ' ')
            # print(f"    Detay: {hata_mesaji[:50]}...") # İsterseniz bu satırı açarak detay görebilirsiniz
            
            # Sadece IP'yi dosyaya yaz
            try:
                with open(HATA_LOG_DOSYASI, 'a', encoding='utf-8') as f_err:
                    f_err.write(f"{ip}\n")
            except:
                pass 
            
            hata_sayisi += 1

    # --- SONUÇLARI KAYDETME ---
    print("\n" + "="*30)
    
    if tum_veriler:
        print("Veriler birleştiriliyor...")
        final_df = pd.concat(tum_veriler, ignore_index=True)
        final_df.to_excel(CIKTI_DOSYASI, index=False)
        print(f"BAŞARILI! Excel kaydedildi: {CIKTI_DOSYASI}")
        print(f"Toplam Veri Satırı: {len(final_df)}")
    else:
        print("Hiçbir sunucudan veri dönmedi.")
    
    print("-" * 30)
    print(f"Başarılı Sunucu: {basarili_sayisi}")
    print(f"Hatalı Sunucu  : {hata_sayisi}")
    if hata_sayisi > 0:
        print(f"Hatalı IP listesi: {HATA_LOG_DOSYASI}")

if __name__ == "__main__":
    main()