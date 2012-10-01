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
.. _module:: gestione utente
    :platform: Unix, Windows
    :synopsis: Form per la gestione degli utenti

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django import forms
from django.forms.widgets import Select

# Librerie di terze parti

# Librerie locali
from cedial.models.ruoli import Ruoli


def get_ruolo():
    ruolo = Ruoli.objects.all()
    lista = []
    for obj in ruolo:
        lista.append((obj.nome, obj.nome))
    return lista


class GestioneUtenteForm(forms.Form):
    """
    Form per la gestionde degli utenti
    """
    def __init__(self, *args, **kwargs):
        modifica = kwargs.pop('modifica')
        super(GestioneUtenteForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(max_length=100)
        if not modifica:
            self.fields['password1'] = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                                       max_length=100, label='Password')
            self.fields['password2'] = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                                       max_length=100, label='Conferma Password')
        self.fields['nome'] = forms.CharField(max_length=100)
        self.fields['cognome'] = forms.CharField(max_length=100)
        self.fields['matricola'] = forms.CharField(max_length=100)
        self.fields['email'] = forms.EmailField(max_length=100, required=False)
        self.fields['ruolo'] = forms.fields.ChoiceField(widget=Select, choices=get_ruolo(), )


