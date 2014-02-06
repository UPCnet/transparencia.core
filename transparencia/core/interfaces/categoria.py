# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("transparencia")


class ICategoria(form.Schema):
    """Una llei
    """

    identificador = schema.TextLine(
        title=_(u"Identificador"),
        description=_(u"Afegeix l'identificador de la categoria"),
        required=True,
    ) 