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
.. _module:: cambio_password
    :platform: Unix, Windows
    :synopsis: Form per il cambio password

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django import forms

# Librerie di terze parti

# Librerie locali


class CambioPasswordForm(forms.Form):
    """
    Form per il cambio password
    """
    password_old = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                   max_length=100, label='Password attuale', )
    password_1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                 max_length=100, label='Nuova password', )
    password_2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                 max_length=100, label='Conferma password', )

