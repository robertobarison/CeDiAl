.. _Oggetto Paziente:

:index:`Paziente <Oggetto Paziente>`
=============================================================================
L'oggetto Paziente identifica i singoli pazienti che frequentano il Centro Diurno e contiene o è collegato ai dati
necessari alla gestione del paziente.

L'oggetto paziente contiene le seguenti informazioni:

- Nome
- Cognome
- Soprannome
- Sesso
- Data di nascita
- Luogo di nascita
- Residenza
- Tipo di residenza (Tabella)
- Stato Civile (Tabella)
- Lingua (Tabella)
- Titolo di studio (Tabella)
- Professioni svolte (Tabella)

- Informazioni familiari

- :ref:`Oggetto Contatto`
- Mezzo di trasferimento al Centro Diurno
- Data di inizio frequenza Centro Diurno
- Data di fine frequenza Centro Diurno
- Motivo fine frequenza (Tabella)
- :ref:`Medico Curante<Oggetto Medico>`

- :ref:`Oggetto Cartella Clinica`

- Storia del paziente (eventi principali della sua vita)

- Stato in CeDiAl (collegare gli stati dispinibili)

L'oggetto paziente viene creato dalla funzione :ref:`Gestione Nuovo Paziente` e viene modificato e cancellato dalla
funzione :ref:`Gestione Modifica Paziente`.

Operazioni sui pazienti:

- nuovo paziente (anagrafica)
- modifica paziente (anagrafica)
- cambia stato (opeartivo)
