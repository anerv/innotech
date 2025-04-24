# Dokumentation

## Installation

Kræver en installation af Python, Jupyter, Conda og pip. For at installere det nødvendige Conda Python-environment køres nedenstående i terminalen:

**Klon GitHub repository**

````bash
git clone -b main --single-branch https://github.com/anerv/innotech-data-processing --depth 1
````

**Skab Conda environment**
```bash
conda create -n innotech --strict-channel-priority geopandas pyyaml pyarrow overpy contextily h3-py ipykernel
```

**Aktiver Conda environment og installer sidste elementer**
````bash
conda activate innotech
pip install matplotlib-scalebar
pip install -e .
````

## Inputdata

- Adresse-data (adresser og adgangsadresser fra DAWI) for den ønskede region.
- CVR-data (Penheder) for den ønskede region.
- Afgrænsning af studieområdet (INPSPIRE data med danske administrative områder. Opdater config.yml andet område end Region Sjælland ønskes.). 

Se config.yml for forventede filnavne og placeringer.

## Anvendelse

Kør alle Python-scripts i mappen `scripts` i nummereret rækkefølge. Resultater eksporteres automatisk til mappen `results`.



