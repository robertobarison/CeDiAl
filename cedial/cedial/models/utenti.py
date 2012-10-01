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
.. _module:: utenti
    :platform: Unix, Windows
    :synopsis: Definizione del model di utenti

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django.contrib.auth.models import User
from django.db import models

# Librerie di terze parti

# Librerie locali
from cedial.models.ruoli import Ruoli


class Utenti(User):
    # Inheriting from User
    matricola = models.CharField(max_length=100, )
    #ruolo = models.ManyToManyField(Ruoli, )
    ruolo = models.ForeignKey(Ruoli)
    #funzionalita = models.ManyToManyField(Funzionalita, )
    #ente = models.ForeignKey(Ente, )
    homepage = models.CharField(max_length=300, )

    data_ins = models.DateTimeField(verbose_name='data inserimento', auto_now_add=True, )

    def __unicode__(self):
        return self.username + ' - ' + self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['first_name']
        app_label = 'cedial'

