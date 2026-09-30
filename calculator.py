"""
Kalkulator Desktop
Dibuat dengan Python 3 dan Tkinter.

Fitur:
- Operasi dasar: tambah, kurang, kali, bagi
- Tambahan: persen, +/-, desimal, backspace, clear (C / AC)
- Input lewat tombol GUI maupun keyboard
- Riwayat perhitungan
- Penanganan error (mis. pembagian dengan nol)
"""

import tkinter as tk
from tkinter import messagebox


class Kalkulator:
    # Warna tema
    BG = "#1e1e2e"
    DISPLAY_BG = "#11111b"
    FG = "#cdd6f4"
    BTN_NUM = "#313244"
    BTN_OP = "#fab387"
    BTN_FUNC = "#585b70"
    BTN_EQ = "#a6e3a1"
    BTN_CLR = "#f38ba8"

    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Desktop")
        self.root.geometry("340x560")
        self.root.minsize(320, 520)
        self.root.configure(bg=self.BG)

        self.expression = ""        # ekspresi yang sedang diketik
        self.riwayat = []           # daftar riwayat
        self.baru_hasil = False     # True jika layar baru menampilkan hasil

        self.buat_display()
        self.buat_tombol()
        self.bind_keyboard()

    # ---------------------------------------------------------------- UI
    def buat_display(self):
        frame = tk.Frame(self.root, bg=self.BG)
        frame.pack(fill="x", padx=10, pady=(12, 4))

        # Label ekspresi (kecil, di atas)
        self.var_expr = tk.StringVar(value="")
        tk.Label(
            frame, textvariable=self.var_expr, anchor="e",
            bg=self.DISPLAY_BG, fg="#9399b2", font=("Helvetica", 12), padx=10,
        ).pack(fill="x")

        # Label hasil (besar)
        self.var_hasil = tk.StringVar(value="0")
        tk.Label(
            frame, textvariable=self.var_hasil, anchor="e",
            bg=self.DISPLAY_BG, fg=self.FG, font=("Helvetica", 32, "bold"),
            padx=10, pady=10,
        ).pack(fill="x")

    def buat_tombol(self):
        frame = tk.Frame(self.root, bg=self.BG)
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        # (teks, warna, perintah)
        layout = [
            [("AC", self.BTN_CLR), ("⌫", self.BTN_FUNC), ("%", self.BTN_FUNC), ("÷", self.BTN_OP)],
            [("7", self.BTN_NUM), ("8", self.BTN_NUM), ("9", self.BTN_NUM), ("×", self.BTN_OP)],
            [("4", self.BTN_NUM), ("5", self.BTN_NUM), ("6", self.BTN_NUM), ("−", self.BTN_OP)],
            [("1", self.BTN_NUM), ("2", self.BTN_NUM), ("3", self.BTN_NUM), ("+", self.BTN_OP)],
            [("±", self.BTN_FUNC), ("0", self.BTN_NUM), (".", self.BTN_NUM), ("=", self.BTN_EQ)],
        ]

        for r, baris in enumerate(layout):
            frame.rowconfigure(r, weight=1)
            for c, (teks, warna) in enumerate(baris):
                frame.columnconfigure(c, weight=1)
                fg = "#11111b" if warna in (self.BTN_OP, self.BTN_EQ, self.BTN_CLR) else self.FG
                tk.Button(
                    frame, text=teks, bg=warna, fg=fg,
                    activebackground=self.FG, font=("Helvetica", 18, "bold"),
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda t=teks: self.tekan(t),
                ).grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Tombol riwayat
        tk.Button(
            self.root, text="Lihat Riwayat", bg=self.BTN_FUNC, fg=self.FG,
            relief="flat", cursor="hand2", command=self.tampil_riwayat,
        ).pack(fill="x", padx=13, pady=(0, 12))

    def bind_keyboard(self):
        self.root.bind("<Key>", self.on_key)
        self.root.bind("<Return>", lambda e: self.tekan("="))
        self.root.bind("<KP_Enter>", lambda e: self.tekan("="))
        self.root.bind("<BackSpace>", lambda e: self.tekan("⌫"))
        self.root.bind("<Escape>", lambda e: self.tekan("AC"))

    def on_key(self, event):
        peta = {"*": "×", "/": "÷", "-": "−"}
        ch = event.char
        if ch in "0123456789.+%":
            self.tekan(ch)
        elif ch in peta:
            self.tekan(peta[ch])

    # ------------------------------------------------------------- Logika
    def tekan(self, tombol):
        if tombol == "AC":
            self.expression = ""
            self.var_expr.set("")
            self.var_hasil.set("0")
            self.baru_hasil = False
        elif tombol == "⌫":
            self.expression = self.expression[:-1]
            self.update_layar()
        elif tombol == "=":
            self.hitung()
        elif tombol == "±":
            self.ganti_tanda()
        elif tombol == "%":
            self.persen()
        elif tombol in "+−×÷":
            self.tambah_operator(tombol)
        elif tombol == ".":
            self.tambah_desimal()
        else:  # angka
            if self.baru_hasil:
                self.expression = ""
                self.baru_hasil = False
            self.expression += tombol
            self.update_layar()

    def tambah_operator(self, op):
        self.baru_hasil = False
        if not self.expression:
            if op == "−":           # izinkan angka negatif di awal
                self.expression = "−"
                self.update_layar()
            return
        if self.expression[-1] in "+−×÷":
            self.expression = self.expression[:-1] + op   # ganti operator
        else:
            self.expression += op
        self.update_layar()

    def tambah_desimal(self):
        if self.baru_hasil:
            self.expression = ""
            self.baru_hasil = False
        # ambil angka terakhir
        angka = self.expression
        for op in "+−×÷":
            angka = angka.split(op)[-1]
        if "." in angka:
            return
        if angka == "":
            self.expression += "0"
        self.expression += "."
        self.update_layar()

    def ganti_tanda(self):
        if not self.expression:
            return
        # cari posisi awal angka terakhir
        idx = max(self.expression.rfind(op) for op in "+−×÷")
        if idx == -1:
            angka, awal = self.expression, ""
        else:
            angka, awal = self.expression[idx + 1:], self.expression[:idx + 1]
        if awal.endswith("−") and (len(awal) == 1 or awal[-2] in "+−×÷"):
            awal = awal[:-1]      # buang tanda negatif -> jadi positif
        elif awal == "" or awal[-1] in "+×÷":
            awal = awal[:-1] + "−" if awal.endswith("+") else awal + "−"
        else:
            awal = awal[:-1] + "+"
        self.expression = awal + angka
        self.update_layar()

    def persen(self):
        try:
            nilai = self.evaluasi(self.expression)
            self.expression = self.format_angka(nilai / 100)
            self.update_layar()
        except Exception:
            self.tampil_error("Ekspresi tidak valid")

    def evaluasi(self, teks):
        """Ubah simbol tampilan ke operator Python lalu hitung dengan aman."""
        ekspresi = teks.replace("×", "*").replace("÷", "/").replace("−", "-")
        # hanya izinkan karakter aman
        if not all(ch in "0123456789.+-*/() " for ch in ekspresi):
            raise ValueError("Karakter tidak valid")
        return eval(ekspresi, {"__builtins__": {}}, {})

    def hitung(self):
        if not self.expression:
            return
        # buang operator di akhir (mis. "5+")
        ekspresi = self.expression
        while ekspresi and ekspresi[-1] in "+−×÷":
            ekspresi = ekspresi[:-1]
        if not ekspresi:
            return
        try:
            hasil = self.evaluasi(ekspresi)
            teks_hasil = self.format_angka(hasil)
            self.riwayat.append(f"{ekspresi} = {teks_hasil}")
            self.var_expr.set(ekspresi + " =")
            self.var_hasil.set(teks_hasil)
            self.expression = teks_hasil
            self.baru_hasil = True
        except ZeroDivisionError:
            self.tampil_error("Tidak bisa dibagi nol")
        except Exception:
            self.tampil_error("Ekspresi tidak valid")

    @staticmethod
    def format_angka(nilai):
        if isinstance(nilai, float):
            nilai = round(nilai, 10)
            if nilai == int(nilai):
                return str(int(nilai))
        return str(nilai)

    def update_layar(self):
        self.var_expr.set("")
        self.var_hasil.set(self.expression if self.expression else "0")

    def tampil_error(self, pesan):
        self.var_expr.set("")
        self.var_hasil.set("Error")
        self.expression = ""
        self.baru_hasil = False
        messagebox.showerror("Kesalahan", pesan)
        self.var_hasil.set("0")

    def tampil_riwayat(self):
        if not self.riwayat:
            messagebox.showinfo("Riwayat", "Belum ada perhitungan.")
        else:
            messagebox.showinfo("Riwayat (10 terakhir)", "\n".join(self.riwayat[-10:]))


if __name__ == "__main__":
    root = tk.Tk()
    Kalkulator(root)
    root.mainloop()
