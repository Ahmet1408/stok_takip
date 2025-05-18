import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, scrolledtext
from datetime import datetime
import csv
import os
import hashlib


kullanicilar = []
urunler = []
cariler = []
stok_hareketleri = []

class Veritabani:
    @staticmethod
    def sifrele(metin):
        return hashlib.sha256(metin.encode()).hexdigest()

    @staticmethod
    def kullanici_ekle(kullanici_adi, sifre, firma, yetki_seviyesi=1, eposta=None, telefon=None):
        for kullanici in kullanicilar:
            if kullanici['kullanici_adi'] == kullanici_adi:
                return False
        kullanicilar.append({
            'id': len(kullanicilar) + 1,
            'kullanici_adi': kullanici_adi,
            'sifre': Veritabani.sifrele(sifre),
            'firma': firma,
            'yetki_seviyesi': yetki_seviyesi,
            'eposta': eposta,
            'telefon': telefon,
            'son_giris': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True

    @staticmethod
    def kullanici_giris(kullanici_adi, sifre):
        for kullanici in kullanicilar:
            if kullanici['kullanici_adi'] == kullanici_adi and kullanici['sifre'] == Veritabani.sifrele(sifre):
                kullanici['son_giris'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return {
                    'id': kullanici['id'],
                    'kullanici_adi': kullanici['kullanici_adi'],
                    'firma': kullanici['firma'],
                    'yetki_seviyesi': kullanici['yetki_seviyesi'],
                    'eposta': kullanici['eposta'],
                    'telefon': kullanici['telefon']
                }
        return None

    @staticmethod
    def urun_ekle(barkod, isim, stok, ekleyen, firma, cari_id=None, kritik_stok=10, 
                  birim='adet', fiyat=0.0, kdv_orani=18, aciklama=None):
        for urun in urunler:
            if urun['barkod'] == barkod and urun['firma'] == firma:
                return None
        urun_id = len(urunler) + 1
        urun = {
            'id': urun_id,
            'barkod': barkod,
            'isim': isim,
            'stok': stok,
            'kritik_stok': kritik_stok,
            'birim': birim,
            'fiyat': fiyat,
            'kdv_orani': kdv_orani,
            'ekleyen': ekleyen,
            'eklenme_tarihi': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'guncelleme_tarihi': None,
            'firma': firma,
            'cari_id': cari_id,
            'aciklama': aciklama
        }
        urunler.append(urun)
        
       
        stok_hareketleri.append({
            'id': len(stok_hareketleri) + 1,
            'urun_id': urun_id,
            'hareket_tipi': 'giris',
            'miktar': stok,
            'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'kullanici': ekleyen,
            'firma': firma,
            'referans': None,
            'aciklama': 'İlk stok girişi'
        })
        return urun_id

    @staticmethod
    def urun_guncelle(urun_id, firma, **kwargs):
        for urun in urunler:
            if urun['id'] == urun_id and urun['firma'] == firma:
                for key, value in kwargs.items():
                    urun[key] = value
                urun['guncelleme_tarihi'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return True
        return False

    @staticmethod
    def urun_sil(urun_id, firma):
        global urunler
        urunler = [urun for urun in urunler if not (urun['id'] == urun_id and urun['firma'] == firma)]
        return True

    @staticmethod
    def urun_getir(urun_id, firma):
        for urun in urunler:
            if urun['id'] == urun_id and urun['firma'] == firma:
                return urun
        return None

    @staticmethod
    def urunleri_listele(firma, filtre=None):
        result = []
        for urun in urunler:
            if urun['firma'] == firma:
                cari_ad = None
                if urun['cari_id']:
                    for cari in cariler:
                        if cari['id'] == urun['cari_id']:
                            cari_ad = cari['ad']
                            break
                urun_dict = urun.copy()
                urun_dict['cari_ad'] = cari_ad
                if filtre:
                    if (filtre.lower() in urun['isim'].lower() or 
                        (urun['barkod'] and filtre.lower() in urun['barkod'].lower()) or
                        (cari_ad and filtre.lower() in cari_ad.lower())):
                        result.append(urun_dict)
                else:
                    result.append(urun_dict)
        return result

    @staticmethod
    def kritik_stoktaki_urunler(firma):
        return [urun for urun in urunler if urun['firma'] == firma and urun['stok'] <= urun['kritik_stok']]

    @staticmethod
    def cari_ekle(cari_kodu, ad, firma, vergi_no=None, vergi_dairesi=None, 
                  adres=None, telefon=None, eposta=None, yetkili=None, aciklama=None):
        for cari in cariler:
            if cari['cari_kodu'] == cari_kodu and cari['firma'] == firma:
                return None
        cari_id = len(cariler) + 1
        cariler.append({
            'id': cari_id,
            'cari_kodu': cari_kodu,
            'ad': ad,
            'vergi_no': vergi_no,
            'vergi_dairesi': vergi_dairesi,
            'adres': adres,
            'telefon': telefon,
            'eposta': eposta,
            'yetkili': yetkili,
            'firma': firma,
            'kayit_tarihi': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'aciklama': aciklama
        })
        return cari_id

    @staticmethod
    def carileri_listele(firma, filtre=None):
        result = []
        for cari in cariler:
            if cari['firma'] == firma:
                if filtre:
                    if (filtre.lower() in cari['ad'].lower() or 
                        filtre.lower() in cari['cari_kodu'].lower() or
                        (cari['vergi_no'] and filtre.lower() in cari['vergi_no'].lower())):
                        result.append(cari)
                else:
                    result.append(cari)
        return result

    @staticmethod
    def cari_getir(cari_id, firma):
        for cari in cariler:
            if cari['id'] == cari_id and cari['firma'] == firma:
                return cari
        return None

    @staticmethod
    def stok_hareketi_ekle(urun_id, hareket_tipi, miktar, kullanici, firma, referans=None, aciklama=None):
        stok_hareketleri.append({
            'id': len(stok_hareketleri) + 1,
            'urun_id': urun_id,
            'hareket_tipi': hareket_tipi,
            'miktar': miktar,
            'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'kullanici': kullanici,
            'firma': firma,
            'referans': referans,
            'aciklama': aciklama
        })
        for urun in urunler:
            if urun['id'] == urun_id and urun['firma'] == firma:
                if hareket_tipi == 'giris':
                    urun['stok'] += miktar
                elif hareket_tipi == 'cikis':
                    urun['stok'] -= miktar
                return stok_hareketleri[-1]['id']
        return None

    @staticmethod
    def stok_hareketlerini_getir(firma, urun_id=None, baslangic_tarihi=None, bitis_tarihi=None):
        result = []
        for hareket in stok_hareketleri:
            if hareket['firma'] == firma:
                if urun_id and hareket['urun_id'] != urun_id:
                    continue
                if baslangic_tarihi and bitis_tarihi:
                    if not (baslangic_tarihi <= hareket['tarih'] <= bitis_tarihi):
                        continue
                for urun in urunler:
                    if urun['id'] == hareket['urun_id']:
                        hareket_dict = hareket.copy()
                        hareket_dict['urun_adi'] = urun['isim']
                        hareket_dict['barkod'] = urun['barkod']
                        result.append(hareket_dict)
                        break
        return sorted(result, key=lambda x: x['tarih'], reverse=True)

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        style = ttk.Style()
        style.configure('Modern.TButton', 
                        font=('Helvetica', 10, 'bold'),
                        padding=6,
                        foreground='#333',
                        background='#4CAF50',
                        bordercolor='#4CAF50',
                        lightcolor='#4CAF50',
                        darkcolor='#4CAF50')
        kwargs['style'] = 'Modern.TButton'
        super().__init__(master, **kwargs)

class StokYonetimUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Stok Yönetim Sistemi")
        self.root.geometry("1200x800")
        self.root.state('zoomed')
        self.kullanici = None
        self.firma = None
        self.yetki_seviyesi = 1
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.giris_ekrani()

    def giris_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        login_frame = ttk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(login_frame, text="Stok Yönetim Sistemi", 
                  font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(login_frame, text="Kullanıcı Adı:", 
                  font=('Helvetica', 10)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.kullanici_adi_entry = ttk.Entry(login_frame, font=('Helvetica', 10))
        self.kullanici_adi_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(login_frame, text="Şifre:", 
                  font=('Helvetica', 10)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.sifre_entry = ttk.Entry(login_frame, show="*", font=('Helvetica', 10))
        self.sifre_entry.grid(row=2, column=1, padx=10, pady=5)
        
        giris_btn = ModernButton(login_frame, text="Giriş Yap", 
                                 command=self.giris_yap)
        giris_btn.grid(row=3, column=0, columnspan=2, pady=15, ipadx=20)
        
        kayit_btn = ttk.Button(login_frame, text="Kayıt Ol", 
                               command=self.kayit_ekrani)
        kayit_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.root.bind('<Return>', lambda event: self.giris_yap())
        self.kullanici_adi_entry.focus()

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        
        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre giriniz")
            return
        
        try:
            kullanici = Veritabani.kullanici_giris(kullanici_adi, sifre)
            if kullanici:
                self.kullanici = kullanici['kullanici_adi']
                self.firma = kullanici['firma']
                self.yetki_seviyesi = kullanici['yetki_seviyesi']
                self.ana_ekran()
            else:
                messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre")
        except Exception as e:
            messagebox.showerror("Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")

    def kayit_ekrani(self):
        kayit_pencere = tk.Toplevel(self.root)
        kayit_pencere.title("Yeni Kullanıcı Kaydı")
        kayit_pencere.geometry("400x400")
        kayit_pencere.resizable(False, False)
        
        ttk.Label(kayit_pencere, text="Yeni Kullanıcı Kaydı", 
                  font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(kayit_pencere)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(form_frame, text="Kullanıcı Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        k_adi_entry = ttk.Entry(form_frame)
        k_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Şifre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        sifre_entry = ttk.Entry(form_frame, show="*")
        sifre_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Şifre Tekrar:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sifre_tekrar_entry = ttk.Entry(form_frame, show="*")
        sifre_tekrar_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Firma Adı:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        firma_entry = ttk.Entry(form_frame)
        firma_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="E-posta:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        eposta_entry = ttk.Entry(form_frame)
        eposta_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Telefon:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        telefon_entry = ttk.Entry(form_frame)
        telefon_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        
        kaydet_btn = ModernButton(form_frame, text="Kayıt Ol", 
                                 command=lambda: self.kayit_ol(
                                     k_adi_entry.get(),
                                     sifre_entry.get(),
                                     sifre_tekrar_entry.get(),
                                     firma_entry.get(),
                                     eposta_entry.get(),
                                     telefon_entry.get(),
                                     kayit_pencere
                                 ))
        kaydet_btn.grid(row=6, column=0, columnspan=2, pady=15, ipadx=20)
        
        form_frame.columnconfigure(1, weight=1)
        kayit_pencere.grab_set()
        k_adi_entry.focus()

    def kayit_ol(self, kullanici_adi, sifre, sifre_tekrar, firma, eposta, telefon, pencere):
        if not all([kullanici_adi, sifre, sifre_tekrar, firma]):
            messagebox.showerror("Hata", "Zorunlu alanları doldurun")
            return
        
        if sifre != sifre_tekrar:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor")
            return
        
        if Veritabani.kullanici_ekle(kullanici_adi, sifre, firma, 1, eposta, telefon):
            messagebox.showinfo("Başarılı", "Kayıt başarılı. Giriş yapabilirsiniz.")
            pencere.destroy()
        else:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten alınmış")

    def ana_ekran(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.menu_cubugu = tk.Menu(self.root)
        self.root.config(menu=self.menu_cubugu)
        
        dosya_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        dosya_menu.add_command(label="Yedek Al", command=self.yedek_al)
        dosya_menu.add_command(label="Yedekten Yükle", command=self.yedekten_yukle)
        dosya_menu.add_separator()
        dosya_menu.add_command(label="Çıkış", command=self.cikis_yap)
        self.menu_cubugu.add_cascade(label="Dosya", menu=dosya_menu)
        
        stok_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        stok_menu.add_command(label="Ürün Ekle", command=self.urun_ekle_ekrani)
        stok_menu.add_command(label="Stok Hareketleri", command=self.stok_hareketleri_ekrani)
        stok_menu.add_command(label="Stok Raporları", command=self.stok_raporlari_ekrani)
        self.menu_cubugu.add_cascade(label="Stok", menu=stok_menu)
        
        cari_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        cari_menu.add_command(label="Cari Ekle", command=self.cari_ekle_ekrani)
        cari_menu.add_command(label="Cari Listesi", command=self.cari_listesi_ekrani)
        self.menu_cubugu.add_cascade(label="Cari", menu=cari_menu)
        
        yardim_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        yardim_menu.add_command(label="Kullanım Kılavuzu", command=self.kullanim_kilavuzu)
        yardim_menu.add_command(label="Hakkında", command=self.hakkinda)
        self.menu_cubugu.add_cascade(label="Yardım", menu=yardim_menu)
        
        ana_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        ana_panel.pack(fill=tk.BOTH, expand=True)
        
        sol_panel = ttk.Frame(ana_panel, width=300, relief=tk.RIDGE)
        ana_panel.add(sol_panel, weight=1)
        
        ttk.Label(sol_panel, text="Dashboard", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        user_frame = ttk.LabelFrame(sol_panel, text="Kullanıcı Bilgileri")
        user_frame.pack(padx=10, pady=5, fill='x')
        
        ttk.Label(user_frame, text=f"Kullanıcı: {self.kullanici}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(user_frame, text=f"Firma: {self.firma}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(user_frame, text=f"Yetki: {'Admin' if self.yetki_seviyesi == 2 else 'Standart'}").pack(anchor='w', padx=5, pady=2)
        
        quick_frame = ttk.LabelFrame(sol_panel, text="Hızlı Erişim")
        quick_frame.pack(padx=10, pady=5, fill='x')
        
        ModernButton(quick_frame, text="Ürün Ekle", 
                     command=self.urun_ekle_ekrani).pack(fill='x', padx=5, pady=2)
        ModernButton(quick_frame, text="Cari Ekle", 
                     command=self.cari_ekle_ekrani).pack(fill='x', padx=5, pady=2)
        ModernButton(quick_frame, text="Stok Raporu", 
                     command=self.stok_raporlari_ekrani).pack(fill='x', padx=5, pady=2)
        
        kritik_urunler = Veritabani.kritik_stoktaki_urunler(self.firma)
        if kritik_urunler:
            uyari_frame = ttk.LabelFrame(sol_panel, text="Kritik Stok Uyarıları")
            uyari_frame.pack(padx=10, pady=5, fill='x')
            for urun in kritik_urunler:
                ttk.Label(uyari_frame, 
                          text=f"{urun['isim']} - {urun['stok']}/{urun['kritik_stok']} {urun['birim']}",
                          foreground='red').pack(anchor='w', padx=5, pady=2)
        
        sag_panel = ttk.Frame(ana_panel)
        ana_panel.add(sag_panel, weight=4)
        
        self.notebook = ttk.Notebook(sag_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        urun_listesi_frame = ttk.Frame(self.notebook)
        self.notebook.add(urun_listesi_frame, text="Ürün Listesi")
        self.urun_listesi_ekrani(urun_listesi_frame)
        
        stok_grafik_frame = ttk.Frame(self.notebook)
        self.notebook.add(stok_grafik_frame, text="Stok Grafiği")
        self.stok_grafigi_ekrani(stok_grafik_frame)
        
        self.status_bar = ttk.Label(self.root, text=f"Hoş geldiniz {self.kullanici} | Firma: {self.firma}", 
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def urun_listesi_ekrani(self, parent):
        arama_frame = ttk.Frame(parent)
        arama_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(arama_frame, text="Ara:").pack(side=tk.LEFT, padx=5)
        self.urun_arama_entry = ttk.Entry(arama_frame)
        self.urun_arama_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.urun_arama_entry.bind('<KeyRelease>', self.urun_ara)
        
        ModernButton(arama_frame, text="Excel'e Aktar", 
                     command=self.urun_excel_aktar).pack(side=tk.RIGHT, padx=5)
        ModernButton(arama_frame, text="Yenile", 
                     command=lambda: self.urun_ara(None)).pack(side=tk.RIGHT, padx=5)
        
        columns = ("ID", "Barkod", "Ürün Adı", "Stok", "Birim", "Fiyat", "Cari")
        self.urun_tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.urun_tree.heading(col, text=col)
            self.urun_tree.column(col, width=100, anchor='center')
        
        self.urun_tree.column("Ürün Adı", width=200, anchor='w')
        self.urun_tree.column("Cari", width=150, anchor='w')
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.urun_tree.yview)
        self.urun_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.urun_tree.pack(fill=tk.BOTH, expand=True)
        
        self.urun_menu = tk.Menu(self.root, tearoff=0)
        self.urun_menu.add_command(label="Düzenle", command=self.urun_duzenle)
        self.urun_menu.add_command(label="Sil", command=self.urun_sil)
        self.urun_menu.add_command(label="Barkod Oluştur", command=self.barkod_olustur)
        self.urun_menu.add_command(label="Stok Hareketleri", command=self.urun_stok_hareketleri)
        self.urun_tree.bind("<Button-3>", self.urun_sag_tik)
        
        self.urun_tree.bind("<Double-1>", lambda e: self.urun_duzenle())
        self.urun_ara(None)

    def urun_ara(self, event):
        filtre = self.urun_arama_entry.get()
        urunler = Veritabani.urunleri_listele(self.firma, filtre)
        
        for item in self.urun_tree.get_children():
            self.urun_tree.delete(item)
        
        for urun in urunler:
            self.urun_tree.insert('', tk.END, 
                                  values=(urun['id'], urun['barkod'], urun['isim'], urun['stok'], 
                                          urun['birim'], f"{urun['fiyat']:.2f} ₺", urun['cari_ad']))

    def urun_ekle_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Ürün Ekle")
        pencere.geometry("500x600")
        pencere.resizable(False, False)
        
        ttk.Label(pencere, text="Yeni Ürün Ekle", 
                  font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(pencere)
        form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(form_frame, text="Ürün Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        isim_entry = ttk.Entry(form_frame)
        isim_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Barkod:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        barkod_entry = ttk.Entry(form_frame)
        barkod_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Stok Miktarı:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        stok_entry = ttk.Spinbox(form_frame, from_=0, to=10000)
        stok_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Kritik Stok:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        kritik_stok_entry = ttk.Spinbox(form_frame, from_=0, to=10000)
        kritik_stok_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Birim:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        birim_combobox = ttk.Combobox(form_frame, values=['adet', 'kg', 'lt', 'metre', 'paket', 'kutu'])
        birim_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        birim_combobox.set('adet')
        
        ttk.Label(form_frame, text="Fiyat:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        fiyat_entry = ttk.Entry(form_frame)
        fiyat_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="KDV Oranı (%):").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        kdv_entry = ttk.Entry(form_frame)
        kdv_entry.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        kdv_entry.insert(0, "18")
        
        ttk.Label(form_frame, text="Cari:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        cari_combobox = ttk.Combobox(form_frame, values=[cari['ad'] for cari in Veritabani.carileri_listele(self.firma)])
        cari_combobox.grid(row=7, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Açıklama:").grid(row=8, column=0, padx=5, pady=5, sticky='ne')
        aciklama_text = scrolledtext.ScrolledText(form_frame, height=4)
        aciklama_text.grid(row=8, column=1, padx=5, pady=5, sticky='we')
        
        kaydet_btn = ModernButton(form_frame, text="Kaydet", 
                                 command=lambda: self.urun_ekle(
                                     isim_entry.get(),
                                     barkod_entry.get(),
                                     stok_entry.get(),
                                     kritik_stok_entry.get(),
                                     birim_combobox.get(),
                                     fiyat_entry.get(),
                                     kdv_entry.get(),
                                     cari_combobox.get(),
                                     aciklama_text.get("1.0", tk.END).strip(),
                                     pencere
                                 ))
        kaydet_btn.grid(row=9, column=0, columnspan=2, pady=15, ipadx=20)
        
        form_frame.columnconfigure(1, weight=1)

    def urun_ekle(self, isim, barkod, stok, kritik_stok, birim, fiyat, kdv, cari_ad, aciklama, pencere):
        if not isim or not stok:
            messagebox.showerror("Hata", "Ürün adı ve stok miktarı zorunludur")
            return
        
        try:
            stok = int(stok)
            kritik_stok = int(kritik_stok) if kritik_stok else 10
            fiyat = float(fiyat) if fiyat else 0.0
            kdv = int(kdv) if kdv else 18
        except ValueError:
            messagebox.showerror("Hata", "Stok, kritik stok, fiyat ve KDV sayısal olmalı")
            return
        
        cari_id = None
        if cari_ad:
            for cari in Veritabani.carileri_listele(self.firma):
                if cari['ad'] == cari_ad:
                    cari_id = cari['id']
                    break
        
        urun_id = Veritabani.urun_ekle(
            barkod=barkod, isim=isim, stok=stok, ekleyen=self.kullanici, firma=self.firma,
            cari_id=cari_id, kritik_stok=kritik_stok, birim=birim, fiyat=fiyat, 
            kdv_orani=kdv, aciklama=aciklama
        )
        
        if urun_id:
            messagebox.showinfo("Başarılı", "Ürün eklendi")
            pencere.destroy()
            self.urun_ara(None)
        else:
            messagebox.showerror("Hata", "Bu barkod zaten kullanımda")

    def urun_duzenle(self):
        selected_item = self.urun_tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        urun_id = int(self.urun_tree.item(selected_item)['values'][0])
        urun = Veritabani.urun_getir(urun_id, self.firma)
        if not urun:
            messagebox.showerror("Hata", "Ürün bulunamadı")
            return
        
        pencere = tk.Toplevel(self.root)
        pencere.title("Ürün Düzenle")
        pencere.geometry("500x600")
        pencere.resizable(False, False)
        
        ttk.Label(pencere, text="Ürün Düzenle", 
                  font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(pencere)
        form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(form_frame, text="Ürün Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        isim_entry = ttk.Entry(form_frame)
        isim_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        isim_entry.insert(0, urun['isim'])
        
        ttk.Label(form_frame, text="Barkod:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        barkod_entry = ttk.Entry(form_frame)
        barkod_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        barkod_entry.insert(0, urun['barkod'])
        
        ttk.Label(form_frame, text="Stok Miktarı:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        stok_entry = ttk.Spinbox(form_frame, from_=0, to=10000)
        stok_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        stok_entry.insert(0, urun['stok'])
        
        ttk.Label(form_frame, text="Kritik Stok:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        kritik_stok_entry = ttk.Spinbox(form_frame, from_=0, to=10000)
        kritik_stok_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        kritik_stok_entry.insert(0, urun['kritik_stok'])
        
        ttk.Label(form_frame, text="Birim:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        birim_combobox = ttk.Combobox(form_frame, values=['adet', 'kg', 'lt', 'metre', 'paket', 'kutu'])
        birim_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        birim_combobox.set(urun['birim'])
        
        ttk.Label(form_frame, text="Fiyat:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        fiyat_entry = ttk.Entry(form_frame)
        fiyat_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        fiyat_entry.insert(0, str(urun['fiyat']))
        
        ttk.Label(form_frame, text="KDV Oranı (%):").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        kdv_entry = ttk.Entry(form_frame)
        kdv_entry.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        kdv_entry.insert(0, str(urun['kdv_orani']))
        
        ttk.Label(form_frame, text="Cari:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        cari_combobox = ttk.Combobox(form_frame, values=[cari['ad'] for cari in Veritabani.carileri_listele(self.firma)])
        cari_combobox.grid(row=7, column=1, padx=5, pady=5, sticky='we')
        if urun['cari_id']:
            for cari in Veritabani.carileri_listele(self.firma):
                if cari['id'] == urun['cari_id']:
                    cari_combobox.set(cari['ad'])
                    break
        
        ttk.Label(form_frame, text="Açıklama:").grid(row=8, column=0, padx=5, pady=5, sticky='ne')
        aciklama_text = scrolledtext.ScrolledText(form_frame, height=4)
        aciklama_text.grid(row=8, column=1, padx=5, pady=5, sticky='we')
        if urun['aciklama']:
            aciklama_text.insert("1.0", urun['aciklama'])
        
        kaydet_btn = ModernButton(form_frame, text="Kaydet", 
                                 command=lambda: self.urun_guncelle(
                                     urun_id,
                                     isim_entry.get(),
                                     barkod_entry.get(),
                                     stok_entry.get(),
                                     kritik_stok_entry.get(),
                                     birim_combobox.get(),
                                     fiyat_entry.get(),
                                     kdv_entry.get(),
                                     cari_combobox.get(),
                                     aciklama_text.get("1.0", tk.END).strip(),
                                     pencere
                                 ))
        kaydet_btn.grid(row=9, column=0, columnspan=2, pady=15, ipadx=20)
        
        form_frame.columnconfigure(1, weight=1)

    def urun_guncelle(self, urun_id, isim, barkod, stok, kritik_stok, birim, fiyat, kdv, cari_ad, aciklama, pencere):
        if not isim or not stok:
            messagebox.showerror("Hata", "Ürün adı ve stok miktarı zorunludur")
            return
        
        try:
            stok = int(stok)
            kritik_stok = int(kritik_stok) if kritik_stok else 10
            fiyat = float(fiyat) if fiyat else 0.0
            kdv = int(kdv) if kdv else 18
        except ValueError:
            messagebox.showerror("Hata", "Stok, kritik stok, fiyat ve KDV sayısal olmalı")
            return
        
        cari_id = None
        if cari_ad:
            for cari in Veritabani.carileri_listele(self.firma):
                if cari['ad'] == cari_ad:
                    cari_id = cari['id']
                    break
        
        if Veritabani.urun_guncelle(
            urun_id=urun_id, firma=self.firma,
            isim=isim, barkod=barkod, stok=stok, kritik_stok=kritik_stok,
            birim=birim, fiyat=fiyat, kdv_orani=kdv, cari_id=cari_id, aciklama=aciklama
        ):
            messagebox.showinfo("Başarılı", "Ürün güncellendi")
            pencere.destroy()
            self.urun_ara(None)
        else:
            messagebox.showerror("Hata", "Ürün güncelleme başarısız")

    def urun_sil(self):
        selected_item = self.urun_tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        urun_id = int(self.urun_tree.item(selected_item)['values'][0])
        if messagebox.askyesno("Onay", "Bu ürünü silmek istediğinize emin misiniz?"):
            if Veritabani.urun_sil(urun_id, self.firma):
                messagebox.showinfo("Başarılı", "Ürün silindi")
                self.urun_ara(None)
            else:
                messagebox.showerror("Hata", "Ürün silme başarısız")

    def urun_sag_tik(self, event):
        item = self.urun_tree.identify_row(event.y)
        if item:
            self.urun_tree.selection_set(item)
            self.urun_menu.post(event.x_root, event.y_root)

    def barkod_olustur(self):
        selected_item = self.urun_tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        messagebox.showinfo("Bilgi", "Barkod oluşturma özelliği henüz uygulanmadı")

    def urun_stok_hareketleri(self):
        selected_item = self.urun_tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        urun_id = int(self.urun_tree.item(selected_item)['values'][0])
        pencere = tk.Toplevel(self.root)
        pencere.title("Stok Hareketleri")
        pencere.geometry("800x400")
        
        columns = ("ID", "Ürün Adı", "Barkod", "Hareket Tipi", "Miktar", "Tarih", "Kullanıcı")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        tree.column("Ürün Adı", width=150, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        hareketler = Veritabani.stok_hareketlerini_getir(self.firma, urun_id=urun_id)
        for hareket in hareketler:
            tree.insert('', tk.END, 
                        values=(hareket['id'], hareket['urun_adi'], hareket['barkod'], 
                                hareket['hareket_tipi'], hareket['miktar'], 
                                hareket['tarih'], hareket['kullanici']))

    def cari_ekle_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Yeni Cari Ekle")
        pencere.geometry("500x600")
        pencere.resizable(False, False)
        
        ttk.Label(pencere, text="Yeni Cari Ekle", 
                  font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(pencere)
        form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(form_frame, text="Cari Kodu:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        cari_kodu_entry = ttk.Entry(form_frame)
        cari_kodu_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Ad:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ad_entry = ttk.Entry(form_frame)
        ad_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Vergi No:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        vergi_no_entry = ttk.Entry(form_frame)
        vergi_no_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Vergi Dairesi:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        vergi_dairesi_entry = ttk.Entry(form_frame)
        vergi_dairesi_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Adres:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        adres_entry = ttk.Entry(form_frame)
        adres_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Telefon:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        telefon_entry = ttk.Entry(form_frame)
        telefon_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="E-posta:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        eposta_entry = ttk.Entry(form_frame)
        eposta_entry.grid(row=6, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Yetkili:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        yetkili_entry = ttk.Entry(form_frame)
        yetkili_entry.grid(row=7, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(form_frame, text="Açıklama:").grid(row=8, column=0, padx=5, pady=5, sticky='ne')
        aciklama_text = scrolledtext.ScrolledText(form_frame, height=4)
        aciklama_text.grid(row=8, column=1, padx=5, pady=5, sticky='we')
        
        kaydet_btn = ModernButton(form_frame, text="Kaydet", 
                                 command=lambda: self.cari_ekle(
                                     cari_kodu_entry.get(),
                                     ad_entry.get(),
                                     vergi_no_entry.get(),
                                     vergi_dairesi_entry.get(),
                                     adres_entry.get(),
                                     telefon_entry.get(),
                                     eposta_entry.get(),
                                     yetkili_entry.get(),
                                     aciklama_text.get("1.0", tk.END).strip(),
                                     pencere
                                 ))
        kaydet_btn.grid(row=9, column=0, columnspan=2, pady=15, ipadx=20)
        
        form_frame.columnconfigure(1, weight=1)

    def cari_ekle(self, cari_kodu, ad, vergi_no, vergi_dairesi, adres, telefon, eposta, yetkili, aciklama, pencere):
        if not cari_kodu or not ad:
            messagebox.showerror("Hata", "Cari kodu ve ad zorunludur")
            return
        
        cari_id = Veritabani.cari_ekle(
            cari_kodu=cari_kodu, ad=ad, firma=self.firma, vergi_no=vergi_no,
            vergi_dairesi=vergi_dairesi, adres=adres, telefon=telefon,
            eposta=eposta, yetkili=yetkili, aciklama=aciklama
        )
        
        if cari_id:
            messagebox.showinfo("Başarılı", "Cari eklendi")
            pencere.destroy()
        else:
            messagebox.showerror("Hata", "Bu cari kodu zaten kullanımda")

    def cari_listesi_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Cari Listesi")
        pencere.geometry("800x400")
        
        arama_frame = ttk.Frame(pencere)
        arama_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(arama_frame, text="Ara:").pack(side=tk.LEFT, padx=5)
        arama_entry = ttk.Entry(arama_frame)
        arama_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        columns = ("ID", "Cari Kodu", "Ad", "Vergi No", "Telefon", "E-posta")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        tree.column("Ad", width=150, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def ara(event=None):
            filtre = arama_entry.get()
            for item in tree.get_children():
                tree.delete(item)
            cariler = Veritabani.carileri_listele(self.firma, filtre)
            for cari in cariler:
                tree.insert('', tk.END, 
                            values=(cari['id'], cari['cari_kodu'], cari['ad'], 
                                    cari['vergi_no'], cari['telefon'], cari['eposta']))
        
        arama_entry.bind('<KeyRelease>', ara)
        ara()

    def stok_hareketleri_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Stok Hareketleri")
        pencere.geometry("800x400")
        
        columns = ("ID", "Ürün Adı", "Barkod", "Hareket Tipi", "Miktar", "Tarih", "Kullanıcı")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        tree.column("Ürün Adı", width=150, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        hareketler = Veritabani.stok_hareketlerini_getir(self.firma)
        for hareket in hareketler:
            tree.insert('', tk.END, 
                        values=(hareket['id'], hareket['urun_adi'], hareket['barkod'], 
                                hareket['hareket_tipi'], hareket['miktar'], 
                                hareket['tarih'], hareket['kullanici']))

    def stok_raporlari_ekrani(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Stok Raporları")
        pencere.geometry("600x400")
        
        ttk.Label(pencere, text="Stok Raporları", 
                  font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        rapor_frame = ttk.Frame(pencere)
        rapor_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ModernButton(rapor_frame, text="Tüm Ürünler Raporu", 
                     command=lambda: self.urun_excel_aktar()).pack(fill='x', padx=5, pady=5)
        ModernButton(rapor_frame, text="Kritik Stok Raporu", 
                     command=self.kritik_stok_raporu).pack(fill='x', padx=5, pady=5)

    def kritik_stok_raporu(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Kritik Stok Raporu")
        pencere.geometry("600x400")
        
        columns = ("ID", "Barkod", "Ürün Adı", "Stok", "Kritik Stok", "Birim")
        tree = ttk.Treeview(pencere, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        tree.column("Ürün Adı", width=150, anchor='w')
        
        scrollbar = ttk.Scrollbar(pencere, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        kritik_urunler = Veritabani.kritik_stoktaki_urunler(self.firma)
        for urun in kritik_urunler:
            tree.insert('', tk.END, 
                        values=(urun['id'], urun['barkod'], urun['isim'], 
                                urun['stok'], urun['kritik_stok'], urun['birim']))

    def yedek_al(self):
        dosya = filedialog.asksaveasfilename(defaultextension=".csv", 
                                             filetypes=[("CSV dosyaları", "*.csv")])
        if dosya:
            with open(dosya, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Tablo", "Veri"])
                writer.writerow(["Kullanicilar", kullanicilar])
                writer.writerow(["Urunler", urunler])
                writer.writerow(["Cariler", cariler])
                writer.writerow(["Stok Hareketleri", stok_hareketleri])
            messagebox.showinfo("Başarılı", "Yedek alındı")

    def yedekten_yukle(self):
        dosya = filedialog.askopenfilename(filetypes=[("CSV dosyaları", "*.csv")])
        if dosya:
            global kullanicilar, urunler, cariler, stok_hareketleri
            with open(dosya, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Başlık satırını atla
                for row in reader:
                    if row[0] == "Kullanicilar":
                        kullanicilar = eval(row[1])
                    elif row[0] == "Urunler":
                        urunler = eval(row[1])
                    elif row[0] == "Cariler":
                        cariler = eval(row[1])
                    elif row[0] == "Stok Hareketleri":
                        stok_hareketleri = eval(row[1])
            messagebox.showinfo("Başarılı", "Yedek yüklendi")
            self.urun_ara(None)

    def urun_excel_aktar(self):
        dosya = filedialog.asksaveasfilename(defaultextension=".csv", 
                                             filetypes=[("CSV dosyaları", "*.csv")])
        if dosya:
            with open(dosya, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Barkod", "Ürün Adı", "Stok", "Birim", "Fiyat", "Cari"])
                for urun in Veritabani.urunleri_listele(self.firma):
                    writer.writerow([urun['id'], urun['barkod'], urun['isim'], 
                                     urun['stok'], urun['birim'], urun['fiyat'], urun['cari_ad']])
            messagebox.showinfo("Başarılı", "Ürünler CSV'ye aktarıldı")

    def stok_grafigi_ekrani(self, parent):
        ttk.Label(parent, text="Stok Grafiği (Henüz uygulanmadı)", 
                  font=('Helvetica', 12, 'bold')).pack(pady=20)

    def kullanim_kilavuzu(self):
        messagebox.showinfo("Kullanım Kılavuzu", "Stok Yönetim Sistemi Kullanım Kılavuzu:\n1. Giriş yapın veya kayıt olun.\n2. Ürün ve cari ekleyin.\n3. Stok hareketlerini izleyin.")

    def hakkinda(self):
        messagebox.showinfo("Hakkında", "Stok Yönetim Sistemi v1.0\nHazırlayan: Efe Ahmet")

    def cikis_yap(self):
        self.kullanici = None
        self.firma = None
        self.yetki_seviyesi = 1
        self.giris_ekrani()

if __name__ == "__main__":
    root = tk.Tk()
    app = StokYonetimUygulamasi(root)
    root.mainloop()