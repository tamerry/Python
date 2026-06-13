
🇹🇷 TCMB Döviz Kurları Çekici & REST API
=========================================

Bu proje, **Türkiye Cumhuriyet Merkez Bankası (TCMB)** tarafından günlük olarak yayınlanan güncel döviz kurlarını otomatik olarak çeken bir arka plan servisi ile bu verileri şık bir web paneli ve JSON API olarak sunan bir Flask uygulamasından oluşmaktadır.

* * *

✨ Özellikler
------------

*   **7/24 Otonom Çalışma:** NSSM (Non-Sucking Service Manager) ile Windows Servisi olarak çalışır. Sunucu yeniden başlasa bile her gece 00:05'te kurları otomatik günceller.
*   **Hızlı ve Hafif JSON API:** Diğer sistemlerin (Mobil, Web, Muhasebe) kolayca tüketebilmesi için IIS ve FastCGI üzerinden kesintisiz REST API sunar.
*   **Modern Web Dashboard:** Tarayıcı üzerinden girildiğinde kurları şık, modern ve mobil uyumlu bir tablo ile gösterir.
*   **Excel ile %100 Uyumlu CSV:** Çekilen veriler Türkçe karakter bozulması olmadan (`utf-8-sig`) CSV formatında yedeklenir.
*   **SSL Sertifika Bypass Özelliği:** Kurumsal ağlarda veya proxy arkasında yaşanan `SSLCertVerificationError` hatalarını otomatik olarak aşar.

* * *



* * *

🚀 Gereksinimler ve Kurulum
---------------------------

Projenin tam kapasiteyle çalışması için Windows Server/IIS ortamı ve Python 3.x gereklidir.

**Gerekli Kütüphaneler:**

    pip install requests schedule flask

**Adım Adım Kurulum:**

1.  `tcmb_servis.py` dosyasını NSSM kullanarak bir Windows Servisi haline getirin (Örn: `TCMB_Kur_Servisi`).
2.  Flask uygulamasını barındıran `app.py` dosyasını IIS `wwwroot` dizinine yerleştirin.
3.  IIS üzerinde `wfastcgi` ayarlarını yaparak Python yolunuzu `web.config` içine tanımlayın.
4.  Hem `wwwroot` hem de CSV'nin kaydedildiği klasöre `IIS_IUSRS` için okuma/yazma izinlerini verin.

* * *

📡 API Kullanımı
----------------

Sisteminizi ayağa kaldırdıktan sonra JSON formatında verilere erişmek için aşağıdaki uç noktayı (endpoint) kullanabilirsiniz:

**İstek (Request):**

    GET /api/kurlar HTTP/1.1
    Host: sunucu_adresiniz.com

**Örnek Yanıt (Response):**

    {
      "durum": "basarili",
      "kurlar": [
        {
          "Döviz Alış (Forex)": "32.1456",
          "Döviz Cinsi": "ABD DOLARI",
          "Döviz Kodu": "USD",
          "Döviz Satış (Forex)": "32.2035",
          "Efektif Alış (Nakit)": "32.1232",
          "Efektif Satış (Nakit)": "32.2518"
        }
      ],
      "veri_sayisi": 1
    }

* * *

🤝 Katkıda Bulunma
------------------

Geliştirme taleplerinizi veya hata bildirimlerinizi iletmekten çekinmeyin!

1.  Bu depoyu **Fork** edin.
2.  Yeni bir Feature Branch oluşturun (`git checkout -b yeni-ozellik`).
3.  Değişikliklerinizi **Commit** edin (`git commit -m 'Yeni özellik eklendi'`).
4.  Branch'inizi **Push** edin (`git push origin yeni-ozellik`).
5.  Bir **Pull Request** açın.

* * *

📜 Lisans
---------

Bu proje [MIT](LICENSE) lisansı altında lisanslanmıştır. Dilediğiniz gibi kullanabilir, değiştirebilir ve ticari projelerinize entegre edebilirsiniz.