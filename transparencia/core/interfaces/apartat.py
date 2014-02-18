# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.directives import form
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("transparencia")

from zope import schema


class IApartat(form.Schema):
    """ Banner con icon
    """  

    icon = schema.TextLine(
        title=_(u"Icona"),
        description=_(u"Nom de la classe de font awesome a fer servir per icona (sense el prefix icon-)"),
        required=False,
    )

    url = schema.TextLine(
        title=_(u"URL de destí"),
        description=_(u"Comença la url per http:// si vols enllaçar fora del teu espai."),
        required=False,
    )

    new_window = schema.Bool(
        title=_(u"Obrir en una nova finestra?"),
        description=_(u"Seleccioneu per obrir l'enllaç en una finestra nova"),
        default=True,
        required=False,
    )
