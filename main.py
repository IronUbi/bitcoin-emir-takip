import os
import json
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime

# Kazıma yapılacak borsaların listesi
BORSALAR = ['binance', 'bybit', 'coinbase', 'okx', 'bitget', 'mexc', 'gateio', 'kucoin']

# Rastgele User-Agent oluşturma fonksiyonu
def rastgele_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    ]
    return random.choice(user_agents)

# Standart HTTP headers
def standart_headers():
    return {
        'User-Agent': rastgele_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

# JSON isteği için headers
def json_headers():
    return {
        'User-Agent': rastgele_user_agent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

# Binance emir defteri kazıma
def binance_emir_defteri_kazima():
    print("Binance verilerini kazıma...")
    try:
        # Binance Futures API endpoint
        url = "https://fapi.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"Binance API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        bids = [[float(price), float(amount)] for price, amount in data.get('bids', [])[:10]]
        asks = [[float(price), float(amount)] for price, amount in data.get('asks', [])[:10]]
        
        # Sonuçları döndür
        return {
            'borsa': 'binance',
            'sembol': 'BTCUSDT',
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': bids,
            'satis_emirleri': asks
        }
    
    except Exception as e:
        print(f"Binance kazıma sırasında hata: {str(e)}")
        return None

# Bybit emir defteri kazıma
def bybit_emir_defteri_kazima():
    print("Bybit verilerini kazıma...")
    try:
        # Bybit API endpoint
        url = "https://api.bybit.com/v5/market/orderbook?category=linear&symbol=BTCUSDT&limit=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"Bybit API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        result = data.get('result', {})
        
        if 'b' in result and 'a' in result:
            bids = [[float(item[0]), float(item[1])] for item in result.get('b', [])[:10]]
            asks = [[float(item[0]), float(item[1])] for item in result.get('a', [])[:10]]
            
            # Sonuçları döndür
            return {
                'borsa': 'bybit',
                'sembol': 'BTCUSDT',
                'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'alis_emirleri': bids,
                'satis_emirleri': asks
            }
        else:
            print("Bybit API yanıtı beklenen formatta değil")
            return None
    
    except Exception as e:
        print(f"Bybit kazıma sırasında hata: {str(e)}")
        return None

# Coinbase emir defteri kazıma
def coinbase_emir_defteri_kazima():
    print("Coinbase verilerini kazıma...")
    try:
        # Coinbase API endpoint - BTC-USD
        url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"Coinbase API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        bids = [[float(item[0]), float(item[1])] for item in data.get('bids', [])[:10]]
        asks = [[float(item[0]), float(item[1])] for item in data.get('asks', [])[:10]]
        
        # Sonuçları döndür
        return {
            'borsa': 'coinbase',
            'sembol': 'BTC-USD',
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': bids,
            'satis_emirleri': asks
        }
    
    except Exception as e:
        print(f"Coinbase kazıma sırasında hata: {str(e)}")
        return None

# OKX emir defteri kazıma
def okx_emir_defteri_kazima():
    print("OKX verilerini kazıma...")
    try:
        # OKX API endpoint
        url = "https://www.okx.com/api/v5/market/books?instId=BTC-USDT-SWAP&sz=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"OKX API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        if 'data' in data and len(data['data']) > 0:
            orderbook = data['data'][0]
            
            bids = [[float(item[0]), float(item[1])] for item in orderbook.get('bids', [])[:10]]
            asks = [[float(item[0]), float(item[1])] for item in orderbook.get('asks', [])[:10]]
            
            # Sonuçları döndür
            return {
                'borsa': 'okx',
                'sembol': 'BTC-USDT-SWAP',
                'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'alis_emirleri': bids,
                'satis_emirleri': asks
            }
        else:
            print("OKX API yanıtı beklenen formatta değil")
            return None
    
    except Exception as e:
        print(f"OKX kazıma sırasında hata: {str(e)}")
        return None

# Bitget emir defteri kazıma
def bitget_emir_defteri_kazima():
    print("Bitget verilerini kazıma...")
    try:
        # Bitget API endpoint
        url = "https://api.bitget.com/api/mix/v1/market/depth?symbol=BTCUSDT_UMCBL&limit=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"Bitget API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        if 'data' in data and 'asks' in data['data'] and 'bids' in data['data']:
            bids_data = data['data']['bids']
            asks_data = data['data']['asks']
            
            bids = [[float(item[0]), float(item[1])] for item in bids_data[:10]]
            asks = [[float(item[0]), float(item[1])] for item in asks_data[:10]]
            
            # Sonuçları döndür
            return {
                'borsa': 'bitget',
                'sembol': 'BTCUSDT_UMCBL',
                'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'alis_emirleri': bids,
                'satis_emirleri': asks
            }
        else:
            print("Bitget API yanıtı beklenen formatta değil")
            return None
    
    except Exception as e:
        print(f"Bitget kazıma sırasında hata: {str(e)}")
        return None

# MEXC emir defteri kazıma
def mexc_emir_defteri_kazima():
    print("MEXC verilerini kazıma...")
    try:
        # MEXC API endpoint
        url = "https://api.mexc.com/api/v3/depth?symbol=BTCUSDT&limit=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"MEXC API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        bids = [[float(price), float(amount)] for price, amount in data.get('bids', [])[:10]]
        asks = [[float(price), float(amount)] for price, amount in data.get('asks', [])[:10]]
        
        # Sonuçları döndür
        return {
            'borsa': 'mexc',
            'sembol': 'BTCUSDT',
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': bids,
            'satis_emirleri': asks
        }
    
    except Exception as e:
        print(f"MEXC kazıma sırasında hata: {str(e)}")
        return None

# Gate.io emir defteri kazıma
def gateio_emir_defteri_kazima():
    print("Gate.io verilerini kazıma...")
    try:
        # Gate.io API endpoint
        url = "https://api.gateio.ws/api/v4/futures/usdt/order_book?contract=BTC_USDT&limit=10"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"Gate.io API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        bids = [[float(item[0]), float(item[1])] for item in data.get('bids', [])[:10]]
        asks = [[float(item[0]), float(item[1])] for item in data.get('asks', [])[:10]]
        
        # Sonuçları döndür
        return {
            'borsa': 'gateio',
            'sembol': 'BTC_USDT',
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': bids,
            'satis_emirleri': asks
        }
    
    except Exception as e:
        print(f"Gate.io kazıma sırasında hata: {str(e)}")
        return None

# KuCoin emir defteri kazıma
def kucoin_emir_defteri_kazima():
    print("KuCoin verilerini kazıma...")
    try:
        # KuCoin API endpoint - XBTUSDTM (BTC futures)
        url = "https://api-futures.kucoin.com/api/v1/level2/depth?symbol=XBTUSDTM"
        
        # İstek gönder
        response = requests.get(url, headers=json_headers(), timeout=10)
        
        # Başarı durumunu kontrol et
        if response.status_code != 200:
            print(f"KuCoin API'sine erişilemiyor. Durum kodu: {response.status_code}")
            return None
        
        # JSON yanıtı ayrıştır
        data = response.json()
        
        # Emir defteri verilerini al
        if 'data' in data and 'bids' in data['data'] and 'asks' in data['data']:
            bids_data = data['data']['bids']
            asks_data = data['data']['asks']
            
            bids = [[float(item[0]), float(item[1])] for item in bids_data[:10]]
            asks = [[float(item[0]), float(item[1])] for item in asks_data[:10]]
            
            # Sonuçları döndür
            return {
                'borsa': 'kucoin',
                'sembol': 'XBTUSDTM',
                'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'alis_emirleri': bids,
                'satis_emirleri': asks
            }
        else:
            print("KuCoin API yanıtı beklenen formatta değil")
            return None
    
    except Exception as e:
        print(f"KuCoin kazıma sırasında hata: {str(e)}")
        return None

# Belirli bir borsa için emir defteri kazıma fonksiyonunu seç
def borsa_kazima_fonksiyonu(borsa_id):
    kazima_fonksiyonlari = {
        'binance': binance_emir_defteri_kazima,
        'bybit': bybit_emir_defteri_kazima,
        'coinbase': coinbase_emir_defteri_kazima,
        'okx': okx_emir_defteri_kazima,
        'bitget': bitget_emir_defteri_kazima,
        'mexc': mexc_emir_defteri_kazima,
        'gateio': gateio_emir_defteri_kazima,
        'kucoin': kucoin_emir_defteri_kazima
    }
    
    return kazima_fonksiyonlari.get(borsa_id.lower())

# Tüm borsalardan veri kazıma ve kaydetme
def veri_kaydet():
    """Tüm borsalardan veri kazıma ve kaydetme"""
    print("Bitcoin futures emir defteri kazıma başlatılıyor...")
    
    # Veri dizini yoksa oluştur
    os.makedirs('data', exist_ok=True)
    
    # Boş gitkeep dosyası oluştur (ilk çalıştırmada faydalı)
    gitkeep_path = os.path.join('data', '.gitkeep')
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            pass
    
    # Günün tarihiyle dosya adı oluştur
    tarih_str = datetime.now().strftime('%Y-%m-%d')
    dosya_adi = f"data/emir_defteri_{tarih_str}.json"
    
    # Dosya varsa mevcut verileri yükle
    tum_veriler = []
    if os.path.exists(dosya_adi):
        try:
            with open(dosya_adi, 'r') as f:
                tum_veriler = json.load(f)
        except json.JSONDecodeError:
            # Dosya boşsa veya geçersizse yeni bir liste oluştur
            tum_veriler = []
    
    # Başarılı istek sayısını takip et
    basarili_istek_sayisi = 0
    
    # Tüm borsalardan veri çek
    for borsa_id in BORSALAR:
        try:
            # Kısa bekleme ile rate limit aşımını önle
            time.sleep(random.uniform(1, 3))
            
            # Borsa için uygun kazıma fonksiyonunu bul
            kazima_fonksiyonu = borsa_kazima_fonksiyonu(borsa_id)
            
            if kazima_fonksiyonu:
                borsa_veri = kazima_fonksiyonu()
                
                if borsa_veri:
                    tum_veriler.append(borsa_veri)
                    basarili_istek_sayisi += 1
                    print(f"{borsa_id} için veriler başarıyla kazındı")
                else:
                    print(f"{borsa_id} için veri kazıma başarısız oldu")
            else:
                print(f"{borsa_id} için kazıma fonksiyonu bulunamadı")
        
        except Exception as e:
            print(f"{borsa_id} işlemi sırasında beklenmeyen hata: {str(e)}")
    
    # En az bir başarılı istek varsa verileri kaydet
    if basarili_istek_sayisi > 0:
        with open(dosya_adi, 'w') as f:
            json.dump(tum_veriler, f, indent=2)
        print(f"Tüm veriler {dosya_adi} dosyasına kaydedildi")
    else:
        print("Hiçbir borsadan veri alınamadı, dosya kaydedilmedi")
    
    return basarili_istek_sayisi

if __name__ == "__main__":
    sayi = veri_kaydet()
    print(f"Toplam {sayi} adet borsa için veri kaydedildi.")
