import pandas as pd
import numpy as np

# importujemy testowaną funkcję
from data_statistics import calculate_daily_exceedances


def test_calculate_daily_exceedances_simple():
    # sprawdzamy, czy funkcja calculate_daily_exceedances poprawnie liczy liczbę dni
    # z przekroczeniem normy dobowej, liczy średnie dobowe z danych godzinowych i grupuje wyniki po roku
    
    # tworzymy df do testów
    df = pd.DataFrame(
        {
            "PM25": [
                10, 20,   # dzień 1: średnia = 15 (brak przekroczenia)
                30, 40    # dzień 2: średnia = 35 (przekroczenie)
            ]
        },
        index=pd.to_datetime([
            "2024-01-01 01:00",
            "2024-01-01 12:00",
            "2024-01-02 01:00",
            "2024-01-02 12:00",
        ])
    )

    result = calculate_daily_exceedances(df)

    # W 2024 roku powinien być dokładnie 1 dzień z przekroczeniem normy
    assert result.loc[2024, "PM25"] == 1