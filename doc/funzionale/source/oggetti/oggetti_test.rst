.. _Oggetto Test:

:index:`Test <Oggetto Test>`
=============================================================================
L'oggetto Test definisce i possibili test da somministrare ai pazienti.

All'interno dei test vengono definiti i punti che corrispondono alle singole valutazioni da effettuare. Ciascun punto
del test è definito da una descrizione e da una valutazione numerica. Le valutazioni numeriche possono essere libere
all'interno di un intervallo predefinito oppure limitate a valori predefiniti e possono essere anche non omogenee
all'interno di un test.

Le valutazioni complessive di ciascun test comprenderanno calcolo di totale, media e mediana dei risultati di ciascun
punto.

Poichè la definizione dei test potrà variare nel tempo, i risultati di ciascun test somministrato dovranno contenere
anche la definizie del test somministrato.

I test conterranno soglie di valutazione per classificare i risultati ottenuti.

L'analisi storica dei test verrà effettuata basandoni sulle valutazioni complessive per cui, per ciascun test, sarà
necessario valutare se modificare il test esistente o crearne uno nuovo. Per esempio, se si deve inserire un nuovo
punto in un test la cui valutazione complessiva è la media probabilmente è possibile confrontare i nuovi risultati con
i risultati dei test senza il nuovo punto per cui può essere conveniente modificare il test. Se invece si deve inserire
un nuovo punto in un test la cui valutazione complessiva è la somma le valutazioni del vecchio e den nuovo test saranno
significativamente diverse per cui è meglio non confrontare i risultati ottenuto con e senza il nuovo punto e quindi
si dovrà procedere alla creazione di un nuovo test.


Contenuto:

- Periodo di somministrazione ottimale



Funzioni per il test:

- creazione test
- abilitazione test
- disabilitazione test
- copia test
- modifica test
- somministrazione test
- analisi test

Analisi test:

- Lettura singolo test
- Andamento risultati test per paziente
- Verifica somministrazione test
