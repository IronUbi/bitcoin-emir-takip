# bitcoin-emir-takip
# Bitcoin Futures Emir Takip Sistemi

Bu GitHub repository'si, çeşitli kripto para borsalarından Bitcoin futures emir defteri verilerini (alış ve satış emirleri) otomatik olarak çekmek ve kaydetmek için GitHub Actions kullanır.

## Desteklenen Borsalar

- Binance
- Bybit
- Coinbase
- OKX
- Bitget
- MEXC
- Gate.io
- KuCoin

## Çalışma Şekli

1. GitHub Actions, ayarlanan zamanlamaya göre (saatlik) kodu otomatik olarak çalıştırır
2. Script, belirtilen borsalardan Bitcoin futures emir defterlerini çeker
3. Veriler JSON formatında `data` klasörüne kaydedilir
4. Değişiklikler otomatik olarak repository'ye commit edilir

## Dosya Yapısı

- `main.py`: Emir defterlerini çeken ana Python scripti
- `requirements.txt`: Gerekli Python kütüphanelerinin listesi
- `.github/workflows/emir-takip.yml`: GitHub Actions iş akışı tanımı

## Kurulum Adımları

1. Bu repository'yi kendi hesabınıza fork edin:
   - Sağ üst köşedeki "Fork" düğmesine tıklayın
   - Fork işlemi tamamlandığında, kendi GitHub hesabınızda bir kopyasına sahip olacaksınız

2. GitHub Actions'ı Etkinleştirin:
   - Repository'nizde "Actions" sekmesine tıklayın
   - "I understand my workflows, go ahead and enable them" düğmesine tıklayın

3. (Opsiyonel) API Anahtarları Ekleyin:
   - Repository'nizde "Settings" > "Secrets and variables" > "Actions" yolunu izleyin
   - "New repository secret" düğmesine tıklayın
   - API anahtarlarınızı ekleyin (örneğin BINANCE_API_KEY, BINANCE_SECRET_KEY)
   - `.github/workflows/emir-takip.yml` dosyasında ilgili satırların yorumunu kaldırın

4. İlk Çalıştırmayı Manuel Tetikleyin:
   - "Actions" sekmesine gidin
   - "Bitcoin Emir Takip" iş akışını seçin
   - "Run workflow" düğmesine tıklayın

## Zamanlama Ayarları

Varsayılan olarak, script her saat başı çalışır. Zamanlamayı değiştirmek için:

1. `.github/workflows/emir-takip.yml` dosyasını düzenleyin
2. `cron: '0 */1 * * *'` ifadesini değiştirin
   - Örneğin, her 6 saatte bir çalıştırmak için: `cron: '0 */6 * * *'`
   - Her gün saat 12:00'de çalıştırmak için: `cron: '0 12 * * *'`

GitHub Actions cron sözdizimi hakkında daha fazla bilgi için [bu sayfayı](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) ziyaret edin.

## Verilere Erişim

Script çalıştıktan sonra:

1. Veriler `data` klasöründe saklanır
2. Her güne ait veriler `emir_defteri_YYYY-MM-DD.json` formatlı dosyalarda bulunur
3. Repository'nizdeki bu dosyaları görüntüleyebilir veya indirebilirsiniz

## Uyarılar

- GitHub Actions her ay belirli bir süre çalışma süresi sunar, ancak bu genellikle bu tür işler için fazlasıyla yeterlidir
- GitHub'da çok büyük dosyalar (>100MB) saklayamazsınız, ancak JSON verileri genellikle bu limiti aşmaz
- Çok sık çalıştırma GitHub'un kısıtlamalarına takılabilir, bu yüzden mantıklı bir zamanlama seçin
