import os
import json
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime

# Kazıma yapılacak borsaların listesi
BORSALAR = ['binance', 'bybit', 'coinbase', 'okx', 'bitget', 'mexc', 'gateio', 'kucoin']

# Ücretsiz proxy listesi - bu listeyi sık sık güncellemeniz gerekebilir
# https://free-proxy-list.net/, https://geonode.com/free-proxy-list gibi kaynaklardan alabilirsiniz
FREE_PROXIES = [
    "103.152.112.162:80",
    "45.8.105.255:80",
    "92.118.232.74:80",
    "74.205.128.200:80",
    "198.199.86.11:3128",
    "178.128.156.227:3128",
    # Daha fazla güncel proxy ekleyin
    "51.159.115.233:3128",
    "95.56.254.139:3128",
    "3.95.126.111:80",
    "165.227.81.97:9995"
]

# Rastgele proxy seç
def rastgele_proxy():
    return random.choice(FREE_PROXIES) if FREE_PROXIES else None

# Rastgele User-Agent oluşturma fonksiyonu
def rastgele_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
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

# Proxy ile HTTP isteği yap
def proxy_request(url, headers=None, method='get', proxy=None, timeout=15):
    """Proxy kullanarak HTTP isteği yap, başarısızsa normal istek dene"""
    
    if not headers:
        headers = standart_headers()
    
    # İlk olarak proxy ile dene
    if proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            else:
                response = requests.post(url, headers=headers, proxies=proxies, timeout=timeout)
            
            # İstek başarılıysa, cevabı döndür
            if response.status_code == 200:
                return response
        except Exception as e:
            print(f"Proxy ile istek başarısız ({proxy}): {str(e)}")
    
    # Proxy başarısız olursa veya proxy yoksa, normal istek yap
    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, timeout=timeout)
        else:
            response = requests.post(url, headers=headers, timeout=timeout)
        
        return response
    except Exception as e:
        print(f"Normal istek de başarısız: {str(e)}")
        return None

# Alternatif Binance API URL'leri
def binance_emir_defteri_kazima():
    print("Binance verilerini kazıma...")
    try:
        # Alternatif Binance API URL'leri
        urls = [
            "https://fapi.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10",
            "https://api.binance.us/api/v3/depth?symbol=BTCUSDT&limit=10",
            "https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10"
        ]
        
        for url in urls:
            proxy = rastgele_proxy()
            response = proxy_request(url, headers=json_headers(), proxy=proxy)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Emir defteri verilerini al
                    bids = [[float(price), float(amount)] for price, amount in data.get('bids', [])[:10]]
                    asks = [[float(price), float(amount)] for price, amount in data.get('asks', [])[:10]]
                    
                    if bids and asks:
                        # Sonuçları döndür
                        return {
                            'borsa': 'binance',
                            'sembol': 'BTCUSDT',
                            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'alis_emirleri': bids,
                            'satis_emirleri': asks
                        }
                except Exception as e:
                    print(f"Binance API yanıtı ayrıştırılamadı: {str(e)}")
                    continue
        
        # Alternatif olarak: HTML sayfayı kazıma
        print("Binance API istekleri başarısız, HTML sayfayı deneniyor...")
        
        html_url = "https://www.binance.com/en/futures/BTCUSDT"
        html_response = proxy_request(html_url, headers=standart_headers(), proxy=rastgele_proxy())
        
        if html_response and html_response.status_code == 200:
            # HTML içeriği analiz et...
            # Not: Binance sayfasının yapısı değişebilir, kazıma başarısız olabilir
            print("HTML sayfası başarıyla alındı, ama içeriği analiz etmek için özel kod gerekli.")
            
            # HTML içeriğini debug için kaydet
            with open('binance_debug.html', 'w', encoding='utf-8') as f:
                f.write(html_response.text)
            
            print("HTML içeriği 'binance_debug.html' dosyasına kaydedildi, manuel inceleme yapabilirsiniz.")
        
        print("Tüm Binance istekleri başarısız oldu.")
        return None
    
    except Exception as e:
        print(f"Binance kazıma sırasında hata: {str(e)}")
        return None
        
