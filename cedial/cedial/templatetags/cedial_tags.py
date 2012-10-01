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
.. _module:: cedial_tags
    :platform: Unix, Windows
    :synopsis: templatetags di cedial

.. moduleauthor:: Roberto Barison <roberto.barison@anche.no>
"""

# Librerie standard
from django import template

# Librerie di terze parti

# Librerie locali
from cedial.models.utenti import Utenti
from cedial.util import MENU_LOGIN, MENU_LOGOUT, PERM_UTENTI, PERM_TEST, AZ_GEST_ELENCO


register = template.Library()

class StatoNode(template.Node):
    def __init__(self, utente):
        self.utente = template.Variable(utente)

    def render(self, context):
        """
        Costruisce il pannello informativo della pagina di presentazione
        """
        try:
            u = self.utente.resolve(context)
            testo = '<br/>'
            testo = testo + 'Utente: ' + u.username + '<br/>'
            try:
                testo = testo + 'Matricola: ' + str(u.matricola) + '<br/>'
                testo = testo + '' + u.first_name + ' ' + u.last_name + '<br/>'
                testo = testo + 'Ruolo: ' + u.ruolo.nome + '<br/>'
                testo = testo + 'Unit&agrave;: ' + str(u.unita) + '<br/>'
            except:
                pass
        except template.VariableDoesNotExist:
            testo = 'Utente non autenticato'
        return testo


@register.tag
def cedial_stato(parser, token):
    """
    Costruisce il pannello informativo della pagina di presentazione
    """
    try:
        tag_name, utente = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return StatoNode(utente)


class MenuNode(template.Node):
    """
    Costruisce il menu
    """

    def __init__(self, utente):
        self.utente = template.Variable(utente)

    def render(self, context):
        testo = '<ul>'
        u = self.utente.resolve(context)
        if u != '' :
            # utente = Utenti.objects.get(username=u.username)
            for m in MENU_LOGIN:
                testo += '<li><a href="' + m[2] + '">' + m[0] + '</a></li>'
            testo += '</ul>'
        else:
            for m in MENU_LOGOUT:
                testo += '<li><a href="' + m[2] + '">' + m[0] + '</a></li>'
            testo += '</ul>'
        return testo


@register.tag
def cedial_menu(parser, token):
    """
    Costruisce il menu
    """
    try:
        tag_name, utente = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return MenuNode(utente)


class MenuGestNode(template.Node):
    def __init__(self, utente):
        self.utente = template.Variable(utente)
    def render(self, context):
        try:
            u = self.utente.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        testo = '<ul>'
        testo = testo + '<li><a href="' + '/gestione/paziente/' + AZ_GEST_ELENCO + '/0/' + '">Pazienti</a></li>'
        if u.ruolo.funzionalita.filter(nome=PERM_TEST).exists():
            testo = testo + '<li><a href="' + '/gestione/test/' + AZ_GEST_ELENCO + '/0/' + '">Test</a></li>'
        if u.ruolo.funzionalita.filter(nome=PERM_UTENTI).exists():
            testo = testo + '<li><a href="' + '/gestione/ente/' + AZ_GEST_ELENCO + '/0/' + '">Enti</a></li>'
            testo = testo + '<li><a href="' + '/gestione/ruolo/' + AZ_GEST_ELENCO + '/0/' + '">Ruoli</a></li>'
            testo = testo + '<li><a href="' + '/gestione/utente/' + AZ_GEST_ELENCO + '/0/' + '">Utenti</a></li>'
        testo = testo + '<li><a href="' + '/gestione/password/' + '">Cambio Password</a></li>'
        testo += '</ul>'
        return testo


@register.tag
def cedial_menu_gest(parser, token):
    """
    Costruisce il menu di gestione
    """
    try:
        tag_name, utente = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return MenuGestNode(utente)


