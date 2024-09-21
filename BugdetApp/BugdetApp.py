import json
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Veri dosyasýnýn adý
veri_dosyasi = 'budget_data.json'

def veri_kaydet(gelirler, giderler):
    """
    Gelir ve gider verilerini JSON dosyasýna kaydeden fonksiyon.
    """
    veri = {
        "gelirler": gelirler,
        "giderler": giderler
    }
    with open(veri_dosyasi, 'w') as f:
        json.dump(veri, f)
    print("Veriler baþarýyla kaydedildi.")

def veri_yukle():
    """
    JSON dosyasýndan gelir ve gider verilerini yükleyen fonksiyon.
    """
    if os.path.exists(veri_dosyasi):
        with open(veri_dosyasi, 'r') as f:
            veri = json.load(f)
        print("Veriler baþarýyla yüklendi.")
        return veri["gelirler"], veri["giderler"]
    else:
        print("Henüz kaydedilmiþ bir veri bulunmamaktadýr.")
        return [], []

# Global olarak gelirler ve giderler listesi
gelirler = []
giderler = []

def gelir_ekle():
    """
    Gelir eklemek için kullanýlan GUI fonksiyonu.
    """
    gelir_miktar = gelir_miktar_entry.get()
    gelir_aciklama = gelir_aciklama_entry.get()
    gelir_kategori = gelir_kategori_entry.get()

    if gelir_miktar and gelir_aciklama and gelir_kategori:
        try:
            gelir = {"aciklama": gelir_aciklama, "kategori": gelir_kategori, "miktar": float(gelir_miktar)}
            gelirler.append(gelir)
            messagebox.showinfo("Baþarýlý", "Gelir eklendi.")
            gelir_miktar_entry.delete(0, tk.END)
            gelir_aciklama_entry.delete(0, tk.END)
            gelir_kategori_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")
    else:
        messagebox.showerror("Hata", "Tüm alanlarý doldurmalýsýnýz.")

def gider_ekle():
    """
    Gider eklemek için kullanýlan GUI fonksiyonu.
    """
    gider_miktar = gider_miktar_entry.get()
    gider_aciklama = gider_aciklama_entry.get()
    gider_kategori = gider_kategori_entry.get()

    if gider_miktar and gider_aciklama and gider_kategori:
        try:
            gider = {"aciklama": gider_aciklama, "kategori": gider_kategori, "miktar": float(gider_miktar)}
            giderler.append(gider)
            messagebox.showinfo("Baþarýlý", "Gider eklendi.")
            gider_miktar_entry.delete(0, tk.END)
            gider_aciklama_entry.delete(0, tk.END)
            gider_kategori_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")
    else:
        messagebox.showerror("Hata", "Tüm alanlarý doldurmalýsýnýz.")

def kredi_karti_borc_hesapla(giderler):
    """
    Kredi kartý ile yapýlan harcamalarýn toplamýný hesaplayan fonksiyon.
    """
    toplam_borc = sum([gider["miktar"] for gider in giderler if gider["kategori"].lower() == "kredi kartý"])
    return toplam_borc

def tasarruf_onerileri(giderler):
    """
    Harcamalar gelirlerden fazla ise tasarruf önerileri sunan fonksiyon.
    """
    kategoriler = {}
    
    for gider in giderler:
        kategori = gider["kategori"]
        miktar = gider["miktar"]
        
        if kategori not in kategoriler:
            kategoriler[kategori] = 0
        kategoriler[kategori] += miktar
    
    max_harcama_kategori = max(kategoriler, key=kategoriler.get)
    
    print("\nTasarruf Önerisi:")
    return f"En fazla harcama yaptýðýnýz kategori: {max_harcama_kategori}. Bu kategoride harcamalarýnýzý düþürmeyi deneyin."

