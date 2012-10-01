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
.. _module:: presentazione
    :platform: Unix, Windows
    :synopsis: Impostazioni di cedial

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging

# Librerie di terze parti

# Librerie locali
from cedial.models.pazienti import Pazienti
from cedial.models.utenti import Utenti
from cedial.util import STATO_PAZ_ATTIVO


def home(request):
    """
    Funzione di gestione della home page
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}
    try:
        sessid = 'sessionid=' + request.COOKIES["sessionid"]
    except:
        sessid = ''

    template = 'cedial/presentazione/presentazione_sommario.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s %s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], sessid,
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def pazienti(request):
    """
    Visualizzazione elenco pazienti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    logmsg = ''
    try:
        variabili['pazienti'] = Pazienti.objects.filter(stato__nome=STATO_PAZ_ATTIVO)
        ret = render_to_response('cedial/presentazione/pazienti.html', variabili, RequestContext(request))
    except Pazienti.DoesNotExist:
        logger.info('action=redirect_to_home msg=%s' % logmsg)
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                                 variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def paziente(request, azione, id_paziente):
    """
    Presentazione pazienti e azioni
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    logmsg = ''
    try:
        variabili['pazienti'] = Pazienti.objects.filter(stato__nome=STATO_PAZ_ATTIVO)
        ret = render_to_response('cedial/presentazione/pazienti.html', variabili, RequestContext(request))
    except Pazienti.DoesNotExist:
        logger.info('action=redirect_to_home msg=%s' % logmsg)
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
            variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def entrata(request):
    """
    Funzione di entra paziente
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/presentazione/entrata.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def uscita(request):
    """
    Funzione di entra paziente
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/presentazione/entrata.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))