# API anahtarı gerektirmeyen Bybit alternatif yöntemi
def bybit_emir_defteri_kazima():
    print("Bybit verilerini kazıma...")
    try:
        # Bybit API endpoint - birkaç alternatif deneyelim
        urls = [
            "https://api.bybit.com/v5/market/orderbook?category=linear&symbol=BTCUSDT&limit=10",
            "https://api-testnet.bybit.com/v5/market/orderbook?category=linear&symbol=BTCUSDT&limit=10"
        ]
        
        for url in urls:
            proxy = rastgele_proxy()
            response = proxy_request(url, headers=json_headers(), proxy=proxy)
            
            if response and response.status_code == 200:
                try:
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
                except Exception as e:
                    print(f"Bybit API yanıtı ayrıştırılamadı: {str(e)}")
                    continue
        
        # Bybit alternatif endpoint deneyelim
        try:
            alt_url = "https://api.bybit.com/derivatives/v3/public/order-book/L2?category=linear&symbol=BTCUSDT"
            proxy = rastgele_proxy()
            response = proxy_request(alt_url, headers=json_headers(), proxy=proxy)
            
            if response and response.status_code == 200:
                data = response.json()
                
                if 'result' in data and 'b' in data['result'] and 'a' in data['result']:
                    result = data['result']
                    bids = [[float(item[0]), float(item[1])] for item in result.get('b', [])[:10]]
                    asks = [[float(item[0]), float(item[1])] for item in result.get('a', [])[:10]]
                    
                    return {
                        'borsa': 'bybit',
                        'sembol': 'BTCUSDT',
                        'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'alis_emirleri': bids,
                        'satis_emirleri': asks
                    }
        except Exception as e:
            print(f"Bybit alternatif API de başarısız: {str(e)}")
        
        print("Tüm Bybit istekleri başarısız oldu.")
        return None
    
    except Exception as e:
        print(f"Bybit kazıma sırasında hata: {str(e)}")
        return None

# Coinbase için alternatif yaklaşım
def coinbase_emir_defteri_kazima():
    print("Coinbase verilerini kazıma...")
    try:
        # Coinbase Public API - API anahtarı gerektirmez
        url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
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
        else:
            print(f"Coinbase API yanıtı başarısız: {response.status_code if response else 'Yanıt yok'}")
            
            # Alternatif endpoint deneyelim
            alt_url = "https://api.pro.coinbase.com/products/BTC-USD/book?level=2"
            proxy = rastgele_proxy()
            alt_response = proxy_request(alt_url, headers=json_headers(), proxy=proxy)
            
            if alt_response and alt_response.status_code == 200:
                data = alt_response.json()
                
                bids = [[float(item[0]), float(item[1])] for item in data.get('bids', [])[:10]]
                asks = [[float(item[0]), float(item[1])] for item in data.get('asks', [])[:10]]
                
                return {
                    'borsa': 'coinbase',
                    'sembol': 'BTC-USD',
                    'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'alis_emirleri': bids,
                    'satis_emirleri': asks
                }
            
            return None
    
    except Exception as e:
        print(f"Coinbase kazıma sırasında hata: {str(e)}")
        return None

# OKX emir defteri kazıma
def okx_emir_defteri_kazima():
    print("OKX verilerini kazıma...")
    try:
        # OKX API endpoint
        url = "https://www.okx.com/api/v5/market/books?instId=BTC-USDT-SWAP&sz=10"
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
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
                
            # Alternatif endpoint deneyelim
            alt_url = "https://www.okx.com/api/v5/market/books?instId=BTC-USDT&sz=10" 
            proxy = rastgele_proxy()
            alt_response = proxy_request(alt_url, headers=json_headers(), proxy=proxy)
            
            if alt_response and alt_response.status_code == 200:
                data = alt_response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    orderbook = data['data'][0]
                    
                    bids = [[float(item[0]), float(item[1])] for item in orderbook.get('bids', [])[:10]]
                    asks = [[float(item[0]), float(item[1])] for item in orderbook.get('asks', [])[:10]]
                    
                    return {
                        'borsa': 'okx',
                        'sembol': 'BTC-USDT',
                        'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'alis_emirleri': bids,
                        'satis_emirleri': asks
                    }
        else:
            print(f"OKX API yanıtı başarısız: {response.status_code if response else 'Yanıt yok'}")
        
        return None
    
    except Exception as e:
        print(f"OKX kazıma sırasında hata: {str(e)}")
        return None

