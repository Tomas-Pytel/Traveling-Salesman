# 🗺️ Traveling Salesman – Optimalizácia trás v meste Čadca

Tento projekt je CLI aplikácia zameraná na riešenie známeho **Problému obchodného cestujúceho (TSP)**. Aplikácia simuluje hľadanie najefektívnejšej trasy medzi náhodne zvolenými adresami v reálnom prostredí mesta Čadca. (do úvahy sa berie vzdušná vzialenosť)

Projekt vznikol ako semestrálna práca v rámci predmetu zameraného na operačné systémy UNIX a algoritmizáciu.

## 🚀 Hlavné funkcie

- **Generovanie dát:** Používateľ definuje počet náhodných adries v meste, ktoré musí "cestujúci" navštíviť.
- **Porovnávanie algoritmov:** Aplikácia súčasne spúšťa viacero algoritmov a porovnáva ich úspešnosť (dĺžku nájdenej trasy).
- **Vizualizácia výsledkov:** Trasy sa ukladajú do samostatných súborov, ktoré umožňujú následné zobrazenie naplánovanej cesty na mape.
- **Interaktívne CLI:** Jednoduchá komunikácia s používateľom cez terminál s možnosťou opakovaných simulácií.

## 🧠 Implementované algoritmy

V projekte sú implementované a porovnávané tri rôzne prístupy k riešeniu TSP:
1. **Pažravá metóda (Greedy Algorithm):** Rýchla heuristika hľadajúca lokálne optimum.
2. **Metóda zdvojenej kostry (Double Tree Approximation):** Aproximačný algoritmus postavený na minimálnej kostre grafu.
3. **Metóda kostry a párenia (Christofidesov algoritmus):** Pokročilý algoritmus kombinujúci minimálnu kostru a úplné párenie, zaručujúci vysokú presnosť aproximácie.

## 🛠️ Technické detaily

- **Jazyk:** Python

## ⚙️ Použitie aplikácie

1. **Spustenie:** Po spustení programu zadajte požadovaný počet náhodných adries.
2. **Výpočet:** Aplikácia v reálnom čase vypočíta trasy pre všetky implementované algoritmy.
3. **Výstup:** Na konzole sa zobrazí porovnanie dĺžok trás.
4. **Export:** Podrobné trasy nájdete v priložených súboroch.
