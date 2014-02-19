# -*- coding: utf-8 -*-
from zope.interface import implements

from plone.dexterity.content import Item
from plone.dexterity.content import Container
from zExceptions import NotFound

from copy import deepcopy

from plone.app.collection.collection import Collection
from plone.app.querystring.querybuilder import QueryBuilder

from Acquisition import aq_parent, aq_inner
from plone.app.collection.interfaces import ICollection


from transparencia.core.interfaces import ILlei
from transparencia.core.interfaces import ICategoria
from transparencia.core.interfaces import IIndicador
from transparencia.core.interfaces import IApartat

class Llei(Item):
    implements(ILlei)

class Categoria(Item):
    implements(ICategoria)

class Indicador(Container):
    implements(IIndicador)

    # @property
    # def resultat_agregat(self):
    # 	return 0

class Apartat(Item):
    implements(IApartat)