# Bitget emir defteri kazıma
def bitget_emir_defteri_kazima():
    print("Bitget verilerini kazıma...")
    try:
        # Bitget API endpoint
        url = "https://api.bitget.com/api/mix/v1/market/depth?symbol=BTCUSDT&limit=10"
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
            data = response.json()
            
            # Emir defteri verilerini al
            if 'data' in data and 'asks' in data['data'] and 'bids' in data['data']:
                orderbook = data['data']
                
                bids = [[float(item[0]), float(item[1])] for item in orderbook.get('bids', [])[:10]]
                asks = [[float(item[0]), float(item[1])] for item in orderbook.get('asks', [])[:10]]
                
                # Sonuçları döndür
                return {
                    'borsa': 'bitget',
                    'sembol': 'BTCUSDT',
                    'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'alis_emirleri': bids,
                    'satis_emirleri': asks
                }
            else:
                print("Bitget API yanıtı beklenen formatta değil")
                
        # Alternatif endpoint deneyelim
        alt_url = "https://api.bitget.com/api/spot/v1/market/depth?symbol=BTCUSDT_SPBL&type=step0"
        proxy = rastgele_proxy()
        alt_response = proxy_request(alt_url, headers=json_headers(), proxy=proxy)
        
        if alt_response and alt_response.status_code == 200:
            data = alt_response.json()
            
            if 'data' in data and 'asks' in data['data'] and 'bids' in data['data']:
                orderbook = data['data']
                
                bids = [[float(item[0]), float(item[1])] for item in orderbook.get('bids', [])[:10]]
                asks = [[float(item[0]), float(item[1])] for item in orderbook.get('asks', [])[:10]]
                
                return {
                    'borsa': 'bitget',
                    'sembol': 'BTCUSDT_SPBL',
                    'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'alis_emirleri': bids,
                    'satis_emirleri': asks
                }
                
        print("Tüm Bitget istekleri başarısız oldu.")
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
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
            data = response.json()
            
            # Emir defteri verilerini al
            bids = [[float(item[0]), float(item[1])] for item in data.get('bids', [])[:10]]
            asks = [[float(item[0]), float(item[1])] for item in data.get('asks', [])[:10]]
            
            # Sonuçları döndür
            return {
                'borsa': 'mexc',
                'sembol': 'BTCUSDT',
                'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'alis_emirleri': bids,
                'satis_emirleri': asks
            }
                
        print("MEXC istekleri başarısız oldu.")
        return None
    
    except Exception as e:
        print(f"MEXC kazıma sırasında hata: {str(e)}")
        return None

# Gate.io emir defteri kazıma
def gateio_emir_defteri_kazima():
    print("Gate.io verilerini kazıma...")
    try:
        # Gate.io API endpoint
        url = "https://api.gateio.ws/api/v4/spot/order_book?currency_pair=BTC_USDT&limit=10"
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
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
                
        print("Gate.io istekleri başarısız oldu.")
        return None
    
    except Exception as e:
        print(f"Gate.io kazıma sırasında hata: {str(e)}")
        return None

# KuCoin emir defteri kazıma
def kucoin_emir_defteri_kazima():
    print("KuCoin verilerini kazıma...")
    try:
        # KuCoin API endpoint
        url = "https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol=BTC-USDT"
        
        proxy = rastgele_proxy()
        response = proxy_request(url, headers=json_headers(), proxy=proxy)
        
        if response and response.status_code == 200:
            data = response.json()
            
            # Emir defteri verilerini al
            if 'data' in data:
                orderbook = data['data']
                
                bids = [[float(item[0]), float(item[1])] for item in orderbook.get('bids', [])[:10]]
                asks = [[float(item[0]), float(item[1])] for item in orderbook.get('asks', [])[:10]]
                
                # Sonuçları döndür
                return {
                    'borsa': 'kucoin',
                    'sembol': 'BTC-USDT',
                    'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'alis_emirleri': bids,
                    'satis_emirleri': asks
                }
            else:
                print("KuCoin API yanıtı beklenen formatta değil")
                
        print("KuCoin istekleri başarısız oldu.")
        return None
    
    except Exception as e:
        print(f"KuCoin kazıma sırasında hata: {str(e)}")
        return None

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
    saat_str = datetime.now().strftime('%H-%M-%S')
    dosya_adi = f"data/emir_defteri_{tarih_str}_{saat_str}.json"
    
    # Tüm verileri topla
    tum_veriler = []
    basarili_istek_sayisi = 0
    
    # Tüm borsalar için kazıma fonksiyonları
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
    
    # Her borsayı dene
    for borsa_id, kazima_fonksiyonu in kazima_fonksiyonlari.items():
        try:
            # Kısa bekleme ile rate limit aşımını önle
            time.sleep(random.uniform(2, 5))
            
            print(f"{borsa_id} verilerini almaya çalışılıyor...")
            borsa_veri = kazima_fonksiyonu()
            
            if borsa_veri:
                tum_veriler.append(borsa_veri)
                basarili_istek_sayisi += 1
                print(f"{borsa_id} için veriler başarıyla alındı")
            else:
                print(f"{borsa_id} için veri alınamadı")
        
        except Exception as e:
            print(f"{borsa_id} işlemi sırasında beklenmeyen hata: {str(e)}")
    
    # En az bir başarılı istek varsa verileri kaydet
    if basarili_istek_sayisi > 0:
        with open(dosya_adi, 'w') as f:
            json.dump(tum_veriler, f, indent=2)
        print(f"Tüm veriler {dosya_adi} dosyasına kaydedildi")
        print(f"Başarıyla veri alınan borsa sayısı: {basarili_istek_sayisi}/{len(kazima_fonksiyonlari)}")
    else:
        print("Hiçbir borsadan veri alınamadı, dosya kaydedilmedi")
    
    return basarili_istek_sayisi

if __name__ == "__main__":
    sayi = veri_kaydet()
    print(f"Toplam {sayi} adet veri kaynağından veri kaydedildi.")
