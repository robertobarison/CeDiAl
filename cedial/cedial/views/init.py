# coding=utf-8
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
.. _module:: init
    :platform: Unix, Windows
    :synopsis: Azioni di aggiornamento del database

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
import logging

# Librerie di terze parti

# Librerie locali
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cedial.forms.login import LoginForm
from cedial.models.permessi import Permessi
from cedial.models.ruoli import Ruoli
from cedial.models.stati import Stati
from cedial.models.utenti import Utenti
from cedial.util import *


lista_permessi = [
    [PERM_PAZIENTI, [], ],
    [PERM_RUOLI, [], ],
    [PERM_TEST, [], ],
    [PERM_UTENTI, [], ],
]

def crea_permesso():
    """
    Inserisce le funzionalità base di cedial
    """
    logger = logging.getLogger('cedial.file')
    logger.info('action=start')
    testo = ''
    for obj in lista_permessi:
        if Permessi.objects.filter(nome=obj[0]).exists():
            msg = 'Permesso ' + obj[0] + ' presente'
        else:
            funzionalita = Permessi(nome=obj[0], )
            funzionalita.save()
            msg = 'Inserito permesso ' + obj[0]
        testo += str(datetime.datetime.now()) + ' - ' + msg + '<br>'
        logger.info('action=message - msg - %s' % (msg,))
    logger.info('action=end')
    return testo


lista_ruoli = [
    ['Amministratore', [PERM_PAZIENTI, PERM_RUOLI, PERM_TEST, PERM_UTENTI, ], ],
    ['Infermiere', [], ],
    ['Medico', [PERM_PAZIENTI, ], ],
]


def crea_ruoli():
    """
    Inserisce i ruoli base di cedial
    """
    logger = logging.getLogger('cedial.file')
    logger.info('action=start')
    testo = ''
    for obj in lista_ruoli:
        if Ruoli.objects.filter(nome=obj[0]).exists():
            msg = 'Ruolo ' + obj[0] + ' presente'
        else:
            ruolo = Ruoli(nome=obj[0], )
            ruolo.save()
            for f in obj[1]:
                func = Permessi.objects.get(nome=f)
                ruolo.funzionalita.add(func)
            ruolo.save()
            msg = 'Inserito ruolo ' + obj[0]
        testo += str(datetime.datetime.now()) + ' - ' + msg + '<br>'
        logger.info('action=message - msg - %s' % (msg,))
    logger.info('action=end')
    return testo


lista_stati = [
    [STATO_PAZ, STATO_PAZ_ATTESA, ],
    [STATO_PAZ, STATO_PAZ_ATTIVO, ],
    [STATO_PAZ, STATO_PAZ_SOSPESO, ],
    [STATO_PAZ, STATO_PAZ_FINITO, ],
    [STATO_TEST, STATO_TEST_ATTIVO, ],
    [STATO_TEST, STATO_TEST_INATTIVO, ],
    [STATO_TEST, STATO_TEST_SOSPESO, ],
]

def crea_stati():
    """
    Inserisce le funzionalità base di cedial
    """
    logger = logging.getLogger('cedial.file')
    logger.info('action=start')
    testo = ''
    for obj in lista_stati:
        if Stati.objects.filter(nome=obj[0]).exists():
            msg = 'Stato ' + obj[0] + ' presente'
        else:
            stato = Stati(tabella=obj[0], nome=obj[1], )
            stato.save()
            msg = 'Inserito stato ' + obj[0] + ' - ' + obj[1]
        testo += str(datetime.datetime.now()) + ' - ' + msg + '<br>'
        logger.info('action=message - msg - %s' % (msg,))
    logger.info('action=end')
    return testo


lista_utenti = [
    ['cedial', 'cedial', 'Amministratore', ],
]


def crea_utenti():
    """
    Inserisce gli utenti base di cedial
    """
    logger = logging.getLogger('cedial.file')
    logger.info('action=start')
    testo = ''
    for obj in lista_utenti:
        if Utenti.objects.filter(username=obj[0]).exists():
            msg = 'Utente ' + obj[0] + ' presente'
        else:
            utente = Utenti()
            utente.username = obj[0]
            utente.set_password(obj[1])
            utente.ruolo = Ruoli.objects.get(nome=obj[2])
            utente.is_active = True
            utente.is_staff = True
            utente.is_superuser = True
            utente.save()
            msg = 'Inserito utente ' + obj[0]
        testo += str(datetime.datetime.now()) + ' - ' + msg + '<br>'
        logger.info('action=message - msg - %s' % (msg,))
    logger.info('action=end')
    return testo


def init(request):
    """
    Funzione di inizializzazione del sistema
    """
    logger = logging.getLogger('cedial.file')
    logger.info('action=start sessionid=%s method=%s path=%s ipaddr=%s' %
                (request.COOKIES["sessionid"], request.method, request.path, request.META['REMOTE_ADDR'], ))

    messaggio = ''
    ret = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if username == 'init' and password == 'cedial':
                logger.info('action=login user=%s' % (username, ))
                msg = 'Inizio aggiornamento database'
                logger.info('action=message - %s' % (msg,))
                testo = str(datetime.datetime.now()) + ' - ' + msg + '<br>'

                testo += crea_permesso()
                testo += crea_ruoli()
                testo += crea_utenti()
                testo += crea_stati()

                msg = 'Aggiornamento database completato'
                logger.info('action=message - %s' % (msg,))
                testo += str(datetime.datetime.now()) + ' - ' + msg + '<br>'
                ret = render_to_response('cedial/init/init.html', {'testo': testo},
                    RequestContext(request))
            else:
                messaggio = u'Login fallito'
        else:
            messaggio = u'Mancano utente o password'

    if messaggio != '':
        logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
    if ret == '':
        form = LoginForm()
        ret = render_to_response('cedial/login/login.html', {
            'messaggio': messaggio,
            'form': form,
        }, RequestContext(request))

    logger.info('action=end user=%s sessionid=%s' % (request.user, request.COOKIES["sessionid"], ))
    return ret

