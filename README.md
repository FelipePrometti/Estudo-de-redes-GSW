# Golden State Warriors Pass Network Analysis (2017–18)

This project analyzes the Golden State Warriors passing network using real play-by-play data.
Each player is a node and each directed edge (A->B) is an assist from A to B.
The goal is to understand ball movement and roles through network metrics.

---
## Overview

The repository contains code and data to:
- Collect play-by-play data from ESPN.
- Extract assistant->finisher pairs and build directed weighted graphs.
- Compute metrics (in-degree, out-degree, centrality).
- Generate tables, CSVs and optional figures for games or the full set.

---
## Setup and Execution

### Run on Google Colab (recommended)
1) Open the notebook (e.g., analysis.ipynb or main.ipynb).
2) Upload or mount the dados/ folder if needed.
3) Run all cells to generate results (tables, CSVs, metrics).

### Run Locally
```bash
git clone https://github.com/FelipePrometti/Estudo-de-redes-GSW.git
cd Estudo-de-redes-GSW
pip install -r requirements.txt
python src/analyze_network.py
```

---
## Data Description

The dataset contains 10 regular-season games from the 2017–18 season.
Plays include events like:
[Player X] makes [shot type] (assist by [Player Y])
From these, assistant->finisher pairs are extracted to form a weighted directed graph.

---
## Tools and Libraries

- Python 3.10+
- pandas (data manipulation)
- networkx (network analysis)
- matplotlib (visualization)
- python-docx (optional: report generation)

---
## Results Summary

- Total assists analyzed: approx 200
- Unique pass connections: approx 90
- Distinct players involved: approx 12
- Games analyzed: 10

Key patterns: Draymond Green as main creator; Klay Thompson as key finisher;
bench unit forms a secondary module (e.g., Livingston, West, Looney, Young).

---
## Authors

Felipe Prometti
Federal University of ABC (UFABC), Santo Andre, Brazil
Email: felipe.prometti@ufabc.edu.br
Developed for the Communication and Networks (2025/3) course.

---
## Repository Link

https://github.com/FelipePrometti/Estudo-de-redes-GSW
