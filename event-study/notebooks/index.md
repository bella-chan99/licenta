# Ghid de lectura

Citeste materialele in ordinea asta:

1. README.md # cam asta iti zice cum sa rulezi tot in VS Code, bubulet
2. event_study_explicat_ro.ipynb
3. event_study_market_model_ro.ipynb
4. index.md

## 1. Primul notebook

Rol:

- explica exact modelul din codul actual din proiect
- construieste intuitia de baza

Ce inveti:

- cum arata datele brute
- cum treci de la preturi la randamente
- de ce media randamentelor istorice poate fi vazuta ca o regresie liniara doar cu intercept
- ce sunt `normal_returns`, `abnormal_returns`, `t-statistic` si `p-value`

Vizual:

- are grafice pentru preturi, randamente, ferestrele de estimare/eveniment, randamente anormale si CAR

## 2. Al doilea notebook

Rol:

- trece de la modelul simplu la market model-ul standard din finante

Ce inveti:

- cum se estimeaza `alpha` si `beta`
- cum intra randamentul pietei in model
- de ce predictia randamentului normal devine mai realista
- cum legi teoria de un exemplu live din Yahoo Finance

Vizual:

- are grafice pentru regresie, comparatia activ vs. piata, predictii in fereastra de eveniment si CAR

## Regula simpla

- primul notebook = fundatia
- al doilea notebook = extensia academica standard

## Cum le rulezi repede

Din folderul `event-study/`:

```bash
uv sync
```

Apoi deschizi notebook-urile in VS Code, alegi kernel-ul din `.venv` si rulezi `Run All`.
