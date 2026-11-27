#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market fiyat karşılaştırma - gerçek veri

Kaynak: marketfiyati.org.tr (T.C. Ticaret Bakanlığı "Market Fiyatı" servisi).
Aynı ürünün Migros, A101, ŞOK, BİM, CarrefourSA, Hakmar ve Tarım Kredi
fiyatlarını tek kayıtta verir; ürün eşleştirmesini servis yapar.

Kurallar:
- Sahte / sabit yedek veri YOK. Veri gelmezse mevcut products_data.json
  olduğu gibi kalır ve betik hata koduyla çıkar.
- Fiyatlar değişmediyse dosyaya dokunulmaz (yalnız zaman damgası için commit olmaz).
- GitHub Actions'ta çalışırken GITHUB_OUTPUT'a changed=true/false ve count=N yazar.
"""

import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

API_URL = "https://api.marketfiyati.org.tr/api/v2/search"
SOURCE_NAME = "marketfiyati.org.tr (T.C. Ticaret Bakanlığı Market Fiyatı)"
SOURCE_URL = "https://marketfiyati.org.tr"
DATA_FILE = "products_data.json"

# Türkiye yaz/kış saati uygulamıyor: sabit UTC+3
TR_TZ = timezone(timedelta(hours=3))

# Takip edilen sepet (arama kelimeleri)
BASKET = [
    "süt 1 lt",
    "ayçiçek yağı",
    "zeytinyağı",
    "beyaz peynir",
    "kaşar peyniri",
    "yumurta",
    "tereyağı",
    "yoğurt",
    "çay 1000 gr",
    "türk kahvesi",
    "makarna",
    "pirinç",
    "bulgur",
    "kırmızı mercimek",
    "un 5 kg",
    "toz şeker",
    "domates salçası",
    "çamaşır deterjanı",
    "bulaşık deterjanı",
    "tuvalet kağıdı",
    "şampuan",
    "diş macunu",
]

PAGE_SIZE = 24
MIN_PRODUCTS = 5          # bundan az karşılaştırma çıkarsa dosya ezilmez
REQUEST_DELAY = 1.5       # istekler arası bekleme (sn) - servise yük bindirmemek için
MAX_RETRIES = 3

MARKET_NAMES = {
    "migros": "Migros",
    "a101": "A101",
    "sok": "ŞOK",
    "bim": "BİM",
    "carrefour": "CarrefourSA",
    "hakmar": "Hakmar",
    "tarim_kredi": "Tarım Kredi",
}
MARKET_ORDER = list(MARKET_NAMES.values())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def market_label(code):
    return MARKET_NAMES.get(code, str(code).replace("_", " ").title())


class MarketFiyatScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "market-fiyat-karsilastirma/2.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Language": "tr-TR,tr;q=0.9",
        })
        self.request_count = 0
        self.failed_keywords = []
        self.products = {}          # ürün id -> ürün kaydı
        self.index_times = set()

    def search(self, keyword):
        body = {"keywords": keyword, "pages": 0, "size": PAGE_SIZE}
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.request_count += 1
                r = self.session.post(API_URL, json=body, timeout=30)
                if r.status_code == 200:
                    return r.json().get("content") or []
                logger.warning(f"HTTP {r.status_code} ('{keyword}', deneme {attempt}/{MAX_RETRIES})")
                if r.status_code < 500 and r.status_code != 429:
                    return None
            except (requests.RequestException, ValueError) as e:
                logger.warning(f"İstek hatası ('{keyword}', deneme {attempt}/{MAX_RETRIES}): {e}")
            time.sleep(REQUEST_DELAY * attempt * 2)
        return None

    def add_product(self, item, scraped_at):
        pid = item.get("id")
        depots = item.get("productDepotInfoList") or []
        if not pid or pid in self.products or not depots:
            return

        # Her market için en ucuz şube fiyatı
        best = {}
        for d in depots:
            code = d.get("marketAdi")
            price = d.get("price")
            if not code or not isinstance(price, (int, float)) or price <= 0:
                continue
            if code not in best or price < best[code]["price"]:
                best[code] = d
        if len(best) < 2:
            return  # karşılaştırma için en az iki market gerekli

        name = (item.get("title") or "").strip()
        brand = (item.get("brand") or "").strip()
        prices = []
        for code, d in best.items():
            if d.get("indexTime"):
                self.index_times.add(d["indexTime"])
            prices.append({
                "market": market_label(code),
                "price": round(float(d["price"]), 2),
                "brand": brand,
                "full_name": name,
                "store": (d.get("depotName") or "").strip(),
                "unit_price": d.get("unitPrice") or "",
                "discount": bool(d.get("discount")),
                "source_time": d.get("indexTime") or "",
                "scraped_at": scraped_at,
            })
        prices.sort(key=lambda p: (p["price"], MARKET_ORDER.index(p["market"]) if p["market"] in MARKET_ORDER else 99))

        cheapest, dearest = prices[0], prices[-1]
        savings = round(dearest["price"] - cheapest["price"], 2)
        self.products[pid] = {
            "id": pid,
            "name": name,
            "category": item.get("menu_category") or item.get("main_category") or "Diğer",
            "size": item.get("refinedVolumeOrWeight") or "",
            "image": item.get("imageUrl") or "",
            "prices": prices,
            "cheapest_market": cheapest["market"],
            "cheapest_price": cheapest["price"],
            "cheapest_brand": brand,
            "max_savings": savings,
            "savings_percent": round(savings / dearest["price"] * 100, 1) if dearest["price"] else 0,
        }

    @staticmethod
    def data_hash(products):
        """Zaman damgaları hariç fiyat verisinin parmak izi."""
        rows = sorted(
            (p["id"], pr["market"], pr["price"], pr["store"], pr["discount"])
            for p in products for pr in p["prices"]
        )
        return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode("utf-8")).hexdigest()

    @staticmethod
    def load_existing_hash():
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f).get("data_hash")
        except (OSError, ValueError):
            return None

    def run(self):
        logger.info("Market fiyatları çekiliyor - kaynak: " + SOURCE_NAME)
        scraped_at = datetime.now(TR_TZ).isoformat(timespec="seconds")

        for i, kw in enumerate(BASKET):
            if i:
                time.sleep(REQUEST_DELAY)
            items = self.search(kw)
            if items is None:
                self.failed_keywords.append(kw)
                continue
            before = len(self.products)
            for item in items:
                self.add_product(item, scraped_at)
            logger.info(f"  '{kw}': {len(items)} sonuç, {len(self.products) - before} karşılaştırmalı ürün")

        products = sorted(self.products.values(), key=lambda p: (-p["max_savings"], p["name"]))
        price_count = sum(len(p["prices"]) for p in products)
        logger.info(f"Toplam: {len(products)} ürün, {price_count} fiyat, {self.request_count} istek")
        if self.failed_keywords:
            logger.warning(f"Başarısız aramalar: {', '.join(self.failed_keywords)}")

        if len(products) < MIN_PRODUCTS:
            logger.error(f"Gerçek veri yetersiz ({len(products)} ürün) - {DATA_FILE} DEĞİŞTİRİLMEDİ.")
            self.write_output(changed=False, count=len(products))
            return 1

        new_hash = self.data_hash(products)
        if new_hash == self.load_existing_hash():
            logger.info("Fiyatlarda değişiklik yok - dosyaya dokunulmadı.")
            self.write_output(changed=False, count=len(products))
            return 0

        markets = {pr["market"] for p in products for pr in p["prices"]}
        output = {
            "source": SOURCE_NAME,
            "source_url": SOURCE_URL,
            "last_updated": scraped_at,
            "price_index_time": max(self.index_times, key=_parse_index_time) if self.index_times else "",
            "total_products": len(products),
            "total_scraped": price_count,
            "total_requests": self.request_count,
            "markets": sorted(markets, key=lambda m: MARKET_ORDER.index(m) if m in MARKET_ORDER else 99),
            "data_hash": new_hash,
            "products": products,
        }
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_FILE)
        logger.info(f"{DATA_FILE} güncellendi ({len(products)} ürün, {len(markets)} market).")
        for p in products[:5]:
            logger.info(f"  {p['name']}: en ucuz {p['cheapest_market']} {p['cheapest_price']:.2f} TL, fark {p['max_savings']:.2f} TL")
        self.write_output(changed=True, count=len(products))
        return 0

    @staticmethod
    def write_output(changed, count):
        path = os.environ.get("GITHUB_OUTPUT")
        if path:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"changed={'true' if changed else 'false'}\n")
                f.write(f"count={count}\n")


def _parse_index_time(s):
    try:
        return datetime.strptime(s, "%d.%m.%Y %H:%M")
    except ValueError:
        return datetime.min


if __name__ == "__main__":
    sys.exit(MarketFiyatScraper().run())
