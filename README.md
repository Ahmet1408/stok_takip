📦 Gelişmiş Stok Yönetim Sistemi
Gelişmiş Stok Yönetim Sistemi, küçük ve orta ölçekli işletmeler için tasarlanmış, kullanıcı dostu bir stok ve cari yönetim uygulamasıdır. Python ve Tkinter kullanılarak geliştirilen bu sistem, ürün yönetimi, stok takibi, cari hesap yönetimi ve raporlama gibi temel işlevleri sunar. Kullanıcıların stok hareketlerini kolayca izlemesine, ürünleri ve carileri yönetmesine olanak tanır.

🚀 Özellikler

Kullanıcı Yönetimi:
Kullanıcı kaydı ve giriş sistemi (SHA-256 ile şifreleme).
Firma bazlı yetkilendirme ve çoklu kullanıcı desteği.


Ürün Yönetimi:
Ürün ekleme, düzenleme ve silme.
Barkod, stok miktarı, kritik stok seviyesi, fiyat, KDV oranı ve birim desteği.
Cari (tedarikçi/müşteri) ile ilişkilendirme.


Cari Yönetimi:
Cari ekleme ve listeleme.
Cari kodu, vergi no, adres, telefon, e-posta ve yetkili kişi bilgileri.


Stok Hareketleri:
Stok giriş/çıkış hareketlerinin kaydı ve takibi.
Hareketlere kullanıcı, tarih ve açıklama ekleme.


Raporlama:
Kritik stok raporu ve tüm ürünler raporu.
Ürün listesinin CSV formatında dışa aktarımı.


Yedekleme:
Verilerin CSV formatında yedeklenmesi ve geri yüklenmesi.


Kullanıcı Arayüzü:
Modern ve sezgisel Tkinter tabanlı arayüz.
Arama, filtreleme ve sağ tık menüsü ile kolay kullanım.


Kritik Stok Uyarıları:
Stok seviyesi kritik seviyenin altına düştüğünde uyarılar.




🛠 Kurulum
Gereksinimler

Python 3.6 veya üzeri
Tkinter (genellikle Python ile birlikte gelir)
Standart Python kütüphaneleri (csv, hashlib, os, datetime)

Kurulum Adımları

Depoyu Klonlayın veya İndirin:
git clone https://github.com/kullanici/stok-yonetim-sistemi.git

veya ZIP dosyasını indirip çıkarın.

Proje Dizinine Gidin:
cd stok-yonetim-sistemi


Gerekli Kütüphaneleri Kontrol Edin:Tkinter genellikle Python ile birlikte gelir. Emin olmak için şu komutu çalıştırın:
python -c "import tkinter"

Eğer hata alırsanız, Tkinter'ı yükleyin:

Ubuntu/Debian: sudo apt-get install python3-tk
Windows/macOS: Genellikle Python kurulumunda bulunur.


Uygulamayı Çalıştırın:
python stok.py




📚 Kullanım
1. Giriş Yapma veya Kayıt Olma

 ![Uygulama Ekran Görüntüsü](https://github.com/Ahmet1408/stok_takip/blob/main/stok_takip/ss/login.png)

Giriş Ekranı:
Varsayılan kullanıcı oluşturmak için "Kayıt Ol" butonuna tıklayın.
Kullanıcı adı, şifre ve firma adı girerek kayıt olun.
Kayıt olduktan sonra kullanıcı adı ve şifre ile giriş yapın.


Not: Şifreler SHA-256 ile şifrelenir ve güvenli bir şekilde saklanır.

2. Ana Ekran

Sol Panel:
Kullanıcı bilgileri (kullanıcı adı, firma, yetki seviyesi).
Hızlı erişim butonları (Ürün Ekle, Cari Ekle, Stok Raporu).
Kritik stok uyarıları (stok miktarı kritik seviyenin altına düşen ürünler).

 ![Uygulama Ekran Görüntüsü](https://github.com/Ahmet1408/stok_takip/blob/main/stok_takip/ss/main.png)


Sağ Panel:
Sekmeler: Ürün Listesi, Stok Grafiği (henüz uygulanmadı).


Menü Çubuğu:
Dosya: Yedek al, yedekten yükle, çıkış.
Stok: Ürün ekle, stok hareketleri, stok raporları.
Cari: Cari ekle, cari listesi.
Yardım: Kullanım kılavuzu, hakkında.



3. Ürün Yönetimi

Ürün Ekle:
Menüden veya hızlı erişim butonundan "Ürün Ekle"yi seçin.
Ürün adı, barkod, stok miktarı, kritik stok, birim, fiyat, KDV oranı ve cari bilgilerini girin.

 ![Uygulama Ekran Görüntüsü](https://github.com/Ahmet1408/stok_takip/blob/main/stok_takip/ss/%C3%BCr%C3%BCn_ekle.png)


Ürün Düzenle/Sil:
Ürün listesinde bir ürüne sağ tıklayın veya çift tıklayın.
Düzenleme ekranında bilgileri güncelleyin veya silme işlemini onaylayın.


Arama:
Ürün listesi ekranında arama çubuğunu kullanarak ürün adı, barkod veya cari adına göre filtreleme yapın.



4. Cari Yönetimi

 ![Uygulama Ekran Görüntüsü](https://github.com/Ahmet1408/stok_takip/blob/main/stok_takip/ss/cari_ekle.png)

Cari Ekle:
Cari kodu, ad ve diğer bilgileri girerek yeni cari ekleyin.


Cari Listesi:
Cari listesi ekranında arama yaparak carileri filtreleyin.



5. Stok Hareketleri

 ![Uygulama Ekran Görüntüsü](https://github.com/Ahmet1408/stok_takip/blob/main/stok_takip/ss/stok_raporu.png)

Ürün ekleme sırasında otomatik stok girişi kaydedilir.
Ürün stok hareketlerini görmek için ürün listesinde sağ tıklayın ve "Stok Hareketleri"ni seçin.
Hareket tipi (giriş/çıkış), miktar, tarih ve kullanıcı bilgileri listelenir.

6. Raporlama ve Yedekleme

Raporlar:
Tüm ürünleri veya kritik stok seviyesindeki ürünleri CSV formatında dışa aktarın.


Yedekleme:
Tüm verileri (kullanıcılar, ürünler, cariler, stok hareketleri) CSV dosyasına yedekleyin.
Yedekten yükleme ile verileri geri yükleyin.




⚙️ Teknik Detaylar

Dil: Python 3
Arayüz: Tkinter
Veri Depolama: Bellekte liste tabanlı (kullanıcılar, ürünler, cariler, stok hareketleri).
Şifreleme: SHA-256
Dosya Formatı: CSV (yedekleme ve dışa aktarma için)
Yetki Seviyeleri:
1: Standart Kullanıcı
2: Admin (tam yetki)



📧 İletişim
Sorularınız veya önerileriniz için:

E-posta: efeahmet@example.com
GitHub: kullanici/stok-yonetim-sistemi



Gelişmiş Stok Yönetim Sistemi ile iş süreçlerinizi kolaylaştırın! 🚀
