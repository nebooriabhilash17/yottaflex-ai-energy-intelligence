\# YottaFlex AI — Data Dictionary



\## 1. Overview



This document describes the datasets used in the YottaFlex AI industrial energy monitoring and waste detection project.



The project uses synthetic data representing one industrial plant with 20 machines over 90 days. Energy readings are generated at 15-minute intervals.



\## 2. Raw Data Files



\### 2.1 plants.csv



Stores information about industrial plants.



| Column | Description |

|---|---|

| Plant\_ID | Unique identifier for a plant |

| Plant\_Name | Name assigned to the plant |

| Location | Plant location, if provided |

| Other columns | Refer to the actual CSV header |



\### 2.2 machines.csv



Stores machine information.



| Column | Description |

|---|---|

| Machine\_ID | Unique machine identifier, such as MAC-001 |

| Plant\_ID | Plant associated with the machine |

| Other columns | Refer to the actual CSV header |



\### 2.3 meters.csv



Maps energy meters to machines.



| Column | Description |

|---|---|

| Meter\_ID | Unique energy meter identifier |

| Plant\_ID | Plant associated with the meter |

| Machine\_ID | Machine measured by the meter |

| Unit | Energy measurement unit, such as kWh |

| Sampling\_Minutes | Sampling interval in minutes |



\### 2.4 energy\_readings.csv



Contains time-stamped energy readings.



| Column | Description |

|---|---|

| Reading\_ID | Unique identifier for an energy reading |

| Meter\_ID | Meter that produced the reading |

| Timestamp | Date and time of the reading |

| Energy\_kWh | Energy consumed during the sampling interval |

| Other columns | Refer to the actual CSV header |



\### 2.5 production\_batches.csv



Contains production batch information.



| Column | Description |

|---|---|

| Batch\_ID | Unique production batch identifier |

| Machine\_ID | Machine used for production |

| Start\_Time | Batch start time |

| End\_Time | Batch end time |

| Quantity\_Produced | Production quantity, if present |

| Other columns | Refer to the actual CSV header |



\### 2.6 tariffs.csv



Defines electricity prices by time period.



| Column | Description |

|---|---|

| Tariff\_ID | Unique tariff identifier |

| Plant\_ID | Plant to which the tariff applies |

| Period | Tariff period, such as OFF\_PEAK, NORMAL, or PEAK |

| Start\_Hour | Starting hour of the tariff period |

| End\_Hour | Ending hour of the tariff period |

| Price\_Per\_kWh | Electricity price per kWh in rupees |



The analysis uses the interval from Start\_Hour inclusive to End\_Hour exclusive.



\### 2.7 weather\_observations.csv



Contains synthetic weather observations used for weather-energy analysis.



The exact column names and units should be confirmed from the CSV header.



\### 2.8 energy\_anomaly\_test.csv



Contains test records used to evaluate anomaly detection.



\### 2.9 energy\_anomaly\_ground\_truth.csv



Contains reference labels for evaluating the anomaly detector.



\## 3. Processed Data Files



| File | Purpose |

|---|---|

| production\_energy\_analysis.csv | Connects production batches with energy consumption |

| tariff\_cost\_analysis.csv | Summarizes energy and electricity costs by meter and tariff |

| machine\_tariff\_costs.csv | Summarizes tariff-based electricity costs by machine |

| machine\_efficiency.csv | Summarizes energy consumption relative to production |

| batch\_anomaly\_results.csv | Flags production batches for investigation |

| daily\_anomaly\_results.csv | Identifies unusual daily energy consumption |

| machine\_priority\_report.csv | Ranks machines for investigation |

| machine\_priority\_with\_tariffs.csv | Combines priority metrics and machine tariff costs |

| energy\_saving\_recommendations.csv | Provides suggested energy-saving investigations |

| integrated\_yottaflex\_report.csv | Combines major machine, efficiency, anomaly, and cost metrics |

| yottaflex\_executive\_summary.txt | Summarizes key project results |



\## 4. Important Metrics



| Metric | Meaning |

|---|---|

| Total\_Energy\_kWh | Total energy consumption in kilowatt-hours |

| Total\_Electricity\_Cost\_Rs | Electricity cost calculated using the configured tariff schedule |

| Energy\_Per\_Unit\_kWh | Energy consumed per unit of production |

| Flagged\_Batch\_Count | Number of batches flagged for investigation |

| Daily\_Anomaly\_Days | Number of unusual consumption days detected |

| Cost\_Rank | Machine ranking based on total tariff-based electricity cost |

| Priority\_Rank | Machine investigation priority ranking |



\## 5. Units and Interpretation



\- Energy is measured in kilowatt-hours (kWh).

\- Electricity costs are expressed in Indian rupees (Rs).

\- Sampling intervals are measured in minutes.

\- Timestamps should be interpreted according to the time-zone handling used by each analysis script.

\- Tariff costs are based on the synthetic tariff schedule.



\## 6. Limitations



\- The datasets are synthetic and do not represent verified industrial measurements.

\- Anomaly flags identify unusual patterns and do not prove energy waste.

\- Electricity cost is not the same as avoidable waste cost.

\- Estimated savings require further validation against machine operating conditions and production requirements.

\- Column descriptions should be checked against the actual CSV headers before treating this document as a final schema specification.



