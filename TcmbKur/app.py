import os
import csv
import xml.etree.ElementTree as ET
import requests
import urllib3

# SSL doğrulamasını kapattığımız için konsola düşecek uyarıları gizliyoruz
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tcmb_kurlarini_csv_yap(dosya_adi="tcmb_doviz_kurlari.csv"):
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print("TCMB'den güncel kurlar çekiliyor...")
        
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status() 

        # XML verisini ayrıştır (parse et)
        root = ET.fromstring(response.content)

        # ---------------------------------------------------------
        # DOSYANIN KAYDEDİLECEĞİ YERİ BELİRLEME (GÜNCEL KISIM)
        # 1. Bu scriptin çalıştığı tam klasör yolunu bul
        script_dizini = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Klasör yolu ile dosya adını birleştir
        dosya_tam_yolu = os.path.join(script_dizini, dosya_adi)
        # ---------------------------------------------------------

        # CSV dosyasını oluşturuyoruz
        with open(dosya_tam_yolu, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            # Başlık satırı
            writer.writerow([
                "Döviz Kodu",
                "Döviz Cinsi",
                "Döviz Alış (Forex)",
                "Döviz Satış (Forex)",
                "Efektif Alış (Nakit)",
                "Efektif Satış (Nakit)",
            ])

            for currency in root.findall("Currency"):
                kod = currency.get("CurrencyCode")

                if not kod:
                    continue

                isim = (
                    currency.find("Isim").text.strip()
                    if currency.find("Isim") is not None
                    else ""
                )

                forex_alis = (
                    currency.find("ForexBuying").text
                    if currency.find("ForexBuying") is not None
                    else ""
                )
                forex_satis = (
                    currency.find("ForexSelling").text
                    if currency.find("ForexSelling") is not None
                    else ""
                )

                efektif_alis = (
                    currency.find("BanknoteBuying").text
                    if currency.find("BanknoteBuying") is not None
                    else ""
                )
                efektif_satis = (
                    currency.find("BanknoteSelling").text
                    if currency.find("BanknoteSelling") is not None
                    else ""
                )

                writer.writerow([
                    kod,
                    isim,
                    forex_alis,
                    forex_satis,
                    efektif_alis,
                    efektif_satis,
                ])

        print(f"Başarılı! Güncel kurlar tam olarak buraya kaydedildi:\n{dosya_tam_yolu}")

    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: TCMB sitesine ulaşılamadı. Hata: {e}")
    except ET.ParseError as e:
        print(f"XML Ayrıştırma hatası: TCMB'den gelen veri okunamadı. Hata: {e}")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

if __name__ == "__main__":
    tcmb_kurlarini_csv_yap()