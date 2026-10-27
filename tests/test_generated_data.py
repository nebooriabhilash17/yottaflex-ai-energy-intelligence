
import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data/raw")


def test_energy_file_exists():
    assert (DATA_FOLDER / "energy_readings.csv").exists()


def test_meter_file_exists():
    assert (DATA_FOLDER / "meters.csv").exists()


def test_energy_data_has_no_missing_values():
    energy = pd.read_csv(DATA_FOLDER / "energy_readings.csv")

    required_columns = [
        "Reading_ID",
        "Meter_ID",
        "Timestamp",
        "Average_Power_kW",
        "Energy_kWh"
    ]

    assert energy[required_columns].notna().all().all()


def test_reading_ids_are_unique():
    energy = pd.read_csv(DATA_FOLDER / "energy_readings.csv")

    assert energy["Reading_ID"].is_unique


def test_all_readings_reference_existing_meters():
    energy = pd.read_csv(DATA_FOLDER / "energy_readings.csv")
    meters = pd.read_csv(DATA_FOLDER / "meters.csv")

    assert energy["Meter_ID"].isin(meters["Meter_ID"]).all()


def test_energy_matches_average_power():
    energy = pd.read_csv(DATA_FOLDER / "energy_readings.csv")

    expected = energy["Average_Power_kW"] * 15 / 60

    difference = (energy["Energy_kWh"] - expected).abs()

    assert (difference <= 0.0011).all()


def test_energy_values_are_non_negative():
    energy = pd.read_csv(DATA_FOLDER / "energy_readings.csv")

    assert (energy["Energy_kWh"] >= 0).all()
