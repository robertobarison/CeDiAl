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
.. _module:: gestione_test
    :platform: Unix, Windows
    :synopsis: Form per la gestione dei test

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django.forms.widgets import Select
from django import forms

# Librerie di terze parti

# Librerie locali
from cedial.models import Stati


class GestioneTestForm(forms.Form):
    """
    Form per la gestionde degli utenti
    """
    def __init__(self, *args, **kwargs):
        modifica = kwargs.pop('modifica')
        super(GestioneTestForm, self).__init__(*args, **kwargs)

        self.fields['nome'] = forms.CharField(max_length=300)
        self.fields['descrizione'] = forms.CharField(max_length=500)
        self.fields['numero_punti'] = forms.IntegerField()

    def __unicode__(self):
        return self.nome + ' ' + self.cognome
