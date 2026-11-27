# 🛒 Market Fiyat Karşılaştırma · Turkish Supermarket Price Comparison

[![Fiyat güncelleme / Price update](https://github.com/demiralpozturk/market-scraper/actions/workflows/scraper.yml/badge.svg)](https://github.com/demiralpozturk/market-scraper/actions/workflows/scraper.yml)
[![Son veri / Last data](https://img.shields.io/github/last-commit/demiralpozturk/market-scraper/main?path=products_data.json&label=son%20veri%20%2F%20last%20data)](https://github.com/demiralpozturk/market-scraper/commits/main/products_data.json)
[![Canlı sayfa / Live page](https://img.shields.io/badge/canl%C4%B1%20sayfa-live%20page-0f766e)](https://demiralpozturk.github.io/market-scraper/)
[![License: MIT](https://img.shields.io/github/license/demiralpozturk/market-scraper)](LICENSE)

**🔗 Canlı sayfa / Live page: https://demiralpozturk.github.io/market-scraper/**

[Türkçe](#türkçe) · [English](#english)

---

## Türkçe

Aynı ürünün **Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar** ve **Tarım Kredi** fiyatlarını yan yana gösterir ve en ucuz marketi öne çıkarır. Veriler gerçektir, 6 saatte bir GitHub Actions ile otomatik güncellenir ve herkesin kullanabileceği açık bir JSON dosyası olarak yayınlanır.

### Ne yapar?

- Bir alışveriş sepetindeki ürünleri (süt, yağ, peynir, çay, makarna, deterjan…) resmi **[marketfiyati.org.tr](https://marketfiyati.org.tr)** (T.C. Ticaret Bakanlığı Market Fiyatı) servisinden sorgular.
- Servis aynı ürünü marketler arasında eşleştirir; bu proje en az **iki markette** satılan ürünleri alır ve her market için en ucuz şube fiyatını seçer.
- Sonucu [`products_data.json`](https://demiralpozturk.github.io/market-scraper/products_data.json) olarak kaydeder; [canlı sayfa](https://demiralpozturk.github.io/market-scraper/) bu dosyayı arama, kategori filtresi ve sıralamayla gösterir.
- **Sahte/yedek veri yoktur.** Veri alınamazsa son gerçek veri korunur ve iş hata verir. Fiyatlar değişmediyse commit atılmaz.

### Veriyi kullanmak

Herkese açık adres: **`https://demiralpozturk.github.io/market-scraper/products_data.json`**

```js
const data = await (await fetch('https://demiralpozturk.github.io/market-scraper/products_data.json')).json();
console.log(data.products[0].name, data.products[0].cheapest_market, data.products[0].cheapest_price);
```

Alanların açıklaması için [Veri şeması / Data schema](#veri-şeması--data-schema) bölümüne bakın.

### Kendi kopyanı çalıştır

1. Bu repoyu **fork**'la.
2. Fork'ta **Actions** sekmesini aç ve iş akışlarını etkinleştir.
3. **Actions → "Market Fiyat Güncelleme" → Run workflow** ile ilk çalıştırmayı yap (`gh-pages` dalı oluşur).
4. **Settings → Pages → Branch: `gh-pages` / root** seçip kaydet. Sayfan `https://<kullanıcı-adın>.github.io/market-scraper/` adresinde açılır.
5. Takip edilen ürünleri değiştirmek için `scraper.py` içindeki `BASKET` listesini düzenle.

Yerelde:

```bash
pip install -r requirements.txt
python scraper.py              # products_data.json'u günceller
python -m http.server 8000     # sayfayı http://localhost:8000 adresinden aç
```

### Sınırlamalar

- Fiyatlar **şubeye göre** değişir. Servis varsayılan konumu için (şu an İstanbul, Anadolu yakası) şube fiyatlarını döndürür; her satırda şube adı gösterilir.
- Yalnızca servisin **en az iki markette eşleştirdiği** ürünler listelenir; her arama için ilk 24 sonuç alınır.
- Veri en fazla 6 saatte bir yenilenir; kaynaktaki fiyat zamanı JSON'da `price_index_time` alanındadır.
- Bu proje marketlerle veya T.C. Ticaret Bakanlığı ile **bağlantılı değildir**; fiyatlar bilgi amaçlıdır, kasadaki fiyat esastır.
- Kaynak servis arayüzünü değiştirirse güncelleme durabilir. Bu durumda Actions kırmızı görünür ve sayfadaki son veri korunur.

---

## English

Compares the prices of the **same product** across Turkish supermarket chains (**Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar, Tarım Kredi**) and highlights the cheapest one. The data is real, refreshed every 6 hours by GitHub Actions, and published as an open JSON file anyone can use.

### What it does

- Queries a shopping basket (milk, oil, cheese, tea, pasta, detergent…) from the official **[marketfiyati.org.tr](https://marketfiyati.org.tr)** service run by the Turkish Ministry of Trade.
- The service matches the same product across chains; this project keeps products sold in **at least two chains** and picks the cheapest store price per chain.
- Writes the result to [`products_data.json`](https://demiralpozturk.github.io/market-scraper/products_data.json); the [live page](https://demiralpozturk.github.io/market-scraper/) renders it with search, category filter and sorting.
- **No fake or fallback data.** If fetching fails, the last real data is kept and the workflow fails visibly. Nothing is committed when prices did not change.

### Using the data

Public URL: **`https://demiralpozturk.github.io/market-scraper/products_data.json`**

```python
import requests
data = requests.get("https://demiralpozturk.github.io/market-scraper/products_data.json").json()
for p in data["products"][:5]:
    print(p["name"], "->", p["cheapest_market"], p["cheapest_price"], "TRY")
```

### Run your own copy

1. **Fork** this repository.
2. Open the **Actions** tab in your fork and enable workflows.
3. Run **Actions → "Market Fiyat Güncelleme" → Run workflow** once (this creates the `gh-pages` branch).
4. Go to **Settings → Pages → Branch: `gh-pages` / root** and save. Your page will be at `https://<your-username>.github.io/market-scraper/`.
5. Edit the `BASKET` list in `scraper.py` to track other products.

Locally:

```bash
pip install -r requirements.txt
python scraper.py              # updates products_data.json
python -m http.server 8000     # open http://localhost:8000
```

### Limitations

- Prices are **store-specific**. The service returns prices for stores around its default location (currently Istanbul, Asian side); every row shows the store name.
- Only products the service **matches in at least two chains** are listed; the first 24 results per search term are used.
- Data refreshes at most every 6 hours; the source's own price timestamp is in `price_index_time`.
- This project is **not affiliated** with any supermarket chain or the Turkish Ministry of Trade. Prices are informational; the shelf price is what counts.
- If the source service changes its API, updates may stop. The workflow then fails visibly and the last real data stays online.

---

## Veri şeması / Data schema

```jsonc
{
  "source": "marketfiyati.org.tr (T.C. Ticaret Bakanlığı Market Fiyatı)",
  "source_url": "https://marketfiyati.org.tr",
  "last_updated": "2026-11-27T16:09:33+03:00",   // fiyatların değiştiği son çekim / last scrape with changed prices (TR time)
  "price_index_time": "27.11.2026 12:11",        // kaynaktaki fiyat zamanı / source price timestamp
  "total_products": 72,                          // karşılaştırılan ürün / compared products
  "total_scraped": 174,                          // toplam fiyat satırı / total price rows
  "total_requests": 22,
  "markets": ["Migros", "A101", "ŞOK", "BİM", "CarrefourSA", "Hakmar"],
  "data_hash": "…",                              // zaman damgaları hariç parmak izi / fingerprint without timestamps
  "products": [
    {
      "id": "1ZVP",                              // kaynaktaki ürün kimliği / source product id
      "name": "Hasata Basmati Pirinç 1 Kg",
      "category": "Temel Gıda",
      "size": "1 KG",
      "image": "https://cdn.marketfiyati.org.tr/…",  // boş olabilir / may be empty
      "cheapest_market": "A101",
      "cheapest_price": 132.5,
      "cheapest_brand": "Hasata",
      "max_savings": 107.45,                     // en pahalı − en ucuz / most expensive − cheapest (TRY)
      "savings_percent": 44.8,                   // en pahalıya göre % / % of the most expensive
      "prices": [                                // ucuzdan pahalıya / cheapest first
        {
          "market": "A101",
          "price": 132.5,                        // TRY
          "brand": "Hasata",
          "full_name": "Hasata Basmati Pirinç 1 Kg",
          "store": "Adem Yavuz Ümraniye Istanbul",
          "unit_price": "132,50 ₺/Kg",
          "discount": false,
          "source_time": "27.11.2026 12:10",
          "scraped_at": "2026-11-27T16:09:33+03:00"
        }
      ]
    }
  ]
}
```

## Dosyalar / Files

| Dosya / File | Açıklama / Description |
| --- | --- |
| `scraper.py` | Veri çekme / data fetcher (`BASKET` = takip edilen ürünler / tracked products) |
| `index.html` | Karşılaştırma sayfası / comparison page (bağımlılık yok / no dependencies) |
| `products_data.json` | Son gerçek veri / latest real data |
| `.github/workflows/scraper.yml` | 6 saatte bir çalışır, PR'ları test eder / runs every 6 hours, tests pull requests |

## Lisans / License

[MIT](LICENSE) © 2026 [Demiralp Öztürk](https://github.com/demiralpozturk)

Fiyat verisinin kaynağı / Price data source: [marketfiyati.org.tr](https://marketfiyati.org.tr)
