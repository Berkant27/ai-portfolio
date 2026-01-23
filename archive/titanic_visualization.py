"""
Titanic Veri Seti Görselleştirme Script'i
Pandas ve Matplotlib kullanarak Titanic veri setini görselleştirir
Python 3.13 uyumlu
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def titanic_gorselleştirme():
    """
    Titanic veri setini okur ve çeşitli grafikler oluşturur.
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
        print("Titanic Veri Seti Görselleştirme")
        print("=" * 60)
        print(f"\nDosya okunuyor: {dosya_yolu.name}")
        
        # Veriyi oku
        df = pd.read_csv(dosya_yolu)
        print(f"✓ Veri başarıyla yüklendi! ({len(df)} satır)")
        
        # Sütun adlarını standartlaştır (büyük/küçük harf duyarsız)
        sutun_esleme = {}
        for sutun in df.columns:
            sutun_lower = sutun.lower()
            if sutun_lower in ['age', 'yaş']:
                sutun_esleme[sutun] = 'Age'
            elif sutun_lower in ['sex', 'cinsiyet', 'gender']:
                sutun_esleme[sutun] = 'Sex'
            elif sutun_lower in ['survived', 'hayatta_kaldi']:
                sutun_esleme[sutun] = 'Survived'
            elif sutun_lower in ['pclass', 'class', 'sınıf']:
                sutun_esleme[sutun] = 'Pclass'
        
        # Sütun adlarını yeniden adlandır
        df = df.rename(columns=sutun_esleme)
        
        # Gerekli sütunları kontrol et
        gerekli_sutunlar = ['Age', 'Sex', 'Survived', 'Pclass']
        eksik_sutunlar = [s for s in gerekli_sutunlar if s not in df.columns]
        
        if eksik_sutunlar:
            print(f"\nUYARI: Gerekli sütunlar bulunamadı: {eksik_sutunlar}")
            print(f"Mevcut sütunlar: {', '.join(df.columns.tolist())}")
            return None
        
        # Cinsiyete göre hayatta kalma oranlarını hesapla (konsol çıktısı için)
        cinsiyet_survived = df.groupby('Sex')['Survived'].agg(['sum', 'count'])
        cinsiyet_survived['oran'] = (cinsiyet_survived['sum'] / cinsiyet_survived['count']) * 100
        
        # Kadın ve erkek hayatta kalma oranlarını al
        kadin_oran = cinsiyet_survived.loc['female', 'oran'] if 'female' in cinsiyet_survived.index else 0
        erkek_oran = cinsiyet_survived.loc['male', 'oran'] if 'male' in cinsiyet_survived.index else 0
        
        # Eğer cinsiyet değerleri farklıysa (örn: 'Kadın', 'Erkek'), alternatif kontrol
        if kadin_oran == 0 and erkek_oran == 0:
            # Cinsiyet değerlerini kontrol et
            unique_sex = df['Sex'].unique()
            for sex_val in unique_sex:
                sex_lower = str(sex_val).lower()
                if 'f' in sex_lower or 'k' in sex_lower or 'w' in sex_lower:
                    kadin_oran = (df[df['Sex'] == sex_val]['Survived'].sum() / 
                                 len(df[df['Sex'] == sex_val])) * 100
                elif 'm' in sex_lower or 'e' in sex_lower:
                    erkek_oran = (df[df['Sex'] == sex_val]['Survived'].sum() / 
                                 len(df[df['Sex'] == sex_val])) * 100
        
        print(f"\nİçgörü: Kadın hayatta kalma oranı %{kadin_oran:.1f}, erkek %{erkek_oran:.1f}")
        
        # Grafik stilini ayarla
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 2x2 subplot oluştur
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Titanic Veri Seti Analizi - Görselleştirmeler', 
                     fontsize=16, fontweight='bold', y=0.995)
        
        # 1. Yaş dağılımı histogramı
        ax1 = axes[0, 0]
        # Eksik yaş değerlerini kaldır
        yas_verisi = df['Age'].dropna()
        ax1.hist(yas_verisi, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Yaş Dağılımı', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Yaş', fontsize=10)
        ax1.set_ylabel('Frekans', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # 2. Cinsiyete göre hayatta kalma oranları bar plot
        ax2 = axes[0, 1]
        # Cinsiyet ve hayatta kalma durumuna göre grupla
        cinsiyet_survived_df = df.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)
        cinsiyet_survived_df.plot(kind='bar', ax=ax2, color=['#ff6b6b', '#51cf66'], 
                                  edgecolor='black', alpha=0.8)
        ax2.set_title('Cinsiyete Göre Hayatta Kalma Oranları', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Cinsiyet', fontsize=10)
        ax2.set_ylabel('Kişi Sayısı', fontsize=10)
        ax2.legend(['Hayatta Kalmadı', 'Hayatta Kaldı'], loc='upper right')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Sınıf (Pclass) ve hayatta kalma ilişkisi countplot
        ax3 = axes[1, 0]
        # Seaborn countplot kullan
        sns.countplot(data=df, x='Pclass', hue='Survived', ax=ax3, 
                     palette=['#ff6b6b', '#51cf66'], edgecolor='black')
        ax3.set_title('Sınıf ve Hayatta Kalma İlişkisi', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Sınıf (Pclass)', fontsize=10)
        ax3.set_ylabel('Kişi Sayısı', fontsize=10)
        ax3.legend(['Hayatta Kalmadı', 'Hayatta Kaldı'], loc='upper right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Yaş ve hayatta kalma ilişkisi (violin plot veya box plot)
        ax4 = axes[1, 1]
        # Hayatta kalan ve kalmayanlar için yaş dağılımı
        hayatta_kalan = df[df['Survived'] == 1]['Age'].dropna()
        hayatta_kalmayan = df[df['Survived'] == 0]['Age'].dropna()
        
        ax4.hist([hayatta_kalmayan, hayatta_kalan], bins=20, alpha=0.7, 
                color=['#ff6b6b', '#51cf66'], label=['Hayatta Kalmadı', 'Hayatta Kaldı'],
                edgecolor='black')
        ax4.set_title('Yaş ve Hayatta Kalma İlişkisi', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Yaş', fontsize=10)
        ax4.set_ylabel('Frekans', fontsize=10)
        ax4.legend(loc='upper right')
        ax4.grid(True, alpha=0.3)
        
        # Grafikleri düzenle
        plt.tight_layout()
        
        # Grafikleri kaydet
        cikti_dosyasi = script_dizini / "titanic_plots.png"
        plt.savefig(cikti_dosyasi, dpi=300, bbox_inches='tight')
        print(f"\n✓ Grafikler kaydedildi: {cikti_dosyasi}")
        
        # Grafikleri göster (isteğe bağlı - yorum satırına alınabilir)
        # plt.show()
        
        print("\n" + "=" * 60)
        print("Görselleştirme Tamamlandı!")
        print("=" * 60)
        
        return df
        
    except FileNotFoundError as e:
        print(f"\nHATA: Dosya bulunamadı: {e}")
        print("Lütfen titanic.csv veya Titanic-Dataset.csv dosyasının")
        print("script ile aynı klasörde olduğundan emin olun.")
        return None
        
    except ImportError as e:
        print(f"\nHATA: Gerekli kütüphane yüklü değil: {e}")
        print("Lütfen şu komutu çalıştırın: pip install pandas matplotlib seaborn")
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
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Script çalıştırıldığında görselleştirmeyi başlat
    titanic_gorselleştirme()
