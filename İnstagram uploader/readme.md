# Instagram Yükleyici Pro 🚀

Modern arayüzü ve gelişmiş özellikleriyle masaüstünden Instagram'a zahmetsizce Gönderi, Hikaye ve Reel yüklemenizi sağlayan profesyonel bir Python masaüstü (GUI) uygulamasıdır. 

Uygulama, Instagram API'si ile haberleşmek için `instagrapi` kütüphanesini kullanır ve standart komut satırı araçlarının aksine, kullanıcı dostu modern bir arayüze sahiptir.

## ✨ Özellikler

* **Modern ve Şık Arayüz:** Kullanıcı dostu, ferah ve etkileşimli Tkinter tasarımı.
* **Akıllı Oturum Yönetimi:** Şifrenizi her seferinde girmenize gerek kalmaz; oturumunuz (session) güvenli bir şekilde bilgisayarınızın geçici belleğine (Temp) kaydedilir.
* **Çoklu Format Desteği:** * 🎥 **Reel:** MP4 desteği ve isteğe bağlı kapak (thumbnail) görseli ekleme.
  * ⏱ **Hikaye (Story):** JPG, PNG ve MP4 desteği.
  * 🖼 **Gönderi (Post):** JPG, PNG ve MP4 formatlarında tekli veya çoklu (sıralı) yükleme.
* **Gelişmiş Metin Yönetimi:** Açıklama (Caption) ve Etiketleri (Tags) ayrı ayrı yazabilme; program bunları Instagram için otomatik olarak uygun formata dönüştürüp birleştirir.
* **Bağımsız Çalışabilme (.exe):** Python yüklü olmayan bilgisayarlarda bile tek tıkla çalıştırılabilir versiyona derlenebilir.

## 📸 Ekran Görüntüleri

*(Buraya uygulamanızın ekran görüntülerini ekleyebilirsiniz. Örnek kullanım: `![Giriş Ekranı](gorsel_linki_buraya.png)` )*

## 🛠️ Gereksinimler

Kodu geliştirici olarak kendi bilgisayarınızda çalıştırmak için aşağıdaki gereksinimlere ihtiyacınız vardır:

* Python 3.8 veya üzeri
* `instagrapi` (Instagram API işlemleri için)
* `Pillow` (Görsel işleme ve boyutlandırma için)

## 🚀 Kurulum ve Çalıştırma

**1. Repoyu bilgisayarınıza klonlayın:**
` ` `bash
git clone https://github.com/tamerry/Python.git
cd instagram-yukleyici-pro
` ` `

**2. Gerekli kütüphaneleri yükleyin:**
` ` `bash
pip install instagrapi Pillow
` ` `

**3. Programı çalıştırın:**
` ` `bash
python instagram_yukleyici.py
` ` `

## 📦 .exe Olarak Derleme (Windows İçin)

Programı başka bilgisayarlarda Python kurmadan çalıştırmak için `PyInstaller` kullanarak tek bir .exe dosyası haline getirebilirsiniz.

` ` `bash
pip install pyinstaller
pyinstaller --noconsole --onefile instagram_yukleyici.py
` ` `
*Not: Derleme işlemi bittiğinde programınız `dist` klasörü içerisinde `instagram_yukleyici.exe` adıyla oluşacaktır.*

## ⚠️ Önemli Uyarılar ve Bilinmesi Gerekenler

* **Instagram Limitleri:** `instagrapi` resmi olmayan bir API aracıdır. Arka arkaya, hiç beklemeden çok fazla dosya yüklemek veya spam yapmak, Instagram tarafından hesabınızın (Action Block) geçici olarak engellenmesine neden olabilir. Uygulamayı doğal insan davranışlarına uygun hızlarda kullanmanız tavsiye edilir.
* **Antivirüs Uyarıları (.exe):** Programı `.exe` olarak derlediğinizde, PyInstaller'ın çalışma mantığı gereği Windows Defender "False Positive" (Yanlış Alarm) verebilir. Kodu kendiniz derlediğiniz için güvenlidir, istisnalara ekleyebilirsiniz.
* **Video Formatları:** Instagram sunucuları videoları işlerken seçicidir. Hata almamak için yüklediğiniz videoların standart **H.264 codec** ve maksimum **30 FPS** değerlerinde olduğundan emin olun.

## 👨‍💻 Geliştirici

**Tamer Yavuz** Bağlantı kurmak için: [LinkedIn Profilim](https://www.linkedin.com/in/tamer-yavuz-73628084/)

---
*Bu proje açık kaynaklıdır ve eğitim/kişisel kullanım amacıyla geliştirilmiştir. Instagram'ın kullanım koşullarını ihlal edecek şekilde (spam vb.) kullanılması önerilmez.*