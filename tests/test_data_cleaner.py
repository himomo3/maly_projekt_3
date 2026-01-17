import pandas as pd
import numpy as np



# importujemy funkcje które chcemy testować 
from data_cleaner import (
    normalize_dataframe,
    filter_common_stations,
    combine_dataframes,
    fix_midnight_dates
)


def test_normalize_dataframe_basic():
    # ten test sprawdza, czy funkcja normalize_dataframe 

    # tworzymy dataframe do testow
    df = pd.DataFrame({
        "A": ["1,5", "2,5"],
        "B": ["tekst", "3,0"]
    })

    cleaned, changes = normalize_dataframe(df)

    # tutaj sprawdzamy czy przecinek został poprawnie zamieniony na kropkę
    assert cleaned.loc[0, "A"] == 1.5
    assert cleaned.loc[1, "A"] == 2.5

    # sprawdzamy czy tekst pozostał bez zmian
    assert cleaned.loc[0, "B"] == "tekst"


    assert cleaned.loc[1, "B"] == 3.0

    # sprawdzamy, czy funkcja rzeczywiście coś zmieniła
    assert changes > 0


def test_filter_common_stations():
    # w tym miejscu sprawdzamy, czy funkcja filter_common_stations pozostawia tylko te stacje, które
    # występują we wszystkich latach i czy usuwa kolumny unikalne dla pojedynczych lat

    df1 = pd.DataFrame(columns=["S1", "S2", "S3"])
    df2 = pd.DataFrame(columns=["S2", "S3", "S4"])

    data = {
        2015: df1,
        2024: df2
    }

    result = filter_common_stations(data)

    # wspólne stacje tylko dla S2 i S3
    assert list(result[2015].columns) == ["S2", "S3"]
    assert list(result[2024].columns) == ["S2", "S3"]


def test_combine_dataframes():
    # sprawdzamy, czy funkcja combine_dataframes łączy dane z róznych lat w jeden dataframe,
    # czy zachowuje indeks typu datetime i czy sortuje dane chronologicznie

    df1 = pd.DataFrame(
        {"A": [1, 2]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02"])
    )
    df2 = pd.DataFrame(
        {"A": [3]},
        index=pd.to_datetime(["2025-01-01"])
    )

    combined = combine_dataframes({2024: df1, 2025: df2})

    # sprawdzamy liczbę wierszy
    assert combined.shape[0] == 3
    # sprawdzamy pierwszą wartość (czy jest chronologicznie)
    assert combined.iloc[0]["A"] == 1
    # sprawdzamy czy indeks jest posortowany rosnąco
    assert combined.index.is_monotonic_increasing


def test_fix_midnight_dates():
    # ten test sprawdza korektę dat, czyli czy godzina 00:00:00 została przypisana do dnia poprzedniego
    # i czy czas zostaje usunięty i zostaje sama data

    df = pd.DataFrame(
        {"A": [10, 20]},
        index=pd.to_datetime([
            "2024-01-02 00:00:00",
            "2024-01-02 01:00:00"
        ])
    )

    fixed, = fix_midnight_dates(df)[:1] if isinstance(fix_midnight_dates(df), tuple) else (fix_midnight_dates(df),)

    # dzień poprzedni
    assert fixed.index[0] == pd.to_datetime("2024-01-01").date()
    # usunięty czas
    assert fixed.index[1] == pd.to_datetime("2024-01-02").date()
