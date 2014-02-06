# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("transparencia")


class ILlei(form.Schema):
    """Una llei
    """

    descripcio_llei = RichText(
        title=_(u"Descripció llei"),
        description=_(u"Afegeix un text explicatiu de la llei"),
        required=True,
    )

    enllac_BOE = schema.URI(
        title=_(u"Enllaç de la llei al BOE"),
        description=_(u"Indiqueu l'enllàç de la llei al BOE."),
        required=True,
    )   