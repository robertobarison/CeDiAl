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
.. _module:: test
    :platform: Unix, Windows
    :synopsis: Gestione dei test

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging

# Librerie di terze parti

# Librerie locali
from cedial.models import Utenti


def test(request):
    """
    Funzione di gestione di test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/test/test_sommario.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def somministrazione(request):
    """
    Funzione di gestione di test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/test/somministrazione_menu.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def elenco(request):
    """
    Funzione di gestione di test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/test/test_sommario.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def analisi(request):
    """
    Funzione di gestione di test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/test/test_sommario.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


