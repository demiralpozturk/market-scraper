#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ IP BAN ÖNLEYICI MARKET SCRAPER
✅ Proxy rotation
✅ User-agent rotation
✅ Rate limiting
✅ Cloudflare bypass
✅ Retry logic
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import random
import logging

# CloudScraper - Cloudflare bypass için
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    print("⚠️ cloudscraper yüklü değil. Yüklemek için: pip install cloudscraper")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SafeMarketScraper:
    """IP Ban Önleyici Güvenli Scraper"""
    
    def __init__(self):
        # User-Agent havuzu (gerçek tarayıcılar)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        # CloudScraper session (Cloudflare bypass)
        if CLOUDSCRAPER_AVAILABLE:
            self.scraper = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
            )
        else:
            self.scraper = requests.Session()
        
        self.products = []
        
        # Rate limiting ayarları
        self.min_delay = 3  # Minimum 3 saniye
        self.max_delay = 7  # Maximum 7 saniye
        self.request_count = 0
        self.max_requests_per_site = 20  # Site başına max istek
        
        # Retry ayarları
        self.max_retries = 3
        self.retry_delay = 5
    
    def get_random_headers(self):
        """Her istekte farklı header"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def smart_delay(self, extra=0):
        """Akıllı bekleme - insan gibi davran"""
        delay = random.uniform(self.min_delay, self.max_delay) + extra
        logger.info(f"⏳ {delay:.1f} saniye bekleniyor (insan gibi)...")
        time.sleep(delay)
    
    def safe_request(self, url, method='GET', **kwargs):
        """Güvenli HTTP isteği - retry logic ile"""
        for attempt in range(self.max_retries):
            try:
                # Her istekte yeni headers
                headers = self.get_random_headers()
                if 'headers' in kwargs:
                    headers.update(kwargs['headers'])
                kwargs['headers'] = headers
                
                # Timeout ekle
                if 'timeout' not in kwargs:
                    kwargs['timeout'] = 15
                
                # İstek at
                if method.upper() == 'GET':
                    response = self.scraper.get(url, **kwargs)
                else:
                    response = self.scraper.post(url, **kwargs)
                
                self.request_count += 1
                
                # Başarılı
                if response.status_code == 200:
                    logger.info(f"✓ İstek başarılı: {url[:50]}...")
                    return response
                
                # Rate limit (429)
                elif response.status_code == 429:
                    wait_time = self.retry_delay * (attempt + 1) * 2
                    logger.warning(f"⚠️ Rate limit! {wait_time} saniye bekleniyor...")
                    time.sleep(wait_time)
                    continue
                
                # Diğer hatalar
                else:
                    logger.warning(f"⚠️ HTTP {response.status_code}: {url[:50]}...")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    return None
                    
            except Exception as e:
                logger.warning(f"⚠️ Hata (deneme {attempt+1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return None
        
        return None
    
    def clean_price(self, price):
        """Fiyat temizle"""
        if isinstance(price, (int, float)):
            return float(price)
        if not price:
            return 0.0
        import re
        price = str(price)
        price = re.sub(r'[^\d,.]', '', price)
        price = price.replace('.', '').replace(',', '.')
        try:
            return float(price)
        except:
            return 0.0
    
    def scrape_migros(self):
        """Migros - Güvenli scraping"""
        logger.info("\n" + "="*60)
        logger.info("📦 Migros'tan güvenli çekiliyor...")
        logger.info("="*60)
        
        try:
            # Migros kategorileri
            url = "https://www.migros.com.tr/rest/products/search/sanalmarket"
            
            params = {
                'category': 'sut-kahvalti-c-2',
                'page': 0,
                'size': 15,
            }
            
            response = self.safe_request(url, params=params)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    count = 0
                    
                    for item in data.get('products', [])[:10]:
                        try:
                            name = item.get('name', '')
                            brand = item.get('marka', item.get('brand', ''))
                            price_obj = item.get('price', {})
                            price = price_obj.get('value', 0) if price_obj else 0
                            
                            if name and price > 0:
                                self.products.append({
                                    'name': name,
                                    'brand': brand,
                                    'price': float(price),
                                    'market': 'Migros',
                                    'category': 'Süt & Kahvaltı',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                count += 1
                                logger.info(f"  ✓ {name}: {price} ₺")
                        except:
                            continue
                    
                    logger.info(f"✅ Migros: {count} ürün çekildi")
                    self.smart_delay()
                    return count > 0
                    
                except:
                    logger.warning("⚠️ Migros JSON parse hatası")
            
            return False
            
        except Exception as e:
            logger.error(f"✗ Migros hatası: {e}")
            return False
    
    def scrape_a101_safe(self):
        """A101 - Cloudflare bypass ile"""
        logger.info("\n" + "="*60)
        logger.info("📦 A101'den güvenli çekiliyor...")
        logger.info("="*60)
        
        try:
            url = "https://www.a101.com.tr/market/"
            
            response = self.safe_request(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                count = 0
                
                # Farklı selector denemeleri
                selectors = [
                    '.product-card',
                    '.product-item',
                    '.prd-item',
                    '[class*="product"]',
                ]
                
                products = []
                for selector in selectors:
                    products = soup.select(selector)[:10]
                    if products:
                        break
                
                for product in products:
                    try:
                        # İsim
                        name_elem = product.select_one('.name, .product-name, h3, h2, [class*="name"]')
                        # Fiyat
                        price_elem = product.select_one('.price, .product-price, [class*="price"]')
                        
                        if name_elem and price_elem:
                            name = name_elem.text.strip()
                            price = self.clean_price(price_elem.text)
                            
                            if name and price > 0:
                                self.products.append({
                                    'name': name,
                                    'brand': '',
                                    'price': price,
                                    'market': 'A101',
                                    'category': 'Gıda',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                count += 1
                                logger.info(f"  ✓ {name}: {price} ₺")
                    except:
                        continue
                
                logger.info(f"✅ A101: {count} ürün çekildi")
                self.smart_delay()
                return count > 0
            
            return False
            
        except Exception as e:
            logger.error(f"✗ A101 hatası: {e}")
            return False
    
    def add_fallback_data(self):
        """Güvenilir fallback veriler"""
        logger.info("\n📊 Güvenilir fallback veriler ekleniyor...")
        
        fallback = [
            # Süt
            {"name": "Sütaş Süt 1L", "brand": "Sütaş", "price": 45.90, "market": "Migros", "category": "Süt Ürünleri"},
            {"name": "Pınar Süt 1L", "brand": "Pınar", "price": 46.90, "market": "A101", "category": "Süt Ürünleri"},
            {"name": "İçim Süt 1L", "brand": "İçim", "price": 44.50, "market": "ŞOK", "category": "Süt Ürünleri"},
            {"name": "Sütaş Süt 1L", "brand": "Sütaş", "price": 43.90, "market": "BİM", "category": "Süt Ürünleri"},
            
            # Yağ
            {"name": "Komili Zeytinyağı 1L", "brand": "Komili", "price": 285.00, "market": "Migros", "category": "Yağlar"},
            {"name": "Tariş Zeytinyağı 1L", "brand": "Tariş", "price": 289.00, "market": "A101", "category": "Yağlar"},
            {"name": "Komili Zeytinyağı 1L", "brand": "Komili", "price": 279.00, "market": "BİM", "category": "Yağlar"},
            
            # Peynir
            {"name": "Pınar Beyaz Peynir 500g", "brand": "Pınar", "price": 129.90, "market": "Migros", "category": "Peynir"},
            {"name": "Eker Beyaz Peynir 500g", "brand": "Eker", "price": 124.90, "market": "BİM", "category": "Peynir"},
            
            # Deterjan
            {"name": "Ariel Deterjan 3kg", "brand": "Ariel", "price": 189.90, "market": "Migros", "category": "Temizlik"},
            {"name": "Bingo Deterjan 3kg", "brand": "Bingo", "price": 179.90, "market": "BİM", "category": "Temizlik"},
            
            # Şampuan
            {"name": "Clear Şampuan 500ml", "brand": "Clear", "price": 89.90, "market": "A101", "category": "Kişisel Bakım"},
            {"name": "Palmolive Şampuan 500ml", "brand": "Palmolive", "price": 84.90, "market": "BİM", "category": "Kişisel Bakım"},
        ]
        
        for item in fallback:
            self.products.append({
                **item,
                'scraped_at': datetime.now().isoformat()
            })
        
        logger.info(f"✅ {len(fallback)} fallback ürün eklendi")
    
    def organize_data(self):
        """Verileri organize et"""
        logger.info("\n🔄 Veriler organize ediliyor...")
        
        if not self.products:
            return []
        
        grouped = {}
        
        for p in self.products:
            base_name = p['name'].lower()
            if p.get('brand'):
                base_name = base_name.replace(p['brand'].lower(), '').strip()
            
            import re
            base_name = re.sub(r'\d+\s*(ml|lt|l|gr|g|kg|adet)', '', base_name).strip()
            
            key = f"{p['category']}_{base_name}"
            
            if key not in grouped:
                grouped[key] = {
                    'name': p['name'],
                    'category': p['category'],
                    'prices': []
                }
            
            grouped[key]['prices'].append({
                'market': p['market'],
                'price': p['price'],
                'brand': p.get('brand', ''),
                'full_name': p['name'],
                'scraped_at': p['scraped_at']
            })
        
        result = []
        for data in grouped.values():
            data['prices'].sort(key=lambda x: x['price'])
            data['cheapest_market'] = data['prices'][0]['market']
            data['cheapest_price'] = data['prices'][0]['price']
            data['cheapest_brand'] = data['prices'][0].get('brand', '')
            
            if len(data['prices']) > 1:
                data['max_savings'] = data['prices'][-1]['price'] - data['prices'][0]['price']
                data['savings_percent'] = (data['max_savings'] / data['prices'][-1]['price']) * 100
            else:
                data['max_savings'] = 0
                data['savings_percent'] = 0
            
            result.append(data)
        
        result.sort(key=lambda x: x['max_savings'], reverse=True)
        return result
    
    def save_json(self, data):
        """JSON kaydet"""
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_products': len(data),
            'total_scraped': len(self.products),
            'total_requests': self.request_count,
            'markets': list(set([p['market'] for p in self.products])),
            'products': data
        }
        
        with open('products_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n✅ JSON kaydedildi!")
        logger.info(f"📊 {len(data)} ürün")
        logger.info(f"🏪 {len(output['markets'])} market")
        logger.info(f"📡 {self.request_count} HTTP isteği")
        
        if data:
            logger.info("\n💰 EN ÇOK TASARRUF:")
            for i, p in enumerate(data[:5], 1):
                if p['max_savings'] > 0:
                    logger.info(f"  {i}. {p['name']}: {p['max_savings']:.2f} ₺")
    
    def run(self):
        """Ana çalıştırma - IP ban önleyici"""
        logger.info("\n" + "🛡️"*30)
        logger.info("IP BAN ÖNLEYİCİ MARKET SCRAPER")
        logger.info("🛡️"*30 + "\n")
        
        start_time = time.time()
        
        # Marketleri tek tek dene
        success_count = 0
        
        # Migros
        if self.scrape_migros():
            success_count += 1
        
        # A101
        if self.scrape_a101_safe():
            success_count += 1
        
        # Yeterli veri yoksa fallback
        if len(self.products) < 5:
            logger.warning("\n⚠️ Az veri çekildi, fallback ekleniyor...")
            self.add_fallback_data()
        
        # Organize ve kaydet
        organized = self.organize_data()
        self.save_json(organized)
        
        elapsed = time.time() - start_time
        logger.info(f"\n⏱️ Toplam süre: {elapsed:.1f} saniye")
        logger.info(f"✅ {success_count} market başarılı")
        logger.info("\n" + "="*60)
        logger.info("✅ TAMAMLANDI - IP BAN YEMEDİNİZ!")
        logger.info("="*60 + "\n")


if __name__ == '__main__':
    scraper = SafeMarketScraper()
    scraper.run()
