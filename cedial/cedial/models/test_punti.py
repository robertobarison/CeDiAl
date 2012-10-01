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
.. _module:: tests_punti
    :platform: Unix, Windows
    :synopsis: Definizione del model dei punti dei tests

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django.db import models

# Librerie di terze parti

# Librerie locali
from cedial.models import Stati


class TestsPunti(models.Model):
    nome = models.CharField(max_length=300, )
    descrizione = models.CharField(max_length=500, )
    numero_punti = models.IntegerField()
    stato = models.ForeignKey(Stati)

    data_ins = models.DateTimeField(verbose_name='data inserimento', auto_now_add=True, )

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        app_label = 'cedial'

