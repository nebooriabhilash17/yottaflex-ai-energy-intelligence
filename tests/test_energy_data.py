
import pandas as pd


def test_energy_calculation():
    # 20 kW for 15 minutes should consume 5 kWh
    power_kw = 20
    interval_minutes = 15

    energy_kwh = power_kw * interval_minutes / 60

    assert energy_kwh == 5


def test_energy_values_are_non_negative():
    readings = pd.DataFrame({
        "Energy_kWh": [5.0, 4.5, 3.75]
    })

    assert (readings["Energy_kWh"] >= 0).all()


def test_reading_ids_are_unique():
    readings = pd.DataFrame({
        "Reading_ID": ["ENG-001", "ENG-002", "ENG-003"]
    })

    assert readings["Reading_ID"].is_unique


def test_production_quantity_is_non_negative():
    production = pd.DataFrame({
        "Production_Quantity": [100, 0, 150]
    })

    assert (production["Production_Quantity"] >= 0).all()
