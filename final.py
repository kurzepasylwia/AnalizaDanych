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
    # TWORZENIE FIGURY 
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    fig.patch.set_facecolor("#f8f9fa")

# Wspólny styl dla wszystkich osi
    for ax in axs:
        ax.set_facecolor("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#cccccc")
        ax.spines["bottom"].set_color("#cccccc")
        ax.tick_params(colors="#555555", labelsize=9)
        ax.grid(True, axis="y", alpha=0.4, linestyle="--", color="#dddddd")

# --- Histogram wg płci ---
        plcie = przefiltrowane["plec"].unique()
    kolory_hist = {"K": "#e05c5c", "M": "#4a7dc4"}
    for plec in plcie:
        dane_plec = przefiltrowane[przefiltrowane["plec"] == plec]["cisnienie"]
        axs[0].hist(dane_plec, bins=10, alpha=0.7,
                    color=kolory_hist.get(plec, "#999999"),
                    edgecolor="white", linewidth=0.8,
                    label=f"Płeć {plec}")

    axs[0].set_title("Histogram ciśnienia wg płci",
                    fontsize=11, fontweight="bold", color="#333333", pad=10)
    axs[0].set_xlabel("Ciśnienie", color="#555555")
    axs[0].set_ylabel("Liczba osób", color="#555555")
    axs[0].legend(fontsize=9, framealpha=0.5)

# --- Wykres rozrzutu ---
    kolory_scatter = {"K": "#e05c5c", "M": "#4a7dc4"}
    for plec in plcie:
        dane_plec = przefiltrowane[przefiltrowane["plec"] == plec]
        axs[1].scatter(dane_plec["wiek"], dane_plec["cisnienie"],
                    color=kolory_scatter.get(plec, "#999999"),
                    alpha=0.7, s=45, edgecolors="white", linewidths=0.5,
                    label=f"Płeć {plec}")

    axs[1].set_title("Wiek vs Ciśnienie",
                    fontsize=11, fontweight="bold", color="#333333", pad=10)
    axs[1].set_xlabel("Wiek", color="#555555")
    axs[1].set_ylabel("Ciśnienie", color="#555555")
    axs[1].legend(fontsize=9, framealpha=0.5)
    axs[1].grid(True, alpha=0.3, linestyle="--", color="#dddddd")

# --- Słupki — średnia wg płci z błędem standardowym ---
    srednie = przefiltrowane.groupby("plec")["cisnienie"].mean()
    odch = przefiltrowane.groupby("plec")["cisnienie"].std()
    kolory_bar = [kolory_hist.get(p, "#999999") for p in srednie.index]

    bars = axs[2].bar(
        srednie.index, srednie.values,
        color=kolory_bar, edgecolor="white",
        linewidth=1, width=0.5,
        yerr=odch.values, capsize=5,
        error_kw={"ecolor": "#555555", "elinewidth": 1.5}
    )

# Etykiety wartości na słupkach
    for bar, val in zip(bars, srednie.values):
        axs[2].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + odch.values.max() + 0.5,
            f"{val:.1f}",
            ha="center", va="bottom",
            fontsize=9, color="#333333", fontweight="bold"
        )

    axs[2].set_title("Średnie ciśnienie wg płci",
                    fontsize=11, fontweight="bold", color="#333333", pad=10)
    axs[2].set_ylabel("Średnie ciśnienie", color="#555555")
    axs[2].set_ylim(bottom=max(0, srednie.values.min() - 20))

    plt.tight_layout(pad=2.0)

# OSADZENIE W TKINTER 
    canvas = FigureCanvasTkAgg(fig, master=frame_wykresy)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# GUI

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

# Etykieta nad polem wieku
label_wiek = tk.Label(
    frame_form,
    text="Minimalny wiek:",
    font=("Arial", 9),
    bg="#ecf0f1",
    fg="#333333"
)
label_wiek.grid(row=0, column=1, padx=10)

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
btn_wczytaj.grid(row=1, column=0, padx=10)

entry_wiek = tk.Entry(
    frame_form,
    justify="center",
    width=10
)
entry_wiek.grid(row=1, column=1, padx=10)

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
btn_filtruj.grid(row=1, column=2, padx=10)

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