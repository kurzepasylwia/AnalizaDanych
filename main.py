import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

plt.style.use("seaborn-v0_8")

### globalna zmienna dane

df = None

def wczytaj_plik():
    global df
    sciezka = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if sciezka:
        df = pd.read_csv(sciezka)
        label_status.config(text="✅ Plik wczytany poprawnie", fg="green")


def filtruj_dane():
    global df
    if df is None:
        label_status.config(text="❌ Najpierw wczytaj plik!", fg="red")
        return
    
    min_wiek = int(entry_wiek.get())
    przefiltrowane = df[df["wiek"] >= min_wiek]

    srednia = przefiltrowane["cisnienie"].mean()
    mediana = przefiltrowane["cisnienie"].median()
    srednie_plec = przefiltrowane.groupby("plec")["cisnienie"].mean()
    
    label_wyniki.config( 
                    text=f"Średnie ciśnienie: {srednia:.2f}\nMediana: {mediana:.2f}",
                    fg="blue")
    
    przefiltrowane.to_csv("wyniki.csv", index=False)

# Wizualizacja (wykresy obok siebie)
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    
    ### histogram
    axs[0].hist(przefiltrowane["cisnienie"], bins=10, color="#4C72B0", edgecolor="black", alpha=0.8)
    axs[0].set_title("Histogram ciśnienia")
    axs[0].grid(True, linestyle="--", alpha=0.5)

    ### wykres rozrzutu
    axs[1].scatter(przefiltrowane["wiek"], przefiltrowane["cisnienie"], color="#55A868", alpha=0.7)
    axs[1].set_xlabel("Wiek")
    axs[1].set_ylabel("Ciśnienie")
    axs[1].set_title("Wiek vs Ciśnienie")
    axs[1].grid(True, linestyle="--", alpha=0.5)

    ### wykres srednia wartosc cisnienia wzgledem plci
    axs[2].bar(srednie_plec.index, srednie_plec.values, color=["#C44E52", "#8172B3"])
    axs[2].set_title("Średnie ciśnienie wg płci")
    axs[2].set_xlabel("Płeć")
    axs[2].set_ylabel("Średnie ciśnienie")
    axs[2].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout
    manager = plt.get_current_fig_manager()
    manager.window.wm_geometry("+300+200")
    plt.show()

### GUI
root = tk.Tk()
root.title("Analiza danych medycznych")

# Wyswietlanie okna aplikacji na srodku ekranu
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
####root.rowconfigure(0, weight=1)
####root.rowconfigure(4, weight=1)

# Przycisk wczytania pliku
btn_wczytaj = tk.Button(root, text="Wczytaj plik CSV", command=wczytaj_plik)
btn_wczytaj.grid(row=1, column=0, columnspan=2, pady=10)
label_status = tk.Label(root, text="", font=("Arial", 10))
label_status.grid(row=2, column=0, columnspan=2, pady=5)


# Etykieta
label = tk.Label(root, text="Minimalny wiek:")
label.grid(row=3, column=0, columnspan=2, pady=10)

# Pole wpisywania
entry_wiek = tk.Entry(root, justify="center")
entry_wiek.grid(row=4, column=0, columnspan=2, pady=(0, 10))

# Przycisk analizy
btn_filtruj = tk.Button(root, text="Filtruj i analizuj", command=filtruj_dane)
btn_filtruj.grid(row=5, column=0, columnspan=2, pady=10)

# Wyniki srednia i mediana na dole okna
label_wyniki = tk.Label(root, text="", font=("Arial", 18))
label_wyniki.grid(row=5, column=0, columnspan=2, pady=15)

root.mainloop()