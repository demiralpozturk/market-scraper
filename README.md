# 🛒 Market Fiyat Karşılaştırma Sistemi

Türk marketlerindeki ürün fiyatlarını otomatik olarak toplayan ve karşılaştıran web uygulaması.

## ✨ Özellikler

- ✅ **Garantili Veri Üretimi**: Her zaman çalışır, veri çekilemezse örnek veri kullanır
- ✅ **Otomatik Karşılaştırma**: En ucuz marketi otomatik bulur
- ✅ **Modern Web Arayüzü**: Responsive, kullanıcı dostu tasarım
- ✅ **Gerçek Zamanlı Arama**: Ürünleri anında filtrele
- ✅ **Tasarruf Hesaplama**: Ne kadar tasarruf edebileceğinizi gösterir

## 📦 Kurulum

### 1. Repoyu klonlayın
```bash
git clone https://github.com/KULLANICI_ADI/market-scraper.git
cd market-scraper
```

### 2. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 3. Scraper'ı çalıştırın
```bash
python market_scraper_v2.py
```

### 4. Web arayüzünü başlatın
```bash
python -m http.server 8000
```

Tarayıcınızda: http://localhost:8000

## 🚀 GitHub Pages ile Web'e Açma

### Otomatik Yöntem (Önerilen)

1. **GitHub'a yükleyin**:
```bash
git add .
git commit -m "İlk commit"
git push origin main
```

2. **GitHub Actions'ı etkinleştirin**:
   - Repository → Settings → Actions → General
   - "Allow all actions and reusable workflows" seçin

3. **GitHub Pages'i açın**:
   - Repository → Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: "gh-pages" seçin
   - Save

4. **İlk çalıştırma**:
   - Repository → Actions → "Market Fiyat Scraper"
   - "Run workflow" → "Run workflow"

5. **Siteniz hazır!**:
   - `https://KULLANICI_ADI.github.io/REPO_ADI/`

### Manuel Yöntem

```bash
# Scraper'ı çalıştır
python market_scraper_v2.py

# Dosyaları commit et
git add products_data.json index.html
git commit -m "Veri güncellendi"
git push

# GitHub Pages'te otomatik güncellenecek
```

## 📊 Kullanılan Marketler

- 🏪 A101
- 🏪 ŞOK
- 🏪 Migros
- 🏪 BİM

## 🔄 Otomatik Güncelleme

GitHub Actions ile:
- ✅ Her gün saat 08:00 ve 20:00'de otomatik çalışır
- ✅ Verileri otomatik günceller
- ✅ GitHub Pages'e otomatik deploy eder

## 📁 Dosya Yapısı

```
market-scraper/
├── market_scraper_v2.py      # Ana scraper
├── index.html                 # Web arayüzü
├── products_data.json         # Ürün verileri (otomatik oluşur)
├── requirements.txt           # Python bağımlılıkları
├── scraper.log               # Log dosyası (otomatik oluşur)
├── .github/
│   └── workflows/
│       └── scraper.yml       # GitHub Actions
└── README.md                 # Bu dosya
```

## 🛠️ Teknik Detaylar

### Scraper
- **Dil**: Python 3.10+
- **Kütüphaneler**: requests, beautifulsoup4
- **Veri Formatı**: JSON

### Web Arayüzü
- **Teknoloji**: Vanilla JavaScript, HTML5, CSS3
- **Responsive**: Mobil uyumlu
- **Özellikler**: 
  - Gerçek zamanlı arama
  - Otomatik yenileme (60 saniye)
  - Gradient tasarım
  - Animasyonlar

## 🔧 Sorun Giderme

### "Veri çekilemedi" hatası
```bash
# Scraper'ı manuel çalıştırın
python market_scraper_v2.py

# Log dosyasını kontrol edin
cat scraper.log
```

### GitHub Pages görünmüyor
1. Repository → Settings → Pages
2. Branch'i kontrol edin (gh-pages olmalı)
3. Actions sekmesinde workflow'un başarılı olduğunu kontrol edin

### JSON dosyası oluşmuyor
- Script'in çalıştığından emin olun
- Hata olsa bile fallback veri oluşur
- `products_data.json` dosyasının oluşup oluşmadığını kontrol edin

## 📝 Notlar

- Scraper internet bağlantısı gerektirir
- Bazı marketler bot koruması kullanabilir
- Veri çekilemezse otomatik olarak örnek veri kullanılır
- Gerçek zamanlı fiyatlar değişebilir

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yenilik`)
3. Commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yenilik`)
5. Pull Request açın

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz!

## 🎯 Gelecek Planları

- [ ] Daha fazla market ekleme
- [ ] Ürün kategorisi filtreleme
- [ ] Fiyat geçmişi grafikleri
- [ ] Email bildirimleri
- [ ] Mobil uygulama

## 📞 İletişim

Sorularınız için Issue açabilirsiniz!

---

**Not**: Bu proje eğitim amaçlıdır. Market web sitelerinin kullanım şartlarına uygun şekilde kullanın.
