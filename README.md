# E20 Policy: Implementation or Execution Blunder?

Data, code and survey materials for a research paper on India's Ethanol Blended Petrol (EBP) programme. The paper asks whether public friction over E20 petrol comes from policy design flaws or from execution shortcomings.

## Repository Contents

- **data/**:Vahan vehicle registration CSVs (2006–2026).
- **analysis/**:Python scripts that clean and summarise the CSVs
- **survey/**:Survey questionnaire (PDF) and anonymised responses (n = 2)

## Data Files


| File | Contents |
|---|---|
| All Fuel Vehicles (two wheelers only).csv | Two-wheelers, all fuel types, active, 2006–2026 |
| All fuel types (3 wheelers only).csv | Three-wheelers, all fuel types, active, 2006–2026 |
| All Fuel Types (only active 4 wheelers).csv | Four-wheelers, all fuel types, active, 2006–2026 |


## Vahan Extraction Settings

- **Source**: Vahan dashboard   (https://vahan.parivahan.gov.in/), pulled on 29 September 2026
- **Status**: active (compliant and non-compliant)
- **Years**: calendar years 2006–2026
- **State**: all
- **Vehicle type**: [Transport / Non-Transport / both, for each of 2W, 3W, 4W]
- **Category**: Two Wheeler, Three Wheeler, Four Wheeler, pulled separately
- **Fuel**: all fuel types (petrol variants identified during analysis)


## How to Run

Python, with pandas

python analysis/Hypothesis_2 E20 Paper.py


The script prints fuel-type counts and shares for each vehicle class and for 2018–2021 versus 2022–2025.

## Sources

-Vahan, Ministry of Road Transport and Highways: https://vahan.parivahan.gov.in/

## Limitations

-Vahan counts are by calendar year, not fiscal year.
-Fuel labels do not establish E20 compatibility, and compliance cohorts were not computed.
-The survey (n = 2) is exploratory and not generalisable.

## Author

Jatin Chandel