def kategori_grafik_goster(kalemler, tur):
    """
    Gelir ve giderleri kategori bazýnda grafiksel olarak gösterir.
    """
    kategoriler = {}
    for kalem in kalemler:
        kategori = kalem["kategori"]
        miktar = kalem["miktar"]
        if kategori not in kategoriler:
            kategoriler[kategori] = 0
        kategoriler[kategori] += miktar

    plt.figure(figsize=(6,6))
    plt.pie(kategoriler.values(), labels=kategoriler.keys(), autopct='%1.1f%%')
    plt.title(f"{tur} Kategorileri Daðýlýmý")
    plt.show()

def rapor_goster():
    """
    Gelir ve giderlerin analizini gösterir, tasarruf önerileri ve kredi kartý borcu raporunu sunar.
    """
    if gelirler and giderler:
        toplam_gelir = sum([gelir["miktar"] for gelir in gelirler])
        toplam_gider = sum([gider["miktar"] for gider in giderler])
        
        kategori_grafik_goster(gelirler, "Gelir")
        kategori_grafik_goster(giderler, "Gider")
        
        kredi_karti_borc = kredi_karti_borc_hesapla(giderler)
        if kredi_karti_borc > 0:
            messagebox.showinfo("Kredi Kartý Borcu", f"Toplam kredi kartý borcunuz: {kredi_karti_borc} TL")
        
        if toplam_gider > toplam_gelir:
            oneriler = tasarruf_onerileri(giderler)
            messagebox.showinfo("Tasarruf Önerisi", oneriler)
    else:
        messagebox.showerror("Hata", "Henüz gelir veya gider eklenmedi.")

# GUI Penceresi Oluþturma
root = tk.Tk()
root.title("Bütçe Yönetim Uygulamasý")

# Gelir Ekleme Arayüzü
gelir_frame = tk.LabelFrame(root, text="Gelir Ekle", padx=10, pady=10)
gelir_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(gelir_frame, text="Gelir Miktarý:").grid(row=0, column=0)
gelir_miktar_entry = tk.Entry(gelir_frame)
gelir_miktar_entry.grid(row=0, column=1)

tk.Label(gelir_frame, text="Gelir Açýklamasý:").grid(row=1, column=0)
gelir_aciklama_entry = tk.Entry(gelir_frame)
gelir_aciklama_entry.grid(row=1, column=1)

tk.Label(gelir_frame, text="Gelir Kategorisi:").grid(row=2, column=0)
gelir_kategori_entry = tk.Entry(gelir_frame)
gelir_kategori_entry.grid(row=2, column=1)

gelir_ekle_button = tk.Button(gelir_frame, text="Gelir Ekle", command=gelir_ekle)
gelir_ekle_button.grid(row=3, columnspan=2, pady=10)

# Gider Ekleme Arayüzü
gider_frame = tk.LabelFrame(root, text="Gider Ekle", padx=10, pady=10)
gider_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(gider_frame, text="Gider Miktarý:").grid(row=0, column=0)
gider_miktar_entry = tk.Entry(gider_frame)
gider_miktar_entry.grid(row=0, column=1)

tk.Label(gider_frame, text="Gider Açýklamasý:").grid(row=1, column=0)
gider_aciklama_entry = tk.Entry(gider_frame)
gider_aciklama_entry.grid(row=1, column=1)

tk.Label(gider_frame, text="Gider Kategorisi:").grid(row=2, column=0)
gider_kategori_entry = tk.Entry(gider_frame)
gider_kategori_entry.grid(row=2, column=1)

gider_ekle_button = tk.Button(gider_frame, text="Gider Ekle", command=gider_ekle)
gider_ekle_button.grid(row=3, columnspan=2, pady=10)

# Rapor Gösterme Butonu
rapor_button = tk.Button(root, text="Rapor ve Grafik Göster", command=rapor_goster)
rapor_button.grid(row=2, column=0, pady=20)

# Uygulama Çalýþtýrma
root.mainloop()
