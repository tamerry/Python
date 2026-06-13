  TCMB Döviz Kurları Çekici & REST API body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; color: #24292e; max-width: 900px; margin: 0 auto; padding: 40px 20px; background-color: #ffffff; } h1, h2, h3 { border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; margin-top: 24px; margin-bottom: 16px; font-weight: 600; } hr { height: 0.25em; padding: 0; margin: 24px 0; background-color: #e1e4e8; border: 0; } pre { background-color: #f6f8fa; border-radius: 6px; padding: 16px; overflow: auto; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 85%; } code { background-color: rgba(27,31,35,0.05); border-radius: 3px; padding: 0.2em 0.4em; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 85%; } pre code { background-color: transparent; padding: 0; } ul, ol { padding-left: 2em; margin-top: 0; margin-bottom: 16px; } li { margin-bottom: 0.25em; } a { color: #0366d6; text-decoration: none; } a:hover { text-decoration: underline; } mermaid.initialize({startOnLoad:true});

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

📐 Proje Mimarisi ve Veri Akışı
-------------------------------

Sistem arka planda çalışan bir veri toplayıcı ve önyüzde hizmet veren bir API sunucusundan oluşur. Veri akış şemasını aşağıda görebilirsiniz:

flowchart TD subgraph Arka Plan Katmanı \[Arka Plan Zamanlayıcı Servisi\] WS\[Windows Servisi  
TCMB\_Kur\_Servisi / NSSM\] -->|Her Gece 00:05| PyServis\[tcmb\_servis.py\] PyServis -->|HTTP GET / verify=False| TCMB((TCMB XML Servisi)) TCMB -->|Bugünün XML Verisi| PyServis end subgraph Veri Katmanı \[Depolama\] CSV\[(tcmb\_doviz\_kurlari.csv  
Yol: C:\\TcmbKur\\)\] end PyServis -->|XML'i Ayrıştır &  
utf-8-sig ile Kaydet| CSV subgraph Sunucu Katmanı \[IIS & Python Flask Web Server\] IIS\[IIS Web Sunucusu  
Port: 80 / 8080\] -->|wfastcgi.py Köprüsü| Flask\[Flask Uygulaması  
app.py\] Flask -->|Anlık CSV Dosyasını Okur| CSV end subgraph İstemci Katmanı \[Tüketiciler / Entegrasyon\] User1\[Son Kullanıcı  
Tarayıcı\] -->|GET /| IIS User2\[Dış Sistemler  
Muhasebe / Mobil / Web\] -->|GET /api/kurlar| IIS Flask -->|Şık HTML + CSS Arayüzü| User1 Flask -->|Saf JSON Çıktısı| User2 end style CSV fill:#f9f,stroke:#333,stroke-width:2px style TCMB fill:#bbf,stroke:#333,stroke-width:2px style IIS fill:#f96,stroke:#333,stroke-width:2px style Flask fill:#6c6,stroke:#333,stroke-width:1px style WS fill:#fff,stroke:#333,stroke-width:1px

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