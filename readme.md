# Analiza danych medycznych

## Opis projektu

Aplikacja desktopowa w języku Python umożliwiająca analizę danych medycznych pacjentów zapisanych w pliku CSV.

Program pozwala na:
- wczytanie danych z pliku CSV,
- filtrowanie pacjentów według minimalnego wieku,
- obliczanie podstawowych statystyk (średnia i mediana ciśnienia),
- wizualizację danych (histogram oraz wykres rozrzutu),
- eksport przefiltrowanych danych do nowego pliku CSV.

Aplikacja została wykonana z wykorzystaniem biblioteki Tkinter (GUI), Pandas (analiza danych) oraz Matplotlib (wizualizacja).

---

## Wymagania techniczne

- Python 3.x
- pandas
- matplotlib
- tkinter (wbudowany w Python)

---

## Instalacja

1. Sklonuj repozytorium:

   git clone https://github.com/kurzepasylwia/AnalizaDanych

2. Przejdź do folderu projektu:

   cd analiza_danych_med

3. (Opcjonalnie) Utwórz środowisko wirtualne:

   python -m venv .venv

4. Aktywuj środowisko:

   Mac/Linux:
   source .venv/bin/activate

   Windows:
   .venv\Scripts\activate

5. Zainstaluj wymagane biblioteki:

   pip install pandas matplotlib

6. Uruchom aplikację:

   python main.py

---

## Struktura danych wejściowych (CSV)

Plik CSV powinien zawierać kolumny:

- wiek (int)
- plec (string)
- cisnienie (int)
- objaw (string)

Przykład:

wiek,plec,cisnienie,objaw  
34,K,120,kaszel  
50,M,140,goraczka  

---

## Jak działa aplikacja?

1. Użytkownik wybiera plik CSV przy pomocy okna dialogowego.
2. Dane są wczytywane do obiektu DataFrame (Pandas).
3. Użytkownik podaje minimalny wiek pacjentów.
4. Dane są filtrowane według warunku:

   wiek >= podana_wartosc

5. Obliczane są:
   - średnia ciśnienia
   - mediana ciśnienia

6. Wyniki są wyświetlane w oknie aplikacji, na dole.
7. Tworzony jest plik `wyniki.csv` zawierający przefiltrowane dane.
8. Generowane są trzy wykresy:
   - histogram ciśnienia
   - wykres rozrzutu (wiek vs ciśnienie)
   - średnia ciśnienia według płci

---

## Wizualizacja

- Wyniki średniej oraz mediany ciśnienia wyświetlane są w oknie pod przyciskiem analizy.
- Histogram przedstawia rozkład wartości ciśnienia w badanej grupie.
- Wykres rozrzutu pokazuje zależność między wiekiem a ciśnieniem pacjentów.
- Wykres słupkowy średniego ciśnienia według płci

Wykresy wyświetlane są w jednym panelu bez otwierania dodatkowych okien.

---

## Architektura

Projekt opiera się na architekturze zdarzeniowej:

- Tkinter odpowiada za interfejs użytkownika.
- Funkcja `wczytaj_plik()` obsługuje wczytywanie danych.
- Funkcja `filtruj_dane()` odpowiada za:
  - filtrowanie danych,
  - obliczenia statystyczne,
  - eksport danych,
  - generowanie wykresów.

Zastosowano globalną zmienną `df` do przechowywania danych wczytanych z pliku.

---

## Pliki generowane przez aplikację

- `wyniki.csv` – przefiltrowane dane po analizie.

---

## Autor

Projekt wykonany w ramach zadania z zakresu analizy danych medycznych w języku Python.

Autor: Sylwia Kurzępa