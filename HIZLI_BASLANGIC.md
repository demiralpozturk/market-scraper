# 🚀 HIZLI BAŞLANGIÇ REHBERİ

## ⚡ 3 Adımda Web'e Açın!

### ADIM 1: GitHub'a Yükleyin 📤

```bash
# Yeni repo oluşturun GitHub'da
# Sonra terminal'de:

git init
git add .
git commit -m "İlk commit: Market fiyat karşılaştırma"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/market-scraper.git
git push -u origin main
```

### ADIM 2: GitHub Pages'i Aktif Edin 🌐

1. GitHub → Repository → **Settings**
2. Sol menüden **Pages**
3. **Source** → **Deploy from a branch**
4. **Branch** → **gh-pages** seçin (Actions ilk çalıştıktan sonra)
5. **Save**

### ADIM 3: İlk Çalıştırmayı Başlatın ▶️

1. GitHub → Repository → **Actions**
2. "Market Fiyat Scraper" workflow'u seçin
3. **Run workflow** → **Run workflow**

✅ **5 dakika sonra siteniz hazır!**
`https://KULLANICI_ADI.github.io/market-scraper/`

---

## 🖥️ Lokal Test (Web'e açmadan önce)

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Scraper'ı çalıştır
python market_scraper_v2.py

# 3. Web sunucusunu başlat
python -m http.server 8000

# 4. Tarayıcıda aç
# http://localhost:8000
```

---

## 📋 Dosya Açıklamaları

| Dosya | Açıklama | Gerekli mi? |
|-------|----------|-------------|
| `market_scraper_v2.py` | Veri çeken Python scripti | ✅ Evet |
| `index.html` | Web arayüzü | ✅ Evet |
| `requirements.txt` | Python bağımlılıkları | ✅ Evet |
| `products_data.json` | Ürün verileri | ⚙️ Otomatik oluşur |
| `.github/workflows/scraper.yml` | Oto güncelleme | 🔄 İsteğe bağlı |
| `README.md` | Dokümantasyon | 📖 İsteğe bağlı |

---

## 🔄 Otomatik Güncelleme Nasıl Çalışır?

1. **GitHub Actions** her gün 2 kez çalışır (08:00 ve 20:00)
2. Scraper çalışır → Fiyatları çeker
3. `products_data.json` güncellenir
4. Web sitesi otomatik yenilenir

**Manuel çalıştırma**: Actions → Run workflow

---

## 🎨 Özelleştirme

### Scraper çalışma saatini değiştir:
`.github/workflows/scraper.yml` dosyasında:
```yaml
cron: '0 8,20 * * *'  # Şu an 08:00 ve 20:00
# Değiştir:
cron: '0 */6 * * *'   # Her 6 saatte bir
cron: '0 9,12,18 * * *'  # 09:00, 12:00, 18:00
```

### Görünümü değiştir:
`index.html` dosyasındaki CSS'i düzenleyin

---

## ⚠️ Sık Sorulan Sorular

**S: "products_data.json" dosyası oluşmuyor?**
- A: Scraper'ı manuel çalıştırın: `python market_scraper_v2.py`
- Hata olsa bile fallback veri oluşur

**S: GitHub Pages çalışmıyor?**
- A: Actions sekmesinde workflow'un başarılı olduğunu kontrol edin
- `gh-pages` branch'inin oluştuğunu kontrol edin

**S: Veri güncellenmiyor?**
- A: Actions sekmesinde son çalışmayı kontrol edin
- Log'lara bakın: Actions → İlgili workflow → Detaylar

---

## 🎯 Sonuç

Artık kendi market fiyat karşılaştırma siteniz **WEB'DE CANLI!**

🌐 Site URL'niz:
`https://KULLANICI_ADI.github.io/market-scraper/`

---

**İhtiyaç olursa**: README.md dosyasında detaylı bilgi var!
