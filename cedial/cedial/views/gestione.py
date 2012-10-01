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
.. _module:: gestione
    :platform: Unix, Windows
    :synopsis: Pagine di gestione del sistema

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
import datetime
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging

# Librerie di terze parti

# Librerie locali
from cedial.forms.cambio_password import CambioPasswordForm
from cedial.forms.gestione_paziente import GestionePazienteForm
from cedial.forms.gestione_ruolo import GestioneRuoloForm
from cedial.forms.gestione_test import GestioneTestForm
from cedial.forms.gestione_utente import GestioneUtenteForm
from cedial.forms.login import LoginForm
from cedial.models import Enti, Pazienti, Ruoli, Stati, Tests, Utenti
from cedial.util import PERM_UTENTI, PERM_PAZIENTI, PERM_TEST, PERM_RUOLI, \
    STATO_TEST_INATTIVO, \
    AZ_GEST_ELENCO, AZ_GEST_MODIFICA, AZ_GEST_NUOVO, \
    OBJ_ENTE, OBJ_UTENTE, OBJ_TEST, OBJ_RUOLO, OBJ_PAZIENTE

def gestione(request):
    """
    Funzione di gestione del sistema
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = 'cedial/gestione/gestione_sommario.html'
    if request.user.is_authenticated():
        variabili['utente'] = Utenti.objects.get(id=request.user.id)
    else:
        variabili['form'] = LoginForm()

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def pazienti(request):
    """
    Visualizzazione elenco pazienti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    logmsg = ''
    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente
        if utente.ruolo.funzionalita.filter(nome=PERM_PAZIENTI).exists():
            try:
                variabili['pazienti'] = Pazienti.objects.all()
                ret = render_to_response('cedial/gestione/pazienti.html', variabili, RequestContext(request))
            except Pazienti.DoesNotExist:
                logmsg = 'pazienti_non_esiste'
        else:
            logmsg = 'utente_non_autorizzato'
    except Utenti.DoesNotExist:
        logmsg = 'utente_non_esiste'

    if ret == '':
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
    Funzione di amministrazione dei pazienti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = ''
    messaggio = ''
    testo = ''
    form = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        if utente.ruolo.funzionalita.filter(nome=PERM_PAZIENTI).exists():
            variabili['azione'] = azione

            if azione == 'nuovo':
                if request.method == 'POST':
                    form = GestionePazienteForm(request.POST, modifica=False)
                    variabili['form'] = form
                    if form.is_valid():
                        nome = request.POST['nome']
                        cognome = request.POST['cognome']
                        try:
                            Pazienti.objects.get(nome=nome, cognome=cognome)
                            messaggio = u"Paziente gia' presente"
                        except Pazienti.DoesNotExist:
                            paziente = Pazienti()
                            paziente.nome = request.POST['nome']
                            paziente.cognome = request.POST['cognome']
                            paziente.stato = Stati.objects.get(tabella='Paziente', nome=form.cleaned_data['stato'])
                            paziente.save()
                            testo = 'Paziente ' + paziente.nome + ' creato correttamente'
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=paziente_create user=%s paziente=%s_%s' %
                                       (request.user, paziente.nome, paziente.cognome, ))
                    else:
                        messaggio = u'Alcuni campi non sono stati compilati'
                else:
                    variabili['form'] = GestionePazienteForm(modifica=False)

                if messaggio != '':
                    logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
                    variabili['messaggio'] = messaggio
                variabili['testo'] = testo
                template = 'cedial/gestione/paziente.html'

            elif azione == 'modifica':
                if request.method == 'POST':
                    if 'modifica' in request.POST:
                        form = GestionePazienteForm(request.POST, modifica=True)
                        variabili['form'] = form
                        if form.is_valid():
                            paziente = Pazienti.objects.get(id=id_paziente)
                            paziente.nome = request.POST['nome']
                            paziente.cognome = request.POST['cognome']
                            paziente.stato = Stati.objects.get(tabella='Paziente', nome=form.cleaned_data['stato'])
                            paziente.save()
                            testo = "Paziente " + paziente.nome + ' ' + paziente.cognome + " modificato"
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=paziente_modify user=%s paziente=%s' % (request.user, paziente.nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                    elif 'password' in request.POST:
                        logger.debug('password=%s' % request.POST['password'])
                    elif 'cancella' in request.POST:
                        logger.debug('cancella=%s' % request.POST['cancella'])
                else:
                    try:
                        paziente = Pazienti.objects.get(id=id_paziente)
                        init = {
                            'nome': paziente.nome,
                            'cognome': paziente.cognome,
                            'stato': paziente.stato,
                            }
                        variabili['paziente'] = paziente
                        form = GestionePazienteForm(initial=init, modifica=True)
                    except Pazienti.DoesNotExist:
                        logger.info('action=redirect_to_gestione_sommario msg=pazienti_non_esiste')
                        template = 'cedial/gestione/gestione_sommario.html'
                if template == '':
                    variabili['form'] = form
                    variabili['testo'] = testo
                    variabili['messaggio'] = messaggio
                    template = 'cedial/gestione/paziente.html'
        else:
            logger.info('action=redirect_to_home msg=utente_non_autorizzato')
            template = 'cedial/presentazione/presentazione_sommario.html'

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        template = 'cedial/presentazione/presentazione_sommario.html'

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def tests(request):
    """
    Visualizzazione elenco test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    logmsg = ''
    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente
        if utente.ruolo.funzionalita.filter(nome=PERM_TEST).exists():
            try:
                variabili['tests'] = Tests.objects.all()
                ret = render_to_response('cedial/gestione/tests.html', variabili, RequestContext(request))
            except Utenti.DoesNotExist:
                logmsg = 'tests_non_esiste'
        else:
            logmsg = 'utente_non_autorizzato'
    except Utenti.DoesNotExist:
        logmsg = 'utente_non_esiste'

    if ret == '':
        logger.info('action=redirect_to_home msg=%s' % logmsg)
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
            variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def test(request, azione, id_test):
    """
    Funzione di amministrazione dei test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = ''
    messaggio = ''
    testo = ''
    form = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        if utente.ruolo.funzionalita.filter(nome=PERM_TEST).exists():
            variabili['azione'] = azione

            if azione == 'nuovo':
                if request.method == 'POST':
                    form = GestioneTestForm(request.POST, modifica=False)
                    variabili['form'] = form
                    if form.is_valid():
                        nome = request.POST['nome']
                        try:
                            Tests.objects.get(nome=nome)
                            messaggio = u"Test gia' presente"
                        except Tests.DoesNotExist:
                            test = Tests()
                            test.nome = request.POST['nome']
                            test.descrizione = request.POST['descrizione']
                            test.numero_punti = request.POST['numero_punti']
                            test.stato = Stati.objects.get(tabella='Test', nome=STATO_TEST_INATTIVO)
                            test.save()
                            testo = 'Test ' + test.id + ' [' + test.nome + '] creato correttamente'
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=create user=%s object=test id=%s name=%s' %
                                       (request.user, test.id, test.nome, ))
                    else:
                        messaggio = u'Alcuni campi non sono stati compilati'
                else:
                    variabili['form'] = GestioneTestForm(modifica=False)

                if messaggio != '':
                    logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
                    variabili['messaggio'] = messaggio
                variabili['testo'] = testo
                variabili['test'] = test
                template = 'cedial/gestione/test.html'

            elif azione == 'modifica':
                if request.method == 'POST':
                    if 'modifica' in request.POST:
                        form = GestioneTestForm(request.POST, modifica=True)
                        variabili['form'] = form
                        if form.is_valid():
                            test = Tests.objects.get(id=id_test)
                            test.nome = request.POST['nome']
                            test.descrizione = request.POST['descrizione']
                            test.numero_punti = request.POST['numero_punti']
                            test.save()
                            testo = "Test " + test.nome + " modificato"
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=modify user=%s object=test id=%s name=%s' %
                                       (request.user, test.id, test.nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                    elif 'cancella' in request.POST:
                        logger.debug('cancella=%s' % request.POST['cancella'])
                else:
                    try:
                        test = Tests.objects.get(id=id_test)
                        init = {
                            'nome': test.nome,
                            'descrizione': test.descrizione,
                            'numero_punti': test.numero_punti,
                            'stato': test.stato,
                            }
                        variabili['test'] = test
                        form = GestioneTestForm(initial=init, modifica=True)
                    except Tests.DoesNotExist:
                        logger.info('action=redirect_to_gestione_sommario msg=pazienti_non_esiste')
                        template = 'cedial/gestione/gestione_sommario.html'
                if template == '':
                    variabili['form'] = form
                    variabili['testo'] = testo
                    variabili['test'] = test
                    variabili['messaggio'] = messaggio
                    template = 'cedial/gestione/test.html'
        else:
            logger.info('action=redirect_to_home msg=utente_non_autorizzato')
            template = 'cedial/presentazione/presentazione_sommario.html'

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        template = 'cedial/presentazione/presentazione_sommario.html'

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def punti(request, azione, id_test):
    """
    Funzione di amministrazione dei punti dei test
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    template = ''
    messaggio = ''
    testo = ''
    form = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        if utente.ruolo.funzionalita.filter(nome=PERM_TEST).exists():
            variabili['azione'] = azione

            if azione == 'modifica':
                if request.method == 'POST':
                    if 'modifica' in request.POST:
                        form = GestioneTestForm(request.POST, modifica=True)
                        variabili['form'] = form
                        if form.is_valid():
                            test = Tests.objects.get(id=id_test)
                            test.nome = request.POST['nome']
                            test.descrizione = request.POST['descrizione']
                            test.numero_punti = request.POST['numero_punti']
                            test.save()
                            testo = "Test " + test.nome + " modificato"
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=modify user=%s object=test id=%s name=%s' %
                                       (request.user, test.id, test.nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                    elif 'cancella' in request.POST:
                        logger.debug('cancella=%s' % request.POST['cancella'])
                else:
                    try:
                        test = Tests.objects.get(id=id_test)
                        init = {
                            'nome': test.nome,
                            'descrizione': test.descrizione,
                            'numero_punti': test.numero_punti,
                            'stato': test.stato,
                            }
                        variabili['test'] = test
                        form = GestioneTestForm(initial=init, modifica=True)
                    except Tests.DoesNotExist:
                        logger.info('action=redirect_to_gestione_sommario msg=pazienti_non_esiste')
                        template = 'cedial/gestione/gestione_sommario.html'
                if template == '':
                    variabili['form'] = form
                    variabili['testo'] = testo
                    variabili['test'] = test
                    variabili['messaggio'] = messaggio
                    template = 'cedial/gestione/test.html'
        else:
            logger.info('action=redirect_to_home msg=utente_non_autorizzato')
            template = 'cedial/presentazione/presentazione_sommario.html'

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        template = 'cedial/presentazione/presentazione_sommario.html'

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
            (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
             request.user, (tend - tstart).microseconds ))
    return render_to_response(template, variabili, RequestContext(request))


def utenti(request):
    """
    Visualizzazione elenco utenti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    logmsg = ''
    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente
        if utente.ruolo.funzionalita.filter(nome=PERM_UTENTI).exists():
            try:
                variabili['utenti'] = Utenti.objects.all()
                ret = render_to_response('cedial/gestione/utenti.html', variabili, RequestContext(request))
            except Utenti.DoesNotExist:
                logmsg = 'utenti_non_esiste'
        else:
            logmsg = 'utente_non_autorizzato'
    except Utenti.DoesNotExist:
        logmsg = 'utente_non_esiste'

    if ret == '':
        logger.info('action=redirect_to_home msg=%s' % logmsg)
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                                     variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def utente(request, azione, id_utente):
    """
    Funzione di amministrazione degli utenti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    messaggio = ''
    testo = ''
    form = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        #if utente.abil_utenti:
        variabili['azione'] = azione

        if azione == 'nuovo':
            if request.method == 'POST':
                form = GestioneUtenteForm(request.POST, modifica=False)
                variabili['form'] = form
                if form.is_valid():
                    username = request.POST['username']
                    try:
                        Utenti.objects.get(username=username)
                        messaggio = u"utente gia' presente"
                    except Utenti.DoesNotExist:
                        utente_def = Utenti()
                        utente_def.username = username
                        utente_def.set_password(request.POST['password1'])
                        utente_def.last_name = request.POST['nome']
                        utente_def.first_name = request.POST['cognome']
                        utente_def.email = request.POST['email']
                        utente_def.matricola = request.POST['matricola']
                        utente_def.ruolo = Ruoli.objects.get(nome=form.cleaned_data['ruolo'])
                        utente_def.is_active = True
                        utente_def.save()
                        testo = 'Utente ' + username + ' creato correttamente'
                        audit = logging.getLogger('cedial.audit')
                        audit.info('action=user_create user=%s new_user=%s' % (request.user, username, ))
                    else:
                        messaggio = u'Alcuni campi non sono stati compilati'
            else:
                variabili['form'] = GestioneUtenteForm(modifica=False)

            if messaggio != '':
                logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
                variabili['messaggio'] = messaggio
            variabili['testo'] = testo
            ret = render_to_response('cedial/gestione/utente.html', variabili, RequestContext(request))

        elif azione == 'modifica':
            if request.method == 'POST':
                if 'modifica' in request.POST:
                    form = GestioneUtenteForm(request.POST, modifica=True)
                    variabili['form'] = form
                    if form.is_valid():
                        username = request.POST['username']
                        utente_def = Utenti.objects.get(id=id_utente)
                        utente_def.username = username
                        utente_def.last_name = request.POST['nome']
                        utente_def.first_name = request.POST['cognome']
                        utente_def.email = request.POST['email']
                        utente_def.is_active = True
                        utente_def.matricola = request.POST['matricola']
                        utente_def.ruolo = Ruoli.objects.get(nome=request.POST['ruolo'])
                        utente_def.save()
                        testo = "Utente " + username + " modificato"
                        audit = logging.getLogger('cedial.audit')
                        audit.info('action=user_modify user=%s new_user=%s' % (request.user, username, ))
                    else:
                        messaggio = u'Alcuni campi non sono stati compilati'
                elif 'password' in request.POST:
                    logger.debug('password=%s' % request.POST['password'])
                elif 'cancella' in request.POST:
                    logger.debug('cancella=%s' % request.POST['cancella'])
            else:
                try:
                    utente_def = Utenti.objects.get(id=id_utente)
                    init = {
                        'username': utente_def.username,
                        'password1': utente_def.password,
                        'password2': utente_def.password,
                        'nome': utente_def.first_name,
                        'cognome': utente_def.last_name,
                        'matricola': utente_def.matricola,
                        'email': utente_def.email,
                        'ruolo': utente_def.ruolo,
                    }
                    form = GestioneUtenteForm(initial=init, modifica=True)
                except Utenti.DoesNotExist:
                    logger.info('action=redirect_to_gestione_sommario')
                    ret = render_to_response('cedial/gestione/gestione_sommario.html',
                                             variabili, RequestContext(request))
            if ret == '':
                variabili['form'] = form
                variabili['testo'] = testo
                variabili['messaggio'] = messaggio
                ret = render_to_response('cedial/gestione/utente.html', variabili, RequestContext(request))

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                                 variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def ruolo(request, azione, id_ruolo):
    """
    Funzione di amministrazione dei ruoli
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    messaggio = ''
    testo = ''
    form = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        if utente.ruolo.funzionalita.filter(nome=PERM_TEST).exists():
            variabili['azione'] = azione

            if azione == AZ_GEST_NUOVO:
                if request.method == 'POST':
                    form = GestioneRuoloForm(request.POST, modifica=False)
                    variabili['form'] = form
                    if form.is_valid():
                        nome = request.POST['nome']
                        try:
                            Ruoli.objects.get(nome=nome)
                            messaggio = u"ruolo gia' presente"
                        except Ruoli.DoesNotExist:
                            ruolo = Ruoli()
                            ruolo.nome = request.POST['nome']
                            ruolo.save()
                            testo = 'Ruolo ' + nome + ' creato correttamente'
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=user_create user=%s new_user=%s' % (request.user, nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                else:
                    variabili['form'] = GestioneRuoloForm(modifica=False)

                if messaggio != '':
                    logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
                    variabili['messaggio'] = messaggio
                variabili['testo'] = testo
                ret = render_to_response('cedial/gestione/ruolo.html', variabili, RequestContext(request))

            elif azione == AZ_GEST_MODIFICA:
                if request.method == 'POST':
                    if 'modifica' in request.POST:
                        form = GestioneRuoloForm(request.POST, modifica=True)
                        variabili['form'] = form
                        if form.is_valid():
                            ruolo = Ruoli.objects.get(id=id_ruolo)
                            ruolo.nome = request.POST['nome']
                            ruolo.save()
                            testo = "Ruolo " + ruolo.nome + " modificato"
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=user_modify user=%s new_user=%s' % (request.user, ruolo.nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                    elif 'password' in request.POST:
                        logger.debug('password=%s' % request.POST['password'])
                    elif 'cancella' in request.POST:
                        logger.debug('cancella=%s' % request.POST['cancella'])
                else:
                    try:
                        ruolo = Ruoli.objects.get(id=id_ruolo)
                        init = {
                            'nome': ruolo.nome,
                            }
                        form = GestioneRuoloForm(initial=init, modifica=True)
                        variabili['nome'] = ruolo.nome
                    except Ruoli.DoesNotExist:
                        logger.info('action=redirect_to_gestione_sommario')
                        ret = render_to_response('cedial/gestione/gestione_sommario.html',
                            variabili, RequestContext(request))
                if ret == '':
                    variabili['form'] = form
                    variabili['testo'] = testo
                    variabili['messaggio'] = messaggio
                    ret = render_to_response('cedial/gestione/ruolo.html', variabili, RequestContext(request))

            #azione di default elenco
            else:
                azione = AZ_GEST_ELENCO
                try:
                    tabella = Ruoli
                    variabili['elenco'] = tabella.objects.all()
                    ret = render_to_response('cedial/gestione/ruolo_elenco.html', variabili, RequestContext(request))
                except tabella.DoesNotExist:
                    logger.info('action=redirect_to_home msg=ruoli_non_esiste')
                    ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                        variabili, RequestContext(request))

        else:
            logger.info('action=redirect_to_home msg=utente_non_autorizzato')
            ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                variabili, RequestContext(request))

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
            variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('azione=%s method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (azione, request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret


def nuovo(request, oggetto, tabella):
    """
    Funzione di gestione della ricezione della form per la creazione di un nuovo oggetto

    Restituisce:
    testo: testo da scrivere nel log
    messaggio: messaggio di errore da visualizzare all'utente
    """
    messaggio = 'tipo di oggetto non riconosciuto'
    testo = ''
    if oggetto == OBJ_RUOLO:
        nome = request.POST['nome']
        try:
            tabella.objects.get(nome=nome)
            messaggio = oggetto + u" gia' presente"
        except tabella.DoesNotExist:
            ruolo = tabella()
            ruolo.nome = request.POST['nome']
            ruolo.save()
            testo = oggetto + ' ' + nome + ' creato correttamente'
            audit = logging.getLogger('cedial.audit')
            audit.info('action=user_create user=%s %s=%s' % (request.user, oggetto, nome, ))

    return testo, messaggio


def modifica_get(oggetto, obj):
    nome = ''
    if oggetto == OBJ_RUOLO:

        init = {
            'nome': obj.nome,
            }
        nome = obj.nome

    return init, nome


def modifica_post(oggetto, obj):
    nome = ''
    if oggetto == OBJ_RUOLO:

        init = {
            'nome': obj.nome,
            }
        nome = obj.nome

    return init, nome


def azioni(request, oggetto, azione, id_obj):
    """
    Funzione di amministrazione degli oggetti
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    ret = ''
    messaggio = ''
    testo = ''
    form = ''
    variabili['oggetto'] = oggetto
    variabili['azione'] = azione
    variabili['id_obj'] = id_obj

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        nomeform = GestionePazienteForm
        perm = ''
        tabella = pazienti
        if oggetto == OBJ_ENTE:
            perm = PERM_UTENTI
            tabella = Enti
            #nomeform = GestioneEnteForm
        elif oggetto == OBJ_PAZIENTE:
            perm = PERM_PAZIENTI
            tabella = Pazienti
            nomeform = GestionePazienteForm
        elif oggetto == OBJ_RUOLO:
            perm = PERM_RUOLI
            tabella = Ruoli
            nomeform = GestioneRuoloForm
        elif oggetto == OBJ_TEST:
            perm = PERM_TEST
            tabella = Tests
            nomeform = GestioneTestForm
        elif oggetto == OBJ_UTENTE:
            perm = PERM_UTENTI
            tabella = Utenti
            nomeform = GestioneUtenteForm
        #else:
        # Se l'oggetto non è corretto non faccio niente
            #oggetto = ''

        if perm != '' and utente.ruolo.funzionalita.filter(nome=perm).exists():
            variabili['azione'] = azione

            if azione == AZ_GEST_NUOVO:
                if request.method == 'POST':
                    # in POST ricevo la form compilata
                    form = nomeform(request.POST, modifica=False)
                    variabili['form'] = form
                    if form.is_valid():
                        testo, messaggio = nuovo(request, oggetto, tabella)
                    else:
                        messaggio = u'Alcuni campi non sono stati compilati'
                else:
                    # in GET ricevo la richiesta della form
                    variabili['form'] = nomeform(modifica=False)

                if messaggio != '':
                    logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
                    variabili['messaggio'] = messaggio
                variabili['testo'] = testo
                ret = render_to_response('cedial/gestione/modifica.html', variabili, RequestContext(request))

            elif azione == AZ_GEST_MODIFICA:
                # in POST ricevo la form compilata
                if request.method == 'POST':
                    if 'modifica' in request.POST:
                        form = nomeform(request.POST, modifica=True)
                        variabili['form'] = form
                        if form.is_valid():
                            ruolo = tabella.objects.get(id=id_obj)
                            ruolo.nome = request.POST['nome']
                            ruolo.save()
                            testo = "Ruolo " + ruolo.nome + " modificato"
                            audit = logging.getLogger('cedial.audit')
                            audit.info('action=user_modify user=%s new_user=%s' % (request.user, ruolo.nome, ))
                        else:
                            messaggio = u'Alcuni campi non sono stati compilati'
                    elif 'password' in request.POST:
                        logger.debug('password=%s' % request.POST['password'])
                    elif 'cancella' in request.POST:
                        logger.debug('cancella=%s' % request.POST['cancella'])
                else:
                    # in GET ricevo la richiesta della form
                    try:
                        obj = tabella.objects.get(id=id_obj)
                        init, variabili['nome'] = modifica_get(oggetto, obj)
                        form = nomeform(initial=init, modifica=True)
                    except tabella.DoesNotExist:
                        logger.info('action=redirect_to_gestione_sommario')
                        ret = render_to_response('cedial/gestione/gestione_sommario.html',
                            variabili, RequestContext(request))
                if ret == '':
                    variabili['form'] = form
                    variabili['testo'] = testo
                    variabili['messaggio'] = messaggio
                    ret = render_to_response('cedial/gestione/ruolo.html', variabili, RequestContext(request))

            # Azione di default elenco
            else:
                azione = AZ_GEST_ELENCO
                try:
                    variabili['elenco'] = tabella.objects.all()
                    ret = render_to_response('cedial/gestione/' + oggetto + '_elenco.html',
                        variabili, RequestContext(request))
                except tabella.DoesNotExist:
                    logger.info('action=redirect_to_home msg=' + oggetto + '_non_esiste')
                    ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                        variabili, RequestContext(request))

        else:
            logger.info('action=redirect_to_home msg=utente_non_autorizzato')
            ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                variabili, RequestContext(request))

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home msg=utente_non_esiste')
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
            variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('oggetto=%s azione=%s method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (oggetto, azione, request.method, request.path, request.META['REMOTE_ADDR'],
                 request.COOKIES["sessionid"], request.user, (tend - tstart).microseconds ))
    return ret


def password(request):
    """
    Funzione di cambio password
    """
    tstart = datetime.datetime.now()
    logger = logging.getLogger('cedial.file')
    variabili = {'data': datetime.date.today()}

    messaggio = ''
    testo = ''

    try:
        utente = Utenti.objects.get(id=request.user.id)
        variabili['utente'] = utente

        if request.method == 'POST':
            form = CambioPasswordForm(request.POST)
            if form.is_valid():
                password_old = request.POST['password_old']
                password_2 = request.POST['password_1']
                password_1 = request.POST['password_2']
                if utente.check_password(password_old):
                    if password_1 == password_2:
                        utente.set_password(password_1)
                        utente.save()
                        testo = u'Password cambiata con successo'
                        logger.info(
                            'action=changed_password sessionid=%s - %s' % (request.COOKIES["sessionid"], testo, ))
                    else:
                        messaggio = u'I campi Nuova password e Conferma password sono diversi'
                else:
                    messaggio = u'Password attuale sbagliata'
            else:
                messaggio = u'I campi non sono compilati'

        if messaggio != '':
            logger.info('action=errmsg sessionid=%s - %s' % (request.COOKIES["sessionid"], messaggio, ))
            variabili['messaggio'] = messaggio
        variabili['testo'] = testo
        if testo == '':
            variabili['form'] = CambioPasswordForm()
        ret = render_to_response('cedial/gestione/password.html', variabili, RequestContext(request))

    except Utenti.DoesNotExist:
        logger.info('action=redirect_to_home')
        ret = render_to_response('cedial/presentazione/presentazione_sommario.html',
                                 variabili, RequestContext(request))

    tend = datetime.datetime.now()
    logger.info('method=%s path=%s ipaddr=%s sessionid=%s user=%s responsetime=%s' %
                (request.method, request.path, request.META['REMOTE_ADDR'], request.COOKIES["sessionid"],
                 request.user, (tend - tstart).microseconds ))
    return ret
