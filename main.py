import os
import json
import ccxt
from datetime import datetime

# İşlem yapılacak borsaların listesi
BORSALAR = ['binance', 'bybit', 'coinbase', 'okx', 'bitget', 'mexc', 'gateio', 'kucoin']

# Farklı borsalar için Bitcoin futures sembol eşleştirmeleri
SEMBOL_ESLESME = {
    'binance': 'BTC/USDT:USDT',
    'bybit': 'BTCUSDT',
    'coinbase': 'BTC-USD',
    'okx': 'BTC-USDT-SWAP',
    'bitget': 'BTCUSDT_UMCBL',
    'mexc': 'BTC_USDT',
    'gateio': 'BTC_USDT',
    'kucoin': 'XBTUSDTM'
}

def borsa_baglantisi(borsa_id):
    """Borsa bağlantısını başlat"""
    exchange_class = getattr(ccxt, borsa_id)
    
    # Gate.io için özel durum
    if borsa_id == 'gateio':
        borsa_id = 'gate'
        
    # API anahtarları varsa çevre değişkenlerinden al
    api_key = os.environ.get(f'{borsa_id.upper()}_API_KEY')
    secret_key = os.environ.get(f'{borsa_id.upper()}_SECRET_KEY')
    
    if api_key and secret_key:
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True
        })
    else:
        exchange = exchange_class({
            'enableRateLimit': True
        })
    
    return exchange

def emir_defteri_cek(borsa_id, sembol):
    """Belirtilen borsa ve sembol için emir defterini çek"""
    try:
        exchange = borsa_baglantisi(borsa_id)
        
        # Bazı borsalar futures için özel parametreler gerektirir
        if borsa_id == 'binance':
            exchange.options['defaultType'] = 'future'
        elif borsa_id == 'bybit':
            exchange.options['defaultType'] = 'swap'
        
        # Emir defterini çek
        emir_defteri = exchange.fetch_order_book(sembol)
        
        # Alış (bids) ve satış (asks) emirlerini ayır
        alislar = emir_defteri['bids']
        satislar = emir_defteri['asks']
        
        return {
            'borsa': borsa_id,
            'sembol': sembol,
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': alislar[:10],  # İlk 10 alış emri
            'satis_emirleri': satislar[:10]   # İlk 10 satış emri
        }
    except Exception as e:
        print(f"{borsa_id} borsasından veri çekerken hata: {str(e)}")
        return {
            'borsa': borsa_id,
            'sembol': sembol,
            'zaman': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'alis_emirleri': [],
            'satis_emirleri': [],
            'hata': str(e)
        }

def veri_kaydet():
    """Tüm borsalardan veri çek ve kaydet"""
    print("Bitcoin futures emir defteri toplama başlatılıyor...")
    
    # Veri dizini yoksa oluştur
    os.makedirs('data', exist_ok=True)
    
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
    
    # Tüm borsalardan veri çek
    for borsa_id in BORSALAR:
        sembol = SEMBOL_ESLESME.get(borsa_id)
        if sembol:
            try:
                data = emir_defteri_cek(borsa_id, sembol)
                tum_veriler.append(data)
                print(f"{borsa_id} için veriler alındı")
            except Exception as e:
                print(f"{borsa_id} için veri alınırken hata: {str(e)}")
        else:
            print(f"{borsa_id} için sembol tanımlanmamış")
    
    # Güncel verileri kaydet
    with open(dosya_adi, 'w') as f:
        json.dump(tum_veriler, f, indent=2)
        
    print(f"Tüm veriler {dosya_adi} dosyasına kaydedildi")
    
    return len(tum_veriler)

if __name__ == "__main__":
    sayi = veri_kaydet()
    print(f"Toplam {sayi} adet veri kaydedildi.")
