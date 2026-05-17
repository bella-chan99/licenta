repo-u lu bebe de git:

https://github.com/bella-chan99/licenta

Ca sa poti sa lucrezi pe el, te duci prima data din termimnal pe folderul unde vrei tu sa lucrezi la licenta folosind comanda

```bash
cd
```

gen:
cd ~/Documents/licenta

sau pe unde ai tu deja folderu de lucrezi la ea.

si dupa faci

git clone https://github.com/bella-chan99/licenta

acum, ca sa poti sa faci schimbari pe repo-ul asta si sa lucrezi chiar pe el: Mergi pe setari in github si dai scroll in stanga jos la deleloper settings: personal access tokens -> tokens (classic).
Dupa in dreapta-sus: generate new token -> generate new token (classic) 

La note scrii orice, doar cum s-o numesti
expiration, ai putea sa-ti pui no expiration i think it's pretty oki

si bifezi casutele mari de la urmatoarele categorii:

repo
gist
notifications
user
copilot


cam atat

dupa o sa-ti apara cheia aia, dai copy, si pastraz-o bine ca n-o sa mai potii s-o vezi din nou a doua oaraa.

dupa mergi inapoi in terminal si scrii

```

cat <<'EOF' | git credential approve
protocol=https
host=github.com
username=bella-chan99
password=TOKENU_LU_BUBU
EOF

```

trebuie sa schimbi "TOKENU_LU_BUBU" ala cu fix ala de i-ai dat copy

si dupa o sa poti sa folosesti repo-ul as intended 😎🔥🔥🔥🔥🔥🔥

BEBE YOU TEH BESTT YOUJ MADE IT ALL THE WAY TO THE ENDD LIKE WAHTT YOU"RE INSANEE go take yuourself a treattt  😎😎😎😎😎😎
