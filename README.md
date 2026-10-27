# YottaFlex AI — Industrial Energy Monitoring and Waste Detection



## Project Overview



YottaFlex AI is a data analytics project designed to analyze industrial electricity consumption, identify unusual energy usage patterns, and prioritize machines for further investigation. It combines synthetic energy readings, production data, electricity tariffs, and machine-level analysis to generate actionable reports.



**Note:** This project currently uses synthetic data and is a prototype, not a production-connected industrial monitoring system.



## Objectives



\- Analyze electricity consumption across industrial machines.

\- Detect unusual energy consumption patterns.

\- Link energy readings with production batches.

\- Estimate electricity costs using time-based tariffs.

\- Identify machines that may require operational investigation.

\- Generate reports and visualizations to support energy-efficiency decisions.



## Technology Stack



\- Python

\- Pandas

\- NumPy

\- Pytest

\- Power BI

\- Git and GitHub



## Project Structure



```text

energy-intelligence/

â”œâ”€â”€ data/

â”‚   â”œâ”€â”€ raw/

â”‚   â”œâ”€â”€ processed/

â”‚   â””â”€â”€ ground\_truth/

â”œâ”€â”€ docs/

â”‚   â”œâ”€â”€ architecture.md

â”‚   â”œâ”€â”€ data\_dictionary.md

â”‚   â””â”€â”€ run\_guide.md

â”œâ”€â”€ src/

â”‚   â”œâ”€â”€ data generation scripts

â”‚   â”œâ”€â”€ energy analysis scripts

â”‚   â”œâ”€â”€ anomaly detection scripts

â”‚   â”œâ”€â”€ cost analysis scripts

â”‚   â””â”€â”€ validation scripts

â”œâ”€â”€ tests/

â”œâ”€â”€ generate.py

â”œâ”€â”€ first\_checksums.csv

â”œâ”€â”€ YottaFlex\_AI\_Dashboard.pbix

â”œâ”€â”€ .gitignore

â””â”€â”€ README.md

```



## Dataset Overview



The project dataset contains synthetic records representing:



\- 1 industrial plant

\- 20 machines

\- 90 days of energy readings

\- 172,800 energy readings collected at 15-minute intervals

\- 3,218 production batches

\- Time-based electricity tariff periods



The data is intended for development, testing, and demonstration.



## Key Results



| Metric | Result |

|---|---:|

| Energy readings analyzed | 172,800 |

| Production batches analyzed | 3,218 |

| Batches flagged for investigation | 186 |

| Days flagged for unusual energy patterns | 6 |

| Machines classified as high energy intensity | 5 |

| Total modeled electricity cost | â‚¹3,543,808.88 |

| Estimated cost associated with flagged batches at â‚¹7/kWh | â‚¹140,866.46 |



These are results from the synthetic dataset. The estimated cost associated with flagged batches is not confirmed avoidable waste or guaranteed savings.



## Main Features



### Energy Analysis

Summarizes energy consumption across machines and reporting periods.



### Anomaly Detection

Flags unusual energy consumption patterns and production batches for further investigation.



### Production-Energy Analysis

Matches energy readings with production batches to support energy-intensity analysis.



### Tariff-Based Cost Analysis

Calculates modeled electricity costs using time-based tariff rates.



### Machine Prioritization

Ranks machines using analysis results to help determine which machines should be investigated first.



### Reporting and Dashboard

Exports analytical results to CSV reports and includes a Power BI dashboard for visualization.



## Installation



Clone the repository and navigate to the project directory:



```powershell

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd energy-intelligence

```



Create a virtual environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install the required packages:



```powershell

python -m pip install pandas numpy pytest

```



## Running the Project



Run the main machine and meter data generator:



```powershell

python .\\generate.py

```



This script generates plant, meter, and machine data. Other scripts in `src/` generate or analyze additional datasets and reports. Refer to `docs/run\_guide.md` for the intended execution order.



## Running Tests



Run the automated tests:



```powershell

python -m pytest .\\tests -v

```



## Documentation



\- `docs/architecture.md` — project architecture and components.

\- `docs/data\_dictionary.md` — dataset fields and definitions.

\- `docs/run\_guide.md` — instructions for running the project.



## Limitations



\- The current dataset is synthetic and does not represent actual factory telemetry.

\- Anomaly flags identify records for investigation; they do not prove equipment faults or energy waste.

\- Cost estimates depend on the assumed tariff rates and modeled consumption.

\- Estimated costs associated with flagged batches are not verified savings.

\- The project has not yet demonstrated real-time monitoring on industrial equipment.



## Future Enhancements



\- Integrate real-time energy meter data.

\- Develop machine-learning-based anomaly detection.

\- Add live monitoring and alert notifications.

\- Compare energy consumption against production output.

\- Validate results using real industrial operating data.

\- Develop more detailed energy-efficiency recommendations.



## Project Status



**Prototype — synthetic-data analytics and reporting.**



This project demonstrates data generation, data processing, energy analysis, anomaly screening, cost estimation, testing, and dashboard reporting.




