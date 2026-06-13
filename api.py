import os
import csv
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# JSON çıktısında Türkçe karakterlerin bozulmaması için
app.config['JSON_AS_ASCII'] = False

# ---------------------------------------------------------
# HTML VE CSS TASARIMI (Dashboard Arayüzü)
# ---------------------------------------------------------
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TCMB Döviz Kurları</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 40px 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
        p.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; font-size: 14px; }
        .btn-container { text-align: center; margin-bottom: 30px; }
        .btn { display: inline-block; background: #27ae60; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; transition: background 0.3s, transform 0.2s; }
        .btn:hover { background: #2ecc71; transform: translateY(-2px); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
        th { background-color: #f8f9fa; color: #34495e; font-weight: 600; text-transform: uppercase; font-size: 13px; letter-spacing: 0.5px; }
        tr:hover { background-color: #fcfcfc; }
        .kod { font-weight: bold; color: #2980b9; background: #ebf5fb; padding: 4px 8px; border-radius: 4px; font-size: 13px; }
        .hata { background: #ff7675; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .footer { text-align: center; margin-top: 40px; font-size: 12px; color: #bdc3c7; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇹🇷 TCMB Güncel Döviz Kurları</h1>
        <p class="subtitle">Arka plan servisi tarafından her gece 00:05'te otomatik güncellenir.</p>
        
        <div class="btn-container">
            <a href="/api/kurlar" class="btn" target="_blank">JSON API Formatında Gör</a>
        </div>

        {% if hata %}
            <div class="hata">{{ hata_mesaji }}</div>
        {% else %}
            <table>
                <thead>
                    <tr>
                        <th>Döviz Kodu</th>
                        <th>İsim</th>
                        <th>Alış (Forex)</th>
                        <th>Satış (Forex)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for kur in kurlar %}
                    <tr>
                        <td><span class="kod">{{ kur['Döviz Kodu'] }}</span></td>
                        <td>{{ kur['Döviz Cinsi'] }}</td>
                        <td>{{ kur['Döviz Alış (Forex)'] }}</td>
                        <td>{{ kur['Döviz Satış (Forex)'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
        
        <div class="footer">
            🚀 IIS + FastCGI + Python Flask ile güçlendirilmiştir.
        </div>
    </div>
</body>
</html>
"""

# ---------------------------------------------------------
# 1. ANA SAYFA PANELİ (Dashboard)
# ---------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    dosya_tam_yolu = r"C:\TcmbKur\tcmb_doviz_kurlari.csv"
    kurlar = []
    
    try:
        with open(dosya_tam_yolu, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                kurlar.append(row)
        return render_template_string(HTML_SABLON, kurlar=kurlar, hata=False)
    except Exception as e:
        hata_mesaji = f"Veriler okunamadı. Arka plan servisi dosyayı henüz oluşturmamış olabilir. Hata: {str(e)}"
        return render_template_string(HTML_SABLON, kurlar=[], hata=True, hata_mesaji=hata_mesaji)

# ---------------------------------------------------------
# 2. ENTEGRASYONLAR İÇİN JSON API (/api/kurlar)
# ---------------------------------------------------------
@app.route('/api/kurlar', methods=['GET'])
def get_kurlar():
    dosya_tam_yolu = r"C:\TcmbKur\tcmb_doviz_kurlari.csv"
    kurlar = []
    
    try:
        with open(dosya_tam_yolu, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                kurlar.append(row)
                
        return jsonify({
            "durum": "basarili",
            "veri_sayisi": len(kurlar),
            "kurlar": kurlar
        }), 200
        
    except FileNotFoundError:
        return jsonify({
            "durum": "hata", 
            "mesaj": "Kur dosyasi bulunamadi. Arka plan servisi henüz kurlari cekmemis olabilir."
        }), 404
    except Exception as e:
        return jsonify({
            "durum": "hata", 
            "mesaj": f"Sunucu hatasi: {str(e)}"
        }), 500

# ---------------------------------------------------------
# 3. DOĞRUDAN ÇALIŞTIRMA (Test İçin)
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)