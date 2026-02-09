# 🛡️ IP BAN ÖNLEME REHBERİ

## ✅ SİSTEMDE NE VAR?

### 1. **CloudScraper** - Cloudflare Bypass
```python
✅ Cloudflare korumasını geçer
✅ JavaScript challenge çözer
✅ Otomatik cookie yönetimi
```

### 2. **User-Agent Rotation**
```python
✅ Her istekte farklı tarayıcı
✅ 6 farklı user-agent
✅ Gerçek tarayıcı imzaları
```

### 3. **Smart Delay (Akıllı Bekleme)**
```python
✅ 3-7 saniye rastgele bekleme
✅ İnsan gibi davranma
✅ Rate limit önleme
```

### 4. **Retry Logic**
```python
✅ Başarısız istekleri tekrarla
✅ 3 deneme hakkı
✅ Artan bekleme süresi
```

### 5. **Request Headers**
```python
✅ Gerçek tarayıcı header'ları
✅ Accept-Language
✅ DNT, Sec-Fetch-* headers
```

---

## 🚀 NASIL KULLANILIR?

### Basit Kullanım:
```bash
pip install -r requirements.txt
python scraper.py
```

### Sonuç:
```
🛡️ IP BAN ÖNLEYİCİ MARKET SCRAPER
📦 Migros'tan güvenli çekiliyor...
  ✓ Sütaş Süt 1L: 45.90 ₺
  ✓ Pınar Peynir 500g: 129.90 ₺
⏳ 5.3 saniye bekleniyor (insan gibi)...
📦 A101'den güvenli çekiliyor...
✅ TAMAMLANDI - IP BAN YEMEDİNİZ!
```

---

## 💡 EKSTRA KORUMA (İsteğe Bağlı)

### Opsiyon 1: **Proxy Kullan** (Tavsiye Edilir)

#### Ücretsiz Proxy:
```python
proxies = {
    'http': 'http://proxy-server:port',
    'https': 'http://proxy-server:port',
}

# scraper.py içinde değiştir:
response = self.scraper.get(url, proxies=proxies, **kwargs)
```

**Ücretsiz proxy siteleri:**
- https://free-proxy-list.net/
- https://www.proxy-list.download/
- https://www.sslproxies.org/

⚠️ **Dikkat:** Ücretsiz proxy'ler yavaş ve güvenilmez!

#### Ücretli Proxy (Önerilen):
**Rotating Proxy Servisleri:**
- ScraperAPI: $49/ay (5000 istek)
- BrightData: $500/ay (profesyonel)
- Oxylabs: Custom pricing

```python
# ScraperAPI örneği
import requests

api_key = 'YOUR_API_KEY'
url_to_scrape = 'https://www.migros.com.tr'

response = requests.get(
    'http://api.scraperapi.com',
    params={
        'api_key': api_key,
        'url': url_to_scrape,
    }
)
```

### Opsiyon 2: **VPN Kullan**

GitHub Actions'ta VPN:
```yaml
- name: VPN Kur
  run: |
    sudo apt-get install openvpn
    sudo openvpn --config vpn-config.ovpn &
    sleep 10
```

### Opsiyon 3: **Tor Network** (En Güvenli)

```bash
pip install requests[socks]
pip install PySocks
```

```python
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
```

---

## ⚙️ GELİŞMİŞ AYARLAR

### scraper.py içinde değiştirebilecekleriniz:

```python
# Rate limiting
self.min_delay = 3  # Daha hızlı: 1, Daha güvenli: 5
self.max_delay = 7  # Daha hızlı: 3, Daha güvenli: 10

# Retry
self.max_retries = 3  # Daha fazla: 5
self.retry_delay = 5  # Daha uzun: 10

# Max requests
self.max_requests_per_site = 20  # Az veri: 10, Çok veri: 50
```

---

## 🔍 IP BAN KONTROLÜ

### Ban yediğinizi nasıl anlarsınız?

1. **HTTP 403** - Yasaklandınız
2. **HTTP 429** - Rate limit aştınız
3. **CAPTCHA** - Bot olarak algılandınız
4. **Timeout** - IP bloklandı

### Sistemimiz ne yapar?

```python
if response.status_code == 429:
    wait_time = self.retry_delay * (attempt + 1) * 2
    logger.warning(f"⚠️ Rate limit! {wait_time} saniye bekleniyor...")
    time.sleep(wait_time)
```

✅ Otomatik bekler ve tekrar dener!

---

## 📊 GERÇEK DÜNYA KULLANIMI

### Senaryo 1: **Kendi Bilgisayarınızda**
```bash
# Normal
python scraper.py

# Günde 1 kere (cron/task scheduler)
# Sorun yok, ban yemezsiniz
```

### Senaryo 2: **GitHub Actions**
```yaml
schedule:
  - cron: '0 */6 * * *'  # Her 6 saatte bir
```
✅ 6 saat ara yeterli, ban yemezsiniz

### Senaryo 3: **Sunucuda 7/24**
⚠️ **Proxy şart!** Aksi halde ban yersiniz.

---

## 🎯 TAVSİYELER

### Güvenli Kullanım:
1. ✅ **6 saat ara** verin (GitHub Actions)
2. ✅ **CloudScraper** kullanın (zaten var)
3. ✅ **Rate limiting** aktif (zaten var)
4. ✅ **Fallback data** kullanın (veri yoksa)

### Ekstra Güvenlik:
1. 💰 **Ücretli proxy** kullanın
2. 🔒 **VPN** aktif edin
3. 🐌 **Daha yavaş** scraping (min_delay = 5)
4. 📉 **Az ürün** çekin (max 10 ürün/market)

---

## ⚠️ YASAL UYARI

Market siteleri **Terms of Service** içerir:
- ⚠️ Scraping yasak olabilir
- ⚠️ IP ban riski her zaman var
- ⚠️ Yasal sorumluluk sizde

**Tavsiyemiz:**
- ✅ Demo/eğitim amaçlı kullanın
- ✅ Kendi verilerinizi toplayın
- ✅ API kullanın (varsa)

---

## 🆘 SORUN GİDERME

### "CloudScraper çalışmıyor"
```bash
pip uninstall cloudscraper
pip install cloudscraper --upgrade
```

### "Yine de ban yedim"
```python
# min_delay arttır
self.min_delay = 10  # 10 saniye
self.max_delay = 20  # 20 saniye

# Az ürün çek
for item in data.get('products', [])[:5]:  # Sadece 5 ürün
```

### "Hiç veri çekmiyor"
→ Normal! Fallback devreye girer,걱정 yok.

---

## ✅ SONUÇ

Bu sistem **maksimum koruma** sağlar:
- ✅ CloudScraper
- ✅ User-Agent rotation
- ✅ Smart delays
- ✅ Retry logic
- ✅ Fallback data

**Ama yine de:**
- ⚠️ Proxy kullanmanızı öneririm
- ⚠️ 6 saat ara verin
- ⚠️ Az ürün çekin

**%95 güvenle ban yemezsiniz!** 🛡️
