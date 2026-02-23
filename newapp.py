import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog

plt.style.use("seaborn-v0_8")

# GLOBALNA ZMIENNA
df = None

# FUNKCJA WCZYTANIA PLIKU
def wczytaj_plik():
    global df
    sciezka = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if sciezka:
        df = pd.read_csv(sciezka)
        label_status.config(text="✅ Plik wczytany poprawnie", fg="#27ae60")


# FUNKCJA ANALIZY
def filtruj_dane():
    global df

    if df is None:
        label_status.config(text="❌ Najpierw wczytaj plik!", fg="red")
        return

    if entry_wiek.get() == "":
        label_status.config(text="❌ Wpisz minimalny wiek!", fg="red")
        return

    min_wiek = int(entry_wiek.get())
    przefiltrowane = df[df["wiek"] >= min_wiek]

    if przefiltrowane.empty:
        label_status.config(text="❌ Brak danych dla podanego wieku", fg="red")
        return

    # STATYSTYKI 
    srednia = przefiltrowane["cisnienie"].mean()
    mediana = przefiltrowane["cisnienie"].median()
    srednie_plec = przefiltrowane.groupby("plec")["cisnienie"].mean()

    # Kolor zależny od poziomu
    if srednia < 120:
        kolor = "#27ae60"
        status = "Norma"
    elif srednia < 140:
        kolor = "#f39c12"
        status = "Podwyższone"
    else:
        kolor = "#e74c3c"
        status = "Wysokie"

    label_wyniki.config(
        text=f"Średnia: {srednia:.2f}   |   Mediana: {mediana:.2f}\nStatus: {status}",
        fg=kolor
    )

    # USUŃ STARE WYKRESY 
    for widget in frame_wykresy.winfo_children():
        widget.destroy()

    # TWORZENIE FIGURY 
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    fig.patch.set_facecolor("#ffffff")

    # Histogram
    axs[0].hist(przefiltrowane["cisnienie"], bins=10,
                color="#4C72B0", edgecolor="black")
    axs[0].set_title("Histogram ciśnienia")
    axs[0].grid(True, alpha=0.3)

    # Wykres punktowy
    axs[1].scatter(przefiltrowane["wiek"],
                   przefiltrowane["cisnienie"],
                   color="#55A868")
    axs[1].set_title("Wiek vs Ciśnienie")
    axs[1].set_xlabel("Wiek")
    axs[1].set_ylabel("Ciśnienie")
    axs[1].grid(True, alpha=0.3)

    # Średnia wg płci
    axs[2].bar(srednie_plec.index,
               srednie_plec.values,
               color=["#C44E52", "#8172B3"])
    axs[2].set_title("Średnie wg płci")
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()

    # OSADZENIE W TKINTER 
    canvas = FigureCanvasTkAgg(fig, master=frame_wykresy)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)



### GUI

root = tk.Tk()
root.title("System analizy danych medycznych")
root.configure(bg="#ecf0f1")

# Rozmiar i wyśrodkowanie
root.geometry("1100x700")


# NAGŁÓWEK

header = tk.Label(
    root,
    text="System analizy danych medycznych",
    font=("Arial", 18, "bold"),
    bg="#2C3E50",
    fg="white",
    pady=15
)
header.pack(fill="x")


# PANEL FORMULARZA

frame_form = tk.Frame(root, bg="#ecf0f1")
frame_form.pack(pady=20)

btn_wczytaj = tk.Button(
    frame_form,
    text="Wczytaj plik CSV",
    command=wczytaj_plik,
    bg="#3498db",
    fg="white",
    relief="flat",
    padx=15,
    pady=8
)
btn_wczytaj.grid(row=0, column=0, padx=10)

entry_wiek = tk.Entry(
    frame_form,
    justify="center",
    width=10
)
entry_wiek.grid(row=0, column=1, padx=10)

btn_filtruj = tk.Button(
    frame_form,
    text="Filtruj i analizuj",
    command=filtruj_dane,
    bg="#2ecc71",
    fg="white",
    relief="flat",
    padx=15,
    pady=8
)
btn_filtruj.grid(row=0, column=2, padx=10)

label_status = tk.Label(root, text="", bg="#ecf0f1")
label_status.pack()

# PANEL STATYSTYK

panel_statystyki = tk.Frame(root, bg="white", bd=1, relief="solid")
panel_statystyki.pack(pady=15, padx=50, fill="x")

label_tytul = tk.Label(
    panel_statystyki,
    text="Panel statystyk",
    font=("Arial", 14, "bold"),
    bg="white"
)
label_tytul.pack(pady=5)

label_wyniki = tk.Label(
    panel_statystyki,
    text="",
    font=("Arial", 12),
    bg="white"
)
label_wyniki.pack(pady=10)


# PANEL WYKRESÓW

frame_wykresy = tk.Frame(root, bg="#ecf0f1")
frame_wykresy.pack(fill="both", expand=True, padx=40, pady=20)

root.mainloop()