import matplotlib.pyplot as plt
import csv


def veri_yukle(dosya_adi):
    veriler = {}
    with open(dosya_adi, 'r') as f:
        okuyucu = csv.DictReader(f)
        basliklar = okuyucu.fieldnames

        for b in basliklar:
            veriler[b] = []

        for satir in okuyucu:
            for b in basliklar:
                try:
                    veriler[b].append(float(satir[b]))
                except ValueError:
                    continue
    return veriler


veri_seti = veri_yukle('diabetes.csv')

def kutu_cizimi_yap(veri_dict):
    for sutun_adi, degerler in veri_dict.items():
        if len(degerler) > 0:
            plt.figure(figsize=(8, 6))
            plt.boxplot(degerler)
            plt.title(f"{sutun_adi} Değişkeni Kutu Çizimi")
            plt.ylabel("Değerler")
            plt.show()

kutu_cizimi_yap(veri_seti)


def aykiri_deger_bul(liste):
    sirali_liste = sorted(liste)
    n = len(sirali_liste)


    q1_index = int(n * 0.25)
    q3_index = int(n * 0.75)

    q1 = sirali_liste[q1_index]
    q3 = sirali_liste[q3_index]

    iqr = q3 - q1
    alt_sinir = q1 - 1.5 * iqr
    ust_sinir = q3 + 1.5 * iqr

    aykirilar = [x for x in liste if x < alt_sinir or x > ust_sinir]
    temiz_liste = [x for x in liste if alt_sinir <= x <= ust_sinir]

    return aykirilar, temiz_liste, q1, q3, iqr


def merkezi_egilim_hesapla(liste):
    n = len(liste)
    if n == 0: return 0, 0, 0

    toplam = 0
    for x in liste:
        toplam += x
    ortalama = toplam / n

    sirali = sorted(liste)
    if n % 2 == 1:
        medyan = sirali[n // 2]
    else:
        medyan = (sirali[n // 2 - 1] + sirali[n // 2]) / 2

    frekanslar = {}
    for x in liste:
        frekanslar[x] = frekanslar.get(x, 0) + 1

    en_yuksek_frekans = 0
    mod = liste[0]
    for deger, sayi in frekanslar.items():
        if sayi > en_yuksek_frekans:
            en_yuksek_frekans = sayi
            mod = deger

    return ortalama, medyan, mod


import math


def merkezi_dagilim_hesapla(liste, ortalama, q1, q3):
    n = len(liste)
    if n < 2: return [0] * 6

    # 1. Değişim Aralığı (Range)
    degisim_araligi = max(liste) - min(liste)

    oms_toplam = 0
    for x in liste:
        oms_toplam += abs(x - ortalama)
    oms = oms_toplam / n

    varyans_toplam = 0
    for x in liste:
        varyans_toplam += (x - ortalama) ** 2
    varyans = varyans_toplam / (n - 1)

    std_sapma = math.sqrt(varyans)

    degisim_katsayisi = (std_sapma / ortalama) * 100 if ortalama != 0 else 0

    c_acikligi = q3 - q1

    return degisim_araligi, oms, varyans, std_sapma, degisim_katsayisi, c_acikligi


with open("sonuc.txt", "w", encoding="utf-8") as f:
    for baslik, veriler in veri_seti.items():
        aykirilar, temiz_liste, q1, q3, iqr = aykiri_deger_bul(veriler)

        ort, med, mod = merkezi_egilim_hesapla(temiz_liste)
        r, oms, var, std, dk, ca = merkezi_dagilim_hesapla(temiz_liste, ort, q1, q3)

        rapor = f"\n--- {baslik} DEĞİŞKENİ ANALİZİ ---\n"
        rapor += f"Tespit Edilen Aykırı Değerler: {aykirilar[:10]}... (Toplam: {len(aykirilar)})\n"
        rapor += f"Aritmetik Ortalama: {ort:.2f}\nMedyan: {med:.2f}\nMod: {mod:.2f}\n"
        rapor += f"Varyans: {var:.2f}\nStandart Sapma: {std:.2f}\n"
        rapor += f"Değişim Katsayısı: %{dk:.2f}\nÇeyrekler Açıklığı: {ca:.2f}\n"

        print(rapor)
        f.write(rapor)

print("\nİşlem tamamlandı! Sonuçlar 'sonuc.txt' dosyasına kaydedildi.")


