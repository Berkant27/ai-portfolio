"""
Titanic Veri Seti Analiz Script'i
Pandas kullanarak Titanic veri setini analiz eder
Python 3.13 uyumlu
"""

import pandas as pd
import os
from pathlib import Path

def titanic_analizi():
    """
    Titanic veri setini okur ve temel analizler yapar.
    """
    try:
        # Dosya yolu belirleme - önce titanic.csv, yoksa Titanic-Dataset.csv dene
        script_dizini = Path(__file__).parent
        dosya_yolu = script_dizini / "titanic.csv"
        
        # Eğer titanic.csv yoksa, Titanic-Dataset.csv'yi dene
        if not dosya_yolu.exists():
            dosya_yolu = script_dizini / "Titanic-Dataset.csv"
        
        # Dosya varlığını kontrol et
        if not dosya_yolu.exists():
            print("=" * 60)
            print("HATA: Veri dosyası bulunamadı!")
            print("=" * 60)
            print(f"Aranan dosyalar:")
            print(f"  - {script_dizini / 'titanic.csv'}")
            print(f"  - {script_dizini / 'Titanic-Dataset.csv'}")
            print("\nLütfen veri dosyasının bu klasörde olduğundan emin olun.")
            return None
        
        print("=" * 60)
        print("Titanic Veri Seti Analizi")
        print("=" * 60)
        print(f"\nDosya okunuyor: {dosya_yolu.name}")
        
        # Veriyi oku
        df = pd.read_csv(dosya_yolu)
        
        print(f"✓ Veri başarıyla yüklendi!")
        print(f"  - Toplam satır sayısı: {len(df)}")
        print(f"  - Toplam sütun sayısı: {len(df.columns)}")
        print(f"  - Sütunlar: {', '.join(df.columns.tolist())}")
        
        # İlk 5 satırı göster
        print("\n" + "=" * 60)
        print("1. İlk 5 Satır (head)")
        print("=" * 60)
        print(df.head().to_string())
        
        # Yaş ortalamasını hesapla
        print("\n" + "=" * 60)
        print("2. Yaş Ortalaması")
        print("=" * 60)
        
        # Yaş sütununu kontrol et (bazı veri setlerinde 'Age', bazılarında 'age' olabilir)
        yas_sutunu = None
        for sutun in df.columns:
            if sutun.lower() in ['age', 'yaş', 'age_']:
                yas_sutunu = sutun
                break
        
        if yas_sutunu:
            yas_ortalamasi = df[yas_sutunu].mean()
            eksik_yas = df[yas_sutunu].isnull().sum()
            print(f"Yaş Ortalaması: {yas_ortalamasi:.2f} yaş")
            print(f"Eksik yaş verisi: {eksik_yas} satır")
        else:
            print("UYARI: 'Age' veya 'yaş' sütunu bulunamadı.")
            print(f"Mevcut sütunlar: {', '.join(df.columns.tolist())}")
        
        # Hayatta kalan oranını hesapla
        print("\n" + "=" * 60)
        print("3. Hayatta Kalma Oranı")
        print("=" * 60)
        
        # Survived sütununu kontrol et
        survived_sutunu = None
        for sutun in df.columns:
            if sutun.lower() in ['survived', 'hayatta_kaldi', 'survived_']:
                survived_sutunu = sutun
                break
        
        if survived_sutunu:
            toplam_yolcu = len(df)
            hayatta_kalan = df[survived_sutunu].sum()
            hayatta_kalma_orani = (hayatta_kalan / toplam_yolcu) * 100
            
            print(f"Toplam Yolcu: {toplam_yolcu}")
            print(f"Hayatta Kalan: {hayatta_kalan}")
            print(f"Hayatta Kalma Oranı: {hayatta_kalma_orani:.2f}%")
        else:
            print("UYARI: 'Survived' sütunu bulunamadı.")
            print(f"Mevcut sütunlar: {', '.join(df.columns.tolist())}")
        
        # Cinsiyete göre hayatta kalma oranları
        print("\n" + "=" * 60)
        print("4. Cinsiyete Göre Hayatta Kalma Oranları")
        print("=" * 60)
        
        # Cinsiyet sütununu kontrol et
        cinsiyet_sutunu = None
        for sutun in df.columns:
            if sutun.lower() in ['sex', 'cinsiyet', 'gender', 'sex_']:
                cinsiyet_sutunu = sutun
                break
        
        if survived_sutunu and cinsiyet_sutunu:
            cinsiyet_survived = df.groupby(cinsiyet_sutunu)[survived_sutunu].agg(['sum', 'count'])
            cinsiyet_survived['oran'] = (cinsiyet_survived['sum'] / cinsiyet_survived['count']) * 100
            cinsiyet_survived.columns = ['Hayatta_Kalan', 'Toplam', 'Oran_%']
            
            print("\nCinsiyete Göre Hayatta Kalma İstatistikleri:")
            print("-" * 60)
            print(cinsiyet_survived.to_string())
            print("-" * 60)
        else:
            print("UYARI: 'Sex' veya 'Survived' sütunu bulunamadı.")
            if not cinsiyet_sutunu:
                print(f"Cinsiyet sütunu mevcut değil. Sütunlar: {', '.join(df.columns.tolist())}")
        
        # Eksik değer sayısını göster
        print("\n" + "=" * 60)
        print("5. Eksik Değer Analizi")
        print("=" * 60)
        
        eksik_degerler = df.isnull().sum()
        eksik_degerler_yuzde = (eksik_degerler / len(df)) * 100
        
        eksik_df = pd.DataFrame({
            'Eksik_Adet': eksik_degerler,
            'Eksik_Yuzde': eksik_degerler_yuzde
        })
        
        # Sadece eksik değeri olan sütunları göster
        eksik_df = eksik_df[eksik_df['Eksik_Adet'] > 0]
        
        if len(eksik_df) > 0:
            print("\nEksik Değerler:")
            print("-" * 60)
            print(eksik_df.to_string())
            print("-" * 60)
        else:
            print("\n✓ Veri setinde eksik değer bulunmuyor!")
        
        print("\n" + "=" * 60)
        print("Analiz Tamamlandı!")
        print("=" * 60)
        
        return df
        
    except FileNotFoundError as e:
        print(f"\nHATA: Dosya bulunamadı: {e}")
        print("Lütfen titanic.csv veya Titanic-Dataset.csv dosyasının")
        print("script ile aynı klasörde olduğundan emin olun.")
        return None
        
    except pd.errors.EmptyDataError:
        print("\nHATA: Dosya boş veya geçersiz format!")
        return None
        
    except pd.errors.ParserError as e:
        print(f"\nHATA: Dosya okuma hatası: {e}")
        print("Dosya formatını kontrol edin (CSV formatında olmalı).")
        return None
        
    except Exception as e:
        print(f"\nHATA: Beklenmeyen bir hata oluştu: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    # Script çalıştırıldığında analizi başlat
    titanic_analizi()
