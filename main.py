import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

### globalna zmienna dane

df = None

def wczytaj_plik():
    global df
    sciezka = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if sciezka:
        df = pd.read_csv(sciezka)
        messagebox.showinfo("Sukces", "Plik wczytany poprawnie")

def filtruj_dane():
    global df
    if df is None:
        messagebox.showerror("Błąd", "Najpierw wczytaj plik")
        return
    
    min_wiek = int(entry_wiek.get())
    przefiltrowane = df[df["wiek"] >= min_wiek]

    srednia = przefiltrowane["cisnienie"].mean()
    mediana = przefiltrowane["cisnienie"].median()
    
    messagebox.showinfo("Statystyki", 
                        f"Średnie ciśnienie: {srednia:.2f}\nMediana: {mediana:.2f}")
    
    przefiltrowane.to_csv("wyniki.csv", index=False)

    ### histogram
    fig1 = plt.figure()
    plt.hist(przefiltrowane["cisnienie"])
    plt.title("Histogram ciśnienia")

    ### wykres rozrzutu
    fig2 = plt.figure()
    plt.scatter(przefiltrowane["wiek"], przefiltrowane["cisnienie"])
    plt.xlabel("Wiek")
    plt.ylabel("Ciśnienie")
    plt.title("Wiek vs Ciśnienie")
    
    plt.show()

### GUI
root = tk.Tk()
root.title("Analiza danych medycznych")

# Wyswietlanie okna na srodku ekranu
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{
center_y}')

# Konfiguracja siatki - przy zmianie rozmiaru obiekty centrowane
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(4, weight=1)

# Przycisk wczytania pliku
btn_wczytaj = tk.Button(root, text="Wczytaj CSV", command=wczytaj_plik)
btn_wczytaj.grid(row=1, column=0, columnspan=2, pady=10)

# Etykieta
label = tk.Label(root, text="Minimalny wiek:")
label.grid(row=2, column=0, columnspan=2, pady=10)

# Pole wpisywania
entry_wiek = tk.Entry(root)
entry_wiek.grid(row=3, column=0, columnspan=2, pady=10)

# Przycisk analizy
btn_filtruj = tk.Button(root, text="Filtruj i analizuj", command=filtruj_dane)
btn_filtruj.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
