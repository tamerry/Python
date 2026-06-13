<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TCMB Döviz Kurları Çekici & REST API</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #ffffff;
        }
        h1, h2, h3 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }
        pre {
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 85%;
        }
        code {
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
            padding: 0.2em 0.4em;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 85%;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        ul, ol {
            padding-left: 2em;
            margin-top: 0;
            margin-bottom: 16px;
        }
        li {
            margin-bottom: 0.25em;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>

    <h1>🇹🇷 TCMB Döviz Kurları Çekici & REST API</h1>
    
    <p>Bu proje, <strong>Türkiye Cumhuriyet Merkez Bankası (TCMB)</strong> tarafından günlük olarak yayınlanan güncel döviz kurlarını otomatik olarak çeken bir arka plan servisi ile bu verileri şık bir web paneli ve JSON API olarak sunan bir Flask uygulamasından oluşmaktadır.</p>

    <hr>

    <h2>✨ Özellikler</h2>
    <ul>
        <li><strong>7/24 Otonom Çalışma:</strong> NSSM (Non-Sucking Service Manager) ile Windows Servisi olarak çalışır. Sunucu yeniden başlasa bile her gece 00:05'te kurları otomatik günceller.</li>
        <li><strong>Hızlı ve Hafif JSON API:</strong> Diğer sistemlerin (Mobil, Web, Muhasebe) kolayca tüketebilmesi için IIS ve FastCGI üzerinden kesintisiz REST API sunar.</li>
        <li><strong>Modern Web Dashboard:</strong> Tarayıcı üzerinden girildiğinde kurları şık, modern ve mobil uyumlu bir tablo ile gösterir.</li>
        <li><strong>Excel ile %100 Uyumlu CSV:</strong> Çekilen veriler Türkçe karakter bozulması olmadan (<code>utf-8-sig</code>) CSV formatında yedeklenir.</li>
        <li><strong>SSL Sertifika Bypass Özelliği:</strong> Kurumsal ağlarda veya proxy arkasında yaşanan <code>SSLCertVerificationError</code> hatalarını otomatik olarak aşar.</li>
    </ul>

    <hr>

    <h2>📐 Proje Mimarisi ve Veri Akışı</h2>
    <p>Sistem arka planda çalışan bir veri toplayıcı ve önyüzde hizmet veren bir API sunucusundan oluşur. Veri akış şemasını aşağıda görebilirsiniz:</p>

    <div class="mermaid">
    flowchart TD
        subgraph Arka Plan Katmanı [Arka Plan Zamanlayıcı Servisi]
            WS[Windows Servisi<br/>TCMB_Kur_Servisi / NSSM] -->|Her Gece 00:05| PyServis[tcmb_servis.py]
            PyServis -->|HTTP GET / verify=False| TCMB((TCMB XML Servisi))
            TCMB -->|Bugünün XML Verisi| PyServis
        end

        subgraph Veri Katmanı [Depolama]
            CSV[(tcmb_doviz_kurlari.csv<br/>Yol: C:\TcmbKur\)]
        end

        PyServis -->|XML'i Ayrıştır & <br/>utf-8-sig ile Kaydet| CSV

        subgraph Sunucu Katmanı [IIS & Python Flask Web Server]
            IIS[IIS Web Sunucusu<br/>Port: 80 / 8080] -->|wfastcgi.py Köprüsü| Flask[Flask Uygulaması<br/>app.py]
            Flask -->|Anlık CSV Dosyasını Okur| CSV
        end

        subgraph İstemci Katmanı [Tüketiciler / Entegrasyon]
            User1[Son Kullanıcı<br/>Tarayıcı] -->|GET /| IIS
            User2[Dış Sistemler<br/>Muhasebe / Mobil / Web] -->|GET /api/kurlar| IIS
            Flask -->|Şık HTML + CSS Arayüzü| User1
            Flask -->|Saf JSON Çıktısı| User2
        end

        style CSV fill:#f9f,stroke:#333,stroke-width:2px
        style TCMB fill:#bbf,stroke:#333,stroke-width:2px
        style IIS fill:#f96,stroke:#333,stroke-width:2px
        style Flask fill:#6c6,stroke:#333,stroke-width:1px
        style WS fill:#fff,stroke:#333,stroke-width:1px
    </div>
    <hr>

    <h2>🚀 Gereksinimler ve Kurulum</h2>
    <p>Projenin tam kapasiteyle çalışması için Windows Server/IIS ortamı ve Python 3.x gereklidir.</p>
    
    <p><strong>Gerekli Kütüphaneler:</strong></p>
<pre><code class="language-bash">pip install requests schedule flask</code></pre>

    <p><strong>Adım Adım Kurulum:</strong></p>
    <ol>
        <li><code>tcmb_servis.py</code> dosyasını NSSM kullanarak bir Windows Servisi haline getirin (Örn: <code>TCMB_Kur_Servisi</code>).</li>
        <li>Flask uygulamasını barındıran <code>app.py</code> dosyasını IIS <code>wwwroot</code> dizinine yerleştirin.</li>
        <li>IIS üzerinde <code>wfastcgi</code> ayarlarını yaparak Python yolunuzu <code>web.config</code> içine tanımlayın.</li>
        <li>Hem <code>wwwroot</code> hem de CSV'nin kaydedildiği klasöre <code>IIS_IUSRS</code> için okuma/yazma izinlerini verin.</li>
    </ol>

    <hr>

    <h2>📡 API Kullanımı</h2>
    <p>Sisteminizi ayağa kaldırdıktan sonra JSON formatında verilere erişmek için aşağıdaki uç noktayı (endpoint) kullanabilirsiniz:</p>

    <p><strong>İstek (Request):</strong></p>
<pre><code class="language-http">GET /api/kurlar HTTP/1.1
Host: sunucu_adresiniz.com</code></pre>

    <p><strong>Örnek Yanıt (Response):</strong></p>
<pre><code class="language-json">{
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
}</code></pre>

    <hr>

    <h2>🤝 Katkıda Bulunma</h2>
    <p>Geliştirme taleplerinizi veya hata bildirimlerinizi iletmekten çekinmeyin!</p>
    <ol>
        <li>Bu depoyu <strong>Fork</strong> edin.</li>
        <li>Yeni bir Feature Branch oluşturun (<code>git checkout -b yeni-ozellik</code>).</li>
        <li>Değişikliklerinizi <strong>Commit</strong> edin (<code>git commit -m 'Yeni özellik eklendi'</code>).</li>
        <li>Branch'inizi <strong>Push</strong> edin (<code>git push origin yeni-ozellik</code>).</li>
        <li>Bir <strong>Pull Request</strong> açın.</li>
    </ol>

    <hr>

    <h2>📜 Lisans</h2>
    <p>Bu proje <a href="LICENSE">MIT</a> lisansı altında lisanslanmıştır. Dilediğiniz gibi kullanabilir, değiştirebilir ve ticari projelerinize entegre edebilirsiniz.</p>

</body>
</html>