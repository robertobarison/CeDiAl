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
.. _module:: login
    :platform: Unix, Windows
    :synopsis: Impostazioni di cedial

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
import datetime
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging

# Librerie di terze parti

# Librerie locali
from cedial.forms.login import LoginForm
from cedial.models.utenti import Utenti


def login(request):
    """
    Gestione della login al sistema
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    try:
        sid = request.COOKIES["sessionid"]
        sessid = 'sessionid=' + sid
    except:
        sid = ''
        sessid = ''
    ret = ''
    messaggio = ''
    username = ''
    uid = ''

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        username = request.POST['username']
        if form.is_valid(): # All validation rules pass
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    logger.info('action=login user=%s %s' % (username, sessid, ))
                    auth.login(request, user)
                    utente = Utenti.objects.get(username=username)
                    utente.save()
                    ret = HttpResponseRedirect('/firstpage/' + sid + '/')
                    audit = logging.getLogger('cedial.audit')
                    audit.info('action=login user=%s' % (username, ))
                    uid = user.id
                else:
                    messaggio = u'Utente disabilitato'
            else:
                messaggio = u' Login fallito'
        else:
            messaggio = u'Mancano utente o password'

    if messaggio != '':
        logger.info('action=errmsg utente=%s sessionid=%s - %s' %
                    (username, request.COOKIES["sessionid"], messaggio, ))
    if ret == '':
        form = LoginForm()
        ret = render_to_response('cedial/login/login.html', {
            'messaggio': messaggio,
            'form': form,
            }, RequestContext(request))

    tend = datetime.datetime.now()

    try:
        sessid = 'sessionid=' + request.COOKIES["sessionid"]
    except:
        sessid = ''

    logger.info('method=%s path=%s ipaddr=%s %s user=%s responsetime=%s uid=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], sessid,
                 request.user, (tend - tstart).microseconds, uid))
    return ret


def logout(request):
    """
    Funzione di logout
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    logger.info('action=logout sessionid=%s user=%s' % (request.COOKIES["sessionid"], request.user, ))
    audit = logging.getLogger('cedial.audit')
    audit.info('action=logout user=%s' % (request.user, ))
    auth.logout(request)
    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return HttpResponseRedirect("/")

