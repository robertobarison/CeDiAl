.. Installazione documentation master file, created by
   sphinx-quickstart on Sat Sep  8 14:36:19 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Manuale di installazione di CeDiAl
=========================================

Sommario:

.. toctree::
   :maxdepth: 2


Introduzione
-------------------------------------------

Requisiti di sistema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Componenti di CeDiAl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Procedura di installazione
-------------------------------------------
#. Installare python e django::

    apt-get install python-setuptools python-dev python-django

#. Scompattare cedial in una directory a piacere che chiameremo cedial_base.

#. Aprire un terminale e portarsi nella directory <cedial_base>/cedial.

#. Creare il database::

    ./manage.py syncdb

   Scegliere NO quando chiede di creare un utente amministratore del database.

#. Attivare cedial::

    ./manage.py runserver


Attivare CeDiAl la prima volta
-------------------------------------------
#. Accedere alla fase di inizializzazione di cedial mediante l'url http://localhost:8000/init/ ed utilizzare utente init con password cedial.

#. Scegliere il menu Login ed accedere con utente cedial e password cedial.

Referenze
-------------------------------------------


Indici e tabelle
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

