# Dokumentation

## Installation

Projektet kræver en installation af Python, Jupyter, Conda og pip. For at installere det nødvendige Conda Python-environment køres nedenstående i et terminalvindue:

**Klon GitHub repository**

````bash
git clone -b main --single-branch https://github.com/anerv/innotech --depth 1
````

**Skab Conda environment**
```bash
conda create -n innotech --strict-channel-priority geopandas pyyaml pyarrow overpy contextily sklearn h3-py ipykernel
```

**Aktiver Conda environment og installer sidste elementer**
````bash
conda activate innotech
pip install matplotlib-scalebar
pip install -e .
pip install duckdb
conda install conda-forge::osmium-tool
````

````bash
winget install DuckDB.cli
````

## Inputdata

- Adresse-data fra DAR (adresser, husnumre, og adganspunkter) for den ønskede region.
- BBR-data (enheder) for den ønskede region.
- CVR-data (produktionsenheder, CVR-enheder med brancher, og CVR-enheder med adresser) for den ønskede region.
- Afgrænsning af studieområdet (data med danske administrative områder (regioner eller kommuner). Opdater config.yml hvis et andet område end Region Sjælland ønskes.). 

Alle data kan downloades fra Datafordeleren.

Se config.yml for forventede filnavne og placeringer.

## Anvendelse

Kør alle Python-scripts i mappen `scripts` i nummereret rækkefølge. Resultater eksporteres automatisk til mappen `results`.


