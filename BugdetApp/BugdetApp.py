import json
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Veri dosyas�n�n ad�
veri_dosyasi = 'budget_data.json'

def veri_kaydet(gelirler, giderler):
    """
    Gelir ve gider verilerini JSON dosyas�na kaydeden fonksiyon.
    """
    veri = {
        "gelirler": gelirler,
        "giderler": giderler
    }
    with open(veri_dosyasi, 'w') as f:
        json.dump(veri, f)
    print("Veriler ba�ar�yla kaydedildi.")

def veri_yukle():
    """
    JSON dosyas�ndan gelir ve gider verilerini y�kleyen fonksiyon.
    """
    if os.path.exists(veri_dosyasi):
        with open(veri_dosyasi, 'r') as f:
            veri = json.load(f)
        print("Veriler ba�ar�yla y�klendi.")
        return veri["gelirler"], veri["giderler"]
    else:
        print("Hen�z kaydedilmi� bir veri bulunmamaktad�r.")
        return [], []

# Global olarak gelirler ve giderler listesi
gelirler = []
giderler = []

def gelir_ekle():
    """
    Gelir eklemek i�in kullan�lan GUI fonksiyonu.
    """
    gelir_miktar = gelir_miktar_entry.get()
    gelir_aciklama = gelir_aciklama_entry.get()
    gelir_kategori = gelir_kategori_entry.get()

    if gelir_miktar and gelir_aciklama and gelir_kategori:
        try:
            gelir = {"aciklama": gelir_aciklama, "kategori": gelir_kategori, "miktar": float(gelir_miktar)}
            gelirler.append(gelir)
            messagebox.showinfo("Ba�ar�l�", "Gelir eklendi.")
            gelir_miktar_entry.delete(0, tk.END)
            gelir_aciklama_entry.delete(0, tk.END)
            gelir_kategori_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "L�tfen ge�erli bir miktar girin.")
    else:
        messagebox.showerror("Hata", "T�m alanlar� doldurmal�s�n�z.")

def gider_ekle():
    """
    Gider eklemek i�in kullan�lan GUI fonksiyonu.
    """
    gider_miktar = gider_miktar_entry.get()
    gider_aciklama = gider_aciklama_entry.get()
    gider_kategori = gider_kategori_entry.get()

    if gider_miktar and gider_aciklama and gider_kategori:
        try:
            gider = {"aciklama": gider_aciklama, "kategori": gider_kategori, "miktar": float(gider_miktar)}
            giderler.append(gider)
            messagebox.showinfo("Ba�ar�l�", "Gider eklendi.")
            gider_miktar_entry.delete(0, tk.END)
            gider_aciklama_entry.delete(0, tk.END)
            gider_kategori_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "L�tfen ge�erli bir miktar girin.")
    else:
        messagebox.showerror("Hata", "T�m alanlar� doldurmal�s�n�z.")

def kredi_karti_borc_hesapla(giderler):
    """
    Kredi kart� ile yap�lan harcamalar�n toplam�n� hesaplayan fonksiyon.
    """
    toplam_borc = sum([gider["miktar"] for gider in giderler if gider["kategori"].lower() == "kredi kart�"])
    return toplam_borc

def tasarruf_onerileri(giderler):
    """
    Harcamalar gelirlerden fazla ise tasarruf �nerileri sunan fonksiyon.
    """
    kategoriler = {}
    
    for gider in giderler:
        kategori = gider["kategori"]
        miktar = gider["miktar"]
        
        if kategori not in kategoriler:
            kategoriler[kategori] = 0
        kategoriler[kategori] += miktar
    
    max_harcama_kategori = max(kategoriler, key=kategoriler.get)
    
    print("\nTasarruf �nerisi:")
    return f"En fazla harcama yapt���n�z kategori: {max_harcama_kategori}. Bu kategoride harcamalar�n�z� d���rmeyi deneyin."

def kategori_grafik_goster(kalemler, tur):
    """
    Gelir ve giderleri kategori baz�nda grafiksel olarak g�sterir.
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
    plt.title(f"{tur} Kategorileri Da��l�m�")
    plt.show()

def rapor_goster():
    """
    Gelir ve giderlerin analizini g�sterir, tasarruf �nerileri ve kredi kart� borcu raporunu sunar.
    """
    if gelirler and giderler:
        toplam_gelir = sum([gelir["miktar"] for gelir in gelirler])
        toplam_gider = sum([gider["miktar"] for gider in giderler])
        
        kategori_grafik_goster(gelirler, "Gelir")
        kategori_grafik_goster(giderler, "Gider")
        
        kredi_karti_borc = kredi_karti_borc_hesapla(giderler)
        if kredi_karti_borc > 0:
            messagebox.showinfo("Kredi Kart� Borcu", f"Toplam kredi kart� borcunuz: {kredi_karti_borc} TL")
        
        if toplam_gider > toplam_gelir:
            oneriler = tasarruf_onerileri(giderler)
            messagebox.showinfo("Tasarruf �nerisi", oneriler)
    else:
        messagebox.showerror("Hata", "Hen�z gelir veya gider eklenmedi.")

# GUI Penceresi Olu�turma
root = tk.Tk()
root.title("B�t�e Y�netim Uygulamas�")

# Gelir Ekleme Aray�z�
gelir_frame = tk.LabelFrame(root, text="Gelir Ekle", padx=10, pady=10)
gelir_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(gelir_frame, text="Gelir Miktar�:").grid(row=0, column=0)
gelir_miktar_entry = tk.Entry(gelir_frame)
gelir_miktar_entry.grid(row=0, column=1)

tk.Label(gelir_frame, text="Gelir A��klamas�:").grid(row=1, column=0)
gelir_aciklama_entry = tk.Entry(gelir_frame)
gelir_aciklama_entry.grid(row=1, column=1)

tk.Label(gelir_frame, text="Gelir Kategorisi:").grid(row=2, column=0)
gelir_kategori_entry = tk.Entry(gelir_frame)
gelir_kategori_entry.grid(row=2, column=1)

gelir_ekle_button = tk.Button(gelir_frame, text="Gelir Ekle", command=gelir_ekle)
gelir_ekle_button.grid(row=3, columnspan=2, pady=10)

# Gider Ekleme Aray�z�
gider_frame = tk.LabelFrame(root, text="Gider Ekle", padx=10, pady=10)
gider_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(gider_frame, text="Gider Miktar�:").grid(row=0, column=0)
gider_miktar_entry = tk.Entry(gider_frame)
gider_miktar_entry.grid(row=0, column=1)

tk.Label(gider_frame, text="Gider A��klamas�:").grid(row=1, column=0)
gider_aciklama_entry = tk.Entry(gider_frame)
gider_aciklama_entry.grid(row=1, column=1)

tk.Label(gider_frame, text="Gider Kategorisi:").grid(row=2, column=0)
gider_kategori_entry = tk.Entry(gider_frame)
gider_kategori_entry.grid(row=2, column=1)

gider_ekle_button = tk.Button(gider_frame, text="Gider Ekle", command=gider_ekle)
gider_ekle_button.grid(row=3, columnspan=2, pady=10)

# Rapor G�sterme Butonu
rapor_button = tk.Button(root, text="Rapor ve Grafik G�ster", command=rapor_goster)
rapor_button.grid(row=2, column=0, pady=20)

# Uygulama �al��t�rma
root.mainloop()
