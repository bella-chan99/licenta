# Notebook-uri

Citeste notebook-urile in ordinea asta:

1. `event_study_explicat_ro.ipynb`
2. `event_study_market_model_ro.ipynb`

## Ordinea recomandata

### 1. `event_study_explicat_ro.ipynb`

Acesta trebuie citit primul.

Explica:

- cum arata datele brute
- diferenta dintre preturi si randamente
- modelul folosit efectiv in codul actual
- de ce acel model este o regresie liniara doar cu intercept
- cum apar `normal_returns`, `abnormal_returns`, `t-test` si `p-value`

### 2. `event_study_market_model_ro.ipynb`

Acesta trebuie citit dupa primul.

Explica varianta mai academica si mai standard din literatura:

- modelul de piata `R_i = alpha + beta R_m + epsilon`
- cum se estimeaza `alpha` si `beta`
- de ce ai nevoie si de randamentul pietei, nu doar de randamentul activului
- cum se face predictia randamentului normal intr-un model mai realist
- cum se obtin randamentele anormale in aceasta versiune

## Varianta simpla: VS Code

1. Deschide folderul `event-study/` in VS Code.
2. Instaleaza extensiile `Python` si `Jupyter` daca nu sunt deja instalate.
3. Din terminalul din `event-study/`, ruleaza:

```bash
uv sync
```

4. Deschide mai intai `notebooks/event_study_explicat_ro.ipynb`.
5. Alege kernel-ul din `.venv` al proiectului.
6. Apasa `Run All`.
7. Abia dupa aceea deschide `notebooks/event_study_market_model_ro.ipynb`.
8. Ruleaza si acolo `Run All`.

Daca VS Code nu vede kernel-ul, ruleaza o singura data:

```bash
uv run python -m ipykernel install --user --name event-study
```

## Ce contine

- cum arata datele brute descarcate
- diferenta dintre preturi si randamente
- modelul din proiect, explicat ca regresie liniara doar cu intercept
- predictia randamentelor normale
- randamente anormale
- `t-test`, `p-value` si interpretarea lor
- extensia catre market model-ul standard din finante
