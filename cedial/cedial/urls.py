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
.. _module:: urls
    :platform: Unix, Windows
    :synopsis: Impostazioni di cedial

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django.conf.urls import patterns, include, url
from django.contrib import admin

# Librerie di terze parti

# Librerie locali

admin.autodiscover()

urlpatterns = patterns('',
    # Home page
    url(r'^$', 'cedial.views.presentazione.home', name='home'),

    # Funzioni di presentazione
    url(r'^presentazione/entrata/$', 'cedial.views.presentazione.entrata', ),
    url(r'^presentazione/paziente/(?P<azione>[^/]+)/(?P<id_paziente>[^/]+)/$', 'cedial.views.presentazione.paziente', ),
    url(r'^presentazione/pazienti/$', 'cedial.views.presentazione.pazienti', ),
    url(r'^presentazione/uscita/$', 'cedial.views.presentazione.uscita', ),

    # Funzioni di gestione dei test
    url(r'^test/$', 'cedial.views.test.test', name='test', ),
    url(r'^test/somministrazione/$', 'cedial.views.test.somministrazione', ),
    url(r'^test/elenco/$', 'cedial.views.test.elenco', ),
    url(r'^test/analisi/$', 'cedial.views.test.analisi', ),

    # Funzioni di gestione
    url(r'^gestione/$', 'cedial.views.gestione.gestione', name='gestione', ),
    url(r'^gestione/password/$', 'cedial.views.gestione.password', name='utenti', ),

    url(r'^gestione/(?P<oggetto>[^/]+)/(?P<azione>[^/]+)/(?P<id_obj>[^/]+)/$', 'cedial.views.gestione.azioni', ),


    #url(r'^gestione/pazienti/$', 'cedial.views.gestione.pazienti', name='pazienti', ),
    url(r'^gestione/paziente/(?P<azione>[^/]+)/(?P<id_paziente>[^/]+)/$', 'cedial.views.gestione.paziente', ),
    #url(r'^gestione/tests/$', 'cedial.views.gestione.tests', name='tests', ),
    url(r'^gestione/test/(?P<azione>[^/]+)/(?P<id_test>[^/]+)/$', 'cedial.views.gestione.test', ),
    #url(r'^gestione/punti/(?P<azione>[^/]+)/(?P<id_test>[^/]+)/$', 'cedial.views.gestione.punti', ),
    url(r'^gestione/ruoli/$', 'cedial.views.gestione.ruoli', name='utenti', ),
    #url(r'^gestione/ruolo/(?P<azione>[^/]+)/(?P<id_ruolo>[^/]+)/$', 'cedial.views.gestione.ruolo', ),
    url(r'^gestione/utenti/$', 'cedial.views.gestione.utenti', name='utenti', ),
    #url(r'^gestione/utente/(?P<azione>[^/]+)/(?P<id_utente>[^/]+)/$', 'cedial.views.gestione.utente', ),

    # Login e logout
    url(r'^login/$', 'cedial.views.login.login', name='login'),
    url(r'^logout/$', 'cedial.views.login.logout', name='logout', ),

    # Inizializzazione del sistema
    url(r'^init/$', 'cedial.views.init.init', name='init'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Tutte le pagine non trovate
    url(r'', 'cedial.views.presentazione.home', ),
)
