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
.. _module:: ente
    :platform: Unix, Windows
    :synopsis: Definizione del model di ente

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django.db import models

# Librerie di terze parti

# Librerie locali
from cedial.models.stati import Stati


class Pazienti(models.Model):
    nome = models.CharField(max_length=100, db_index=True, )
    cognome = models.CharField(max_length=100, db_index=True, )

    cod_fiscale = models.CharField(max_length=16, db_index=True, )
    info_famiglia = models.CharField(max_length=100, db_index=True, )
    residenza = models.CharField(max_length=100, db_index=True, )
    contatto = models.CharField(max_length=100, db_index=True, )

    stato = models.ForeignKey(Stati)

    data_ins = models.DateTimeField(verbose_name='data inserimento', auto_now_add=True, )

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ['cognome', 'nome']
        app_label = 'cedial'
        unique_together = (("nome", "cognome"), )
