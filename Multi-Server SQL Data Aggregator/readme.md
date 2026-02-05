<h1>Multi-Server SQL Data Aggregator</h1> (SqlCalistir.py)
Bu araç, bir metin dosyasındaki (sunucu_ipleri.txt) tüm SQL Server IP'lerine sırayla bağlanır, belirttiğiniz SQL sorgusunu (sorgu.sql) çalıştırır ve dönen tüm sonuçları tek bir Excel dosyasında birleştirir.

Bağlantı kurulamayan sunucuları otomatik olarak bir hata loguna kaydederek takibini kolaylaştırır.

<h3>🚀 Özellikler</h3>
Toplu İşlem: Onlarca hatta yüzlerce sunucuda aynı anda sorgu çalıştırabilir.

Hata Yönetimi: Bağlantı hatalarını ayıklar ve Hatali_Baglantilar.txt dosyasına yazar.

Veri Birleştirme: Her sunucudan gelen veriyi birleştirirken, verinin hangi IP'den geldiğini anlamanız için otomatik olarak SUNUCU_IP sütunu ekler.

Otomatik Excel Çıktısı: Sonuçları temiz bir tablo halinde dışa aktarır.

<h3>🛠 Kurulum</h3>

Python'ın yüklü olduğundan emin olun.

Gerekli kütüphaneleri yükleyin:

```Bash
pip install pandas pyodbc openpyxl
ODBC Driver: Bilgisayarınızda SQL Server ODBC sürücüsünün yüklü olması gerekir (Windows'ta standart olarak gelir).
```
<h3>📂 Dosya Yapısı</h3>
Scriptin çalışması için klasör düzeni şu şekilde olmalıdır:

SqlCalistir.py: Ana kod dosyası.

sunucu_ipleri.txt: Her satıra bir IP gelecek şekilde sunucu listesi.

sorgu.sql: Sunucularda çalıştırılacak T-SQL kodu.

Hatali_Baglantilar.txt: (Otomatik oluşur) Bağlanılamayan IP'ler.

Tum_Magazalar_Transfer_Durumu.xlsx: (Otomatik oluşur) Birleştirilmiş sonuçlar.

<h3>⚙️ Ayarlar</h3>
Kodun içerisindeki şu bölümü kendi veritabanı bilgilerinizle güncellemeyi unutmayın:

```text
# Veritabanı Giriş Bilgileri
DB_USER = 'dbuser'          # Kullanıcı adı     
DB_PASS = 'dbpass'          # Şifre
DB_NAME = 'dbname'          # Veritabanı adı 
```
<h3>📖 Kullanım</h3>
sunucu_ipleri.txt dosyasını oluşturun ve IP'leri alt alta yazın.

sorgu.sql dosyasına istediğiniz SELECT sorgusunu yazın.

Terminal veya komut satırından çalıştırın:

```python
python SqlCalistir.py
```
<h3>⚠️ Önemli Notlar</h3>
Bağlantı zaman aşımı (Timeout) 10 saniye olarak ayarlanmıştır. Yavaş bağlantılarda kodun içinde bu süreyi artırabilirsiniz.

Script, SQL Server kimlik doğrulaması (SQL Auth) kullanmaktadır.

<h3>Geliştirme İçin Not</h3>
Eğer bu araca yeni özellikler eklemek isterseniz (örneğin loglama detaylarının artırılması veya farklı DB türleri desteği), lütfen bir Pull Request açın veya Issue üzerinden bildirin.