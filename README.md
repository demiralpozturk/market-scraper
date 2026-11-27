# 🛒 Market Fiyat Karşılaştırma · Turkish Supermarket Price Comparison

[![Fiyat güncelleme / Price update](https://github.com/demiralpozturk/market-scraper/actions/workflows/scraper.yml/badge.svg)](https://github.com/demiralpozturk/market-scraper/actions/workflows/scraper.yml)
[![Son veri / Last data](https://img.shields.io/github/last-commit/demiralpozturk/market-scraper/main?path=products_data.json&label=son%20veri%20%2F%20last%20data)](https://github.com/demiralpozturk/market-scraper/commits/main/products_data.json)
[![Canlı sayfa / Live page](https://img.shields.io/badge/canl%C4%B1%20sayfa-live%20page-0f766e)](https://demiralpozturk.github.io/market-scraper/)
[![License: MIT](https://img.shields.io/github/license/demiralpozturk/market-scraper)](LICENSE)

**🔗 Canlı sayfa / Live page: https://demiralpozturk.github.io/market-scraper/**

> [!NOTE]
> **Fiyatlar T.C. Ticaret Bakanlığı marketfiyati.org.tr'nin mağaza (şube) verisidir; online mağaza fiyatlarından ve diğer şubelerden farklı olabilir.**
> Prices are in-store (branch) data from the Turkish Ministry of Trade's marketfiyati.org.tr; they may differ from online-store prices and from other branches.
> Hatalı bir fiyat mı gördünüz? / Spotted a wrong price? → [Hatalı fiyat bildir / Report a wrong price](https://github.com/demiralpozturk/market-scraper/issues/new?template=hatali-fiyat.yml)

Creator: **Demiralp Öztürk** · [GitHub](https://github.com/demiralpozturk) · [LinkedIn](https://www.linkedin.com/in/demiralp-%C3%B6zt%C3%BCrk/)

[Türkçe](#türkçe) · [English](#english)

---

## Türkçe

Aynı ürünün **Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar** ve **Tarım Kredi** fiyatlarını yan yana gösterir ve en ucuz marketi öne çıkarır. Veriler gerçektir, 6 saatte bir GitHub Actions ile otomatik güncellenir ve herkesin kullanabileceği açık bir JSON dosyası olarak yayınlanır.

### Ne yapar?

- Bir alışveriş sepetindeki ürünleri (süt, yağ, peynir, çay, makarna, deterjan…) resmi **[marketfiyati.org.tr](https://marketfiyati.org.tr)** (T.C. Ticaret Bakanlığı Market Fiyatı) servisinden sorgular.
- Servis aynı ürünü marketler arasında eşleştirir; bu proje en az **iki markette** satılan ürünleri alır ve her market için en düşük fiyatlı şubeyi seçer.
- Her fiyat için güncel fiyatı, **indirimsiz normal fiyatı** ve indirim oranını kaydeder. "En ucuz" karşılaştırması varsayılan olarak **normal fiyata göre** yapılır; indirimler ayrıca gösterilir (üstü çizili normal fiyat + "%57 indirim"). Sayfadaki **İndirimleri dahil et** seçeneğiyle indirimli fiyatlara göre karşılaştırılabilir.
- Sonucu [`products_data.json`](https://demiralpozturk.github.io/market-scraper/products_data.json) olarak kaydeder; [canlı sayfa](https://demiralpozturk.github.io/market-scraper/) bu dosyayı arama, kategori filtresi ve sıralamayla gösterir. Her fiyatın altında şube adı ve veri saati yazar.
- Her ürün kartındaki **Hatalı fiyat bildir** bağlantısı, ürün/market/şube/fiyat bilgileri doldurulmuş bir GitHub bildirimi açar.
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

- Fiyatlar **mağaza (şube) verisidir** ve şubeye göre değişir; online mağaza fiyatlarından farklı olabilir. Servis varsayılan konumu için (şu an İstanbul, Anadolu yakası) şube fiyatlarını döndürür; her satırda şube adı ve veri saati gösterilir.
- Kaynaktaki bazı kayıtlar hatalı olabilir (ör. çok yüksek indirim, o markette rafta olmayan ürün). Bu proje veriyi değiştirmez; böyle bir durumda lütfen **Hatalı fiyat bildir** ile bildirin.
- Yalnızca servisin **en az iki markette eşleştirdiği** ürünler listelenir; her arama için ilk 24 sonuç alınır.
- Veri en fazla 6 saatte bir yenilenir; kaynaktaki fiyat zamanı JSON'da `price_index_time` alanındadır.
- Bu proje marketlerle veya T.C. Ticaret Bakanlığı ile **bağlantılı değildir**; fiyatlar bilgi amaçlıdır, kasadaki fiyat esastır.
- Kaynak servis arayüzünü değiştirirse güncelleme durabilir. Bu durumda Actions kırmızı görünür ve sayfadaki son veri korunur.

---

## English

Compares the prices of the **same product** across Turkish supermarket chains (**Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar, Tarım Kredi**) and highlights the cheapest one. The data is real, refreshed every 6 hours by GitHub Actions, and published as an open JSON file anyone can use.

### What it does

- Queries a shopping basket (milk, oil, cheese, tea, pasta, detergent…) from the official **[marketfiyati.org.tr](https://marketfiyati.org.tr)** service run by the Turkish Ministry of Trade.
- The service matches the same product across chains; this project keeps products sold in **at least two chains** and picks the lowest-priced store per chain.
- Stores the current price, the **regular (non-discounted) price** and the discount ratio for each price. "Cheapest" is decided by the **regular price** by default; discounts are shown separately (struck-through regular price + "57% off" badge). The **İndirimleri dahil et** (include discounts) switch compares discounted prices instead.
- Writes the result to [`products_data.json`](https://demiralpozturk.github.io/market-scraper/products_data.json); the [live page](https://demiralpozturk.github.io/market-scraper/) renders it with search, category filter and sorting. Each price shows its store name and data time.
- The **Hatalı fiyat bildir** (report a wrong price) link on every card opens a GitHub issue pre-filled with product, chain, store and price.
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

- Prices are **in-store (branch) data** and vary by store; they may differ from online-store prices. The service returns prices for stores around its default location (currently Istanbul, Asian side); every row shows the store name and data time.
- Some source records may be wrong (e.g. an unusually large discount, or a product that is not on that chain's shelves). This project does not alter the data; please report such cases with **Hatalı fiyat bildir**.
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
  "notice": "Fiyatlar … mağaza (şube) verisidir; …",  // sayfada gösterilen not / notice shown on the page
  "price_basis": "regular_price",                 // cheapest_* ve max_savings normal fiyata göre / based on regular price
  "last_updated": "2026-11-27T17:19:20+03:00",    // fiyatların değiştiği son çekim / last scrape with changed prices (TR time)
  "price_index_time": "27.11.2026 12:11",         // kaynaktaki fiyat zamanı / source price timestamp
  "total_products": 72,                           // karşılaştırılan ürün / compared products
  "total_scraped": 174,                           // toplam fiyat satırı / total price rows
  "total_requests": 22,
  "markets": ["Migros", "A101", "ŞOK", "BİM", "CarrefourSA", "Hakmar"],
  "data_hash": "…",                               // zaman damgaları hariç parmak izi / fingerprint without timestamps
  "products": [
    {
      "id": "1R0P",                               // kaynaktaki ürün kimliği / source product id
      "name": "Colgate Optik Beyaz Diş Macunu 75 Ml",
      "category": "Kişisel Bakım",
      "size": "75 ML",
      "image": "https://cdn.marketfiyati.org.tr/…",  // boş olabilir / may be empty
      "cheapest_market": "Migros",                // normal fiyata göre en ucuz / cheapest by regular price
      "cheapest_price": 356.95,
      "cheapest_brand": "Colgate",
      "max_savings": 103.0,                       // normal fiyatlarla en pahalı − en ucuz / by regular prices (TRY)
      "savings_percent": 22.4,                    // en pahalıya göre % / % of the most expensive
      "has_discount": true,                       // en az bir markette indirim var / any discounted price
      "best_deal_market": "CarrefourSA",          // indirimler dahil en ucuz / cheapest incl. discounts
      "best_deal_price": 200.0,
      "prices": [                                 // normal fiyata göre ucuzdan pahalıya / sorted by regular price
        {
          "market": "Migros",
          "price": 356.95,                        // güncel fiyat, indirim dahil (TRY) / current price incl. discount
          "regular_price": 356.95,                // indirimsiz normal fiyat / regular price (source: discountlessPrice)
          "discount": false,                      // regular_price > price
          "discount_ratio": 0,                    // kaynaktaki discountRatio (0–1) / source discountRatio
          "brand": "Colgate",
          "full_name": "Colgate Optik Beyaz Diş Macunu 75 Ml",
          "store": "Kadıköy Caferağa M Migros",   // şube / store
          "unit_price": "4.759,33 ₺/Lt",
          "source_time": "27.11.2026 12:10",      // kaynaktaki veri saati / source data time
          "scraped_at": "2026-11-27T17:19:20+03:00"
        },
        {
          "market": "CarrefourSA",
          "price": 200.0,
          "regular_price": 459.95,
          "discount": true,
          "discount_ratio": 0.5652,               // %57 indirim / 57% off
          "store": "Istanbul Acıbadem Hıper",
          "source_time": "27.11.2026 12:10"
          // … diğer alanlar yukarıdaki gibi / other fields as above
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
| `.github/ISSUE_TEMPLATE/hatali-fiyat.yml` | Hatalı fiyat bildirim formu / wrong-price report form |

## Lisans / License

[MIT](LICENSE) © 2026 Demiralp Öztürk

Creator: **Demiralp Öztürk** · [GitHub](https://github.com/demiralpozturk) · [LinkedIn](https://www.linkedin.com/in/demiralp-%C3%B6zt%C3%BCrk/)

Fiyat verisinin kaynağı / Price data source: [marketfiyati.org.tr](https://marketfiyati.org.tr)
