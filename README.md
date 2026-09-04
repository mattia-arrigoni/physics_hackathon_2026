# physics_hackathon_2026
Physics Hackathon 2026 - A un MILIONE di passi da casa

Università degli Studi di Milano-Bicocca, 31 agosto - 4 settembre 2026
Progetto: simulazioni numeriche per caratterizzare il comportamento della materia attiva

Studio delle ABP (Active Brownian Particles) in un potenziale a doppia buca, 
caratterizzando una funzione committor (probabilità di finire nella regione T 
prima di finire in R) e considerando le regioni più visitate, al crescere dell'attività.

La libreria "libreria_cammini" simula il percorso di una singola particella, soggetta
alla forza -gradU, al moto browniano ed alla propria attività;
la libreria "libreria_committor" raccoglie i dati, simulando molti cammini 
da posizioni casuali in una regione adeguata, e li raccoglie in funzioni discrete.
La libreria "statistica_potenziale" raccoglie le funzioni per lo studio dei parametri critici 
individuati, ovvero "sigma" il rapporto tra la forza attiva v/mu e la moda di gradU,
e il Saddle-Crossing SC il rapporto tra i conteggi effettuati nella fascia centrale e i conteggi totali.
