##############################################################################
#
#  CeDiAl - Centro Diurno Alzheimer
#  2011 Roberto Barison - roberto.barison@anche.no
#
#  This file is part of CeDiAl.
#
#  CeDiAl is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  CeDiAl is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with CeDiAl.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
.. _module:: util
    :platform: Unix, Windows
    :synopsis: Utility per CeDiAl

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard

# Librerie di terze parti

# Librerie locali


# ===========================================================================
# Definizione del menu
#    Testo
#    Funzionalita
#    URL
# ===========================================================================

MENU_LOGIN = [
    ['Presentazione', '', '/'],
    ['Test', '', '/test/'],
    ['Gestione', '', '/gestione/'],
    ['Esci', '', '/logout/'],
]

MENU_LOGOUT = [
    ['Presentazione', '', '/'],
    ['Login', '', '/login/'],
]


# ===========================================================================
# Definizione oggetti
# ===========================================================================
OBJ_ENTE = 'ente'
OBJ_PAZIENTE = 'paziente'
OBJ_RUOLO = 'ruolo'
OBJ_TEST = 'test'
OBJ_UTENTE = 'utente'


# ===========================================================================
# Definizione permessi
# ===========================================================================
PERM_PAZIENTI = 'Gestione pazienti'
PERM_RUOLI = 'Gestione ruoli'
PERM_TEST = 'Gestione test'
PERM_UTENTI = 'Gestione utenti'


# ===========================================================================
# Definizione stati pazienti
# ===========================================================================
STATO_PAZ = 'Paziente'
STATO_PAZ_ATTESA = 'Attesa'
STATO_PAZ_ATTIVO = 'Attivo'
STATO_PAZ_SOSPESO = 'Sospeso'
STATO_PAZ_FINITO = 'Finito'


# ===========================================================================
# Definizione stati test
# ===========================================================================
STATO_TEST = 'Test'
STATO_TEST_ATTIVO = 'Attivo'
STATO_TEST_INATTIVO = 'Inattivo'
STATO_TEST_SOSPESO = 'Sospeso'


# ===========================================================================
# Definizione delle azioni di gestione
# ===========================================================================
AZ_GEST_ELENCO = 'elenco'
AZ_GEST_NUOVO = 'nuovo'
AZ_GEST_MODIFICA = 'modifica'


