# 🚀 SQL Server Multi-Threaded Donanım ve Veri Çekme Aracı

Bu Python betiği, bir metin dosyasında belirtilen SQL Server sunucu listesine **eşzamanlı (multi-threaded)** olarak bağlanır. Hedef sunuculardaki belirli bir veritabanından mağaza bilgilerini çeker ve `xp_cmdshell` üzerinden PowerShell komutları çalıştırarak sunucuların donanım bilgilerini (Seri Numarası, Model, Marka) elde eder. 

İşlem tamamlandığında tüm veriler düzenli bir **Excel (.xlsx)** dosyası olarak raporlanır.

## 🌟 Özellikler

* **Yüksek Performans:** `concurrent.futures.ThreadPoolExecutor` kullanılarak aynı anda 20 sunucuya kadar asenkron bağlantı kurulur. Bekleme süreleri minimize edilir.
* **Donanım Envanteri:** WMI (Windows Management Instrumentation) kullanılarak anakart/sistem seri numarası, üretici firma ve model bilgisi çekilir.
* **Otomatik Güvenlik Yönetimi:** Güvenlik riski oluşturan `xp_cmdshell` bileşeni sadece işlem sırasında aktif edilir ve işlem biter bitmez otomatik olarak tekrar kapatılır.
* **Excel Raporlama:** Başarılı olan işlemler ve bağlantı/yetki hataları temiz bir şekilde Pandas kullanılarak Excel'e aktarılır.
* **Zaman Aşımı Kontrolü:** Erişilemeyen veya yavaş yanıt veren Express sürümlerde scriptin takılı kalmasını önlemek için 5 saniyelik zaman aşımı (timeout) uygulanmıştır.

## 📋 Gereksinimler

Bu betiği çalıştırabilmek için sisteminizde Python 3.x ve aşağıdaki kütüphanelerin kurulu olması gerekmektedir:

```bash
pip install pyodbc pandas openpyxl
```
Ayrıca makinenizde SQL Server ile bağlantı kurabilmek için uygun ODBC Driver kurulu olmalıdır.

🛠️ Kurulum ve Kullanım
Bu repoyu bilgisayarınıza klonlayın veya indirin.

Proje dizininde bir ARA.txt dosyası oluşturun ve taranacak sunucuların IP adreslerini (veya Host namelerini) alt alta yazın.

Betik içerisindeki aşağıdaki ayarları kendi ortamınıza göre güncelleyin:

Dosya Yolları: girdi_dosyasi ve cikti_dosyasi değişkenlerini kendi sisteminize göre ayarlayın. (Öneri: Başka sistemlerde sorunsuz çalışması için tam yol yerine sadece dosya adlarını ARA.txt ve wsonuclar.xlsx olarak bırakabilirsiniz).

SQL Kimlik Bilgileri: conn_str içerisindeki UID (Kullanıcı Adı) ve PWD (Şifre) kısımlarını güncelleyin.

SQL Sorgusu: Eğer farklı bir veritabanından veri çekecekseniz betik içerisindeki Genius3.GENIUS3.STORE yolunu kendi yapınıza göre değiştirin.

⚠️ Güvenlik ve Uyarılar

xp_cmdshell Kullanımı: Betik, işletim sistemi seviyesinde komut çalıştırmak için sp_configure ile xp_cmdshell'i açar ve işlem bitiminde kapatır. Bu işlemin üretim (production) ortamlarında katı güvenlik kurallarına takılabileceğini unutmayın. İşlemi çalıştıran SQL kullanıcısının (örn: sa) bu yetkilere sahip olması gerekir.

Hata Yönetimi: Sunucuya bağlanılamaması veya yetki eksikliği durumunda program çökmez, Excel raporuna "BAĞLANTI/YETKİ HATASI" olarak not düşer.

🤝 Katkıda Bulunma
Geliştirmelere açıktır! Lütfen bir Pull Request açmadan önce yapacağınız değişiklikleri tartışmak için bir Issue oluşturun.

📝 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Serbestçe kullanılabilir ve değiştirilebilir.