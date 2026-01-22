"""
Basit Veri Manipülasyonu Script'i
Pandas ve NumPy kullanarak DataFrame oluşturma ve analiz işlemleri
Python 3.13 uyumlu
"""

import pandas as pd
import numpy as np
from typing import Optional

def veri_manipulasyonu():
    """
    Rastgele veri oluşturur, analiz eder ve filtreler.
    """
    try:
        # Rastgele veri oluşturma için seed ayarla (tekrarlanabilirlik için)
        np.random.seed(42)
        
        # Rastgele isimler listesi
        isimler = ['Ali', 'Ayşe', 'Mehmet', 'Fatma', 'Mustafa', 'Zeynep', 
                   'Ahmet', 'Elif', 'Hasan', 'Selin']
        
        # Rastgele şehirler listesi
        sehirler = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 
                    'Adana', 'Gaziantep', 'Konya', 'Kayseri', 'Eskişehir']
        
        # 10 satırlık rastgele DataFrame oluştur
        print("=" * 60)
        print("1. Rastgele 10 satırlık DataFrame oluşturuluyor...")
        print("=" * 60)
        
        df = pd.DataFrame({
            'ad': np.random.choice(isimler, size=10, replace=False),
            'yaş': np.random.randint(18, 65, size=10),
            'şehir': np.random.choice(sehirler, size=10, replace=True),
            'not_ortalaması': np.random.randint(50, 100, size=10)
        })
        
        # DataFrame'i güzel formatlı göster
        print("\nOluşturulan DataFrame:")
        print(df.to_string(index=True))
        print()
        
        # Yaş ortalamasını hesapla
        print("=" * 60)
        print("2. Yaş ortalaması hesaplanıyor...")
        print("=" * 60)
        
        yas_ortalamasi = df['yaş'].mean()
        print(f"\nYaş Ortalaması: {yas_ortalamasi:.2f} yaş")
        print()
        
        # Not ortalaması >70 olanları filtrele
        print("=" * 60)
        print("3. Not ortalaması >70 olan öğrenciler filtreleniyor...")
        print("=" * 60)
        
        yuksek_notlar = df[df['not_ortalaması'] > 70]
        
        # Sonucu güzel formatlı print et
        if len(yuksek_notlar) > 0:
            print(f"\nNot ortalaması 70'ten yüksek olan {len(yuksek_notlar)} öğrenci:")
            print("-" * 60)
            print(yuksek_notlar.to_string(index=False))
            print("-" * 60)
            
            # İstatistiksel özet
            print(f"\nÖzet İstatistikler:")
            print(f"  - Toplam öğrenci sayısı: {len(df)}")
            print(f"  - Yüksek notlu öğrenci sayısı: {len(yuksek_notlar)}")
            print(f"  - Yüksek notlu öğrencilerin ortalama yaşı: {yuksek_notlar['yaş'].mean():.2f}")
            print(f"  - Yüksek notlu öğrencilerin ortalama notu: {yuksek_notlar['not_ortalaması'].mean():.2f}")
        else:
            print("\nNot ortalaması 70'ten yüksek olan öğrenci bulunamadı.")
        
        print("\n" + "=" * 60)
        print("İşlem başarıyla tamamlandı!")
        print("=" * 60)
        
        return df, yuksek_notlar
        
    except ImportError as e:
        print(f"HATA: Gerekli kütüphane yüklü değil: {e}")
        print("Lütfen şu komutu çalıştırın: pip install pandas numpy")
        return None, None
        
    except Exception as e:
        print(f"HATA: Beklenmeyen bir hata oluştu: {type(e).__name__}: {e}")
        return None, None


if __name__ == "__main__":
    # Script çalıştırıldığında fonksiyonu çağır
    veri_manipulasyonu()
