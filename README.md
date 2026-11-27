# 🛒 Market Fiyat Karşılaştırma

Aynı ürünün farklı marketlerdeki **gerçek** fiyatlarını karşılaştırır ve en çok tasarruf sağlayan ürünleri listeler.

🔗 Site: https://demiralpozturk.github.io/market-scraper/

## Veri kaynağı

Fiyatlar **[marketfiyati.org.tr](https://marketfiyati.org.tr)** (T.C. Ticaret Bakanlığı "Market Fiyatı" servisi) üzerinden alınır.
Servis aynı ürünü marketler arasında eşleştirir; bu proje her market için en ucuz şube fiyatını gösterir.

Kapsanan marketler: **Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar, Tarım Kredi** (servisin o an döndürdüğü kadarıyla).

> Fiyatlar şubeye göre değişebilir. Her fiyat kaydında şube adı, birim fiyat, indirim bilgisi ve kaynaktaki fiyat zamanı tutulur.

## Nasıl çalışır?

1. `scraper.py`, sepetteki arama kelimelerini (süt, yağ, peynir, çay, makarna, deterjan…) servise sorar.
2. En az **iki markette** fiyatı olan ürünleri alır, her market için en ucuz fiyatı seçer.
3. Sonucu `products_data.json` dosyasına yazar; `index.html` bu dosyayı gösterir.

Kurallar:

- **Sahte / sabit yedek veri yoktur.** Veri gelmezse mevcut dosya korunur ve iş hata verir (Actions'ta kırmızı görünür).
- Fiyatlar değişmediyse dosyaya dokunulmaz; **yalnızca fiyat değişince commit** atılır.

## Otomatik güncelleme

`.github/workflows/scraper.yml` her 6 saatte bir çalışır (Actions → "Market Fiyat Güncelleme" → *Run workflow* ile elle de çalıştırılabilir).
Fiyatlar değiştiyse `products_data.json` commit'lenir ve site `gh-pages` dalına yayınlanır.

## Yerelde çalıştırma

```bash
pip install -r requirements.txt
python scraper.py
# sonra index.html'i bir yerel sunucuyla açın, ör.: python -m http.server
```

Takip edilen ürünleri değiştirmek için `scraper.py` içindeki `BASKET` listesini düzenleyin.

## Dosyalar

```
scraper.py                  # veri çekme
index.html                  # karşılaştırma sayfası
products_data.json          # son gerçek veri
requirements.txt
.github/workflows/scraper.yml
```
