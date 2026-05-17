# Notebook-uri

Notebook-ul explicativ este aici:

- `event_study_explicat_ro.ipynb`

## Varianta simpla: VS Code

1. Deschide folderul `event-study/` in VS Code.
2. Instaleaza extensiile `Python` si `Jupyter` daca nu sunt deja instalate.
3. Din terminalul din `event-study/`, ruleaza:

```bash
uv sync
```

4. Deschide notebook-ul `notebooks/event_study_explicat_ro.ipynb`.
5. Alege kernel-ul din `.venv` al proiectului.
6. Apasa `Run All`.

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
