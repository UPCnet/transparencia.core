# -*- coding: utf-8 -*-
"""Behaviours to assign tags (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""

from zope.interface import alsoProvides

from plone.directives import form

from zope import schema


from plone.app.textfield import RichText

from plone.app.textfield.value import RichTextValue


class IRichDescription(form.Schema):
    """Add tags to content
    """

    rich_description = RichText(
        title=u"Descripció amb format",
        description=u"Descripció amb format utilitzada per algunes vistes",
        required=False,
    )

alsoProvides(IRichDescription, form.IFormFieldProvider)



class INewDestacada(form.Schema):
    """Add tags to content
    """
   
    destacat = schema.Bool(
        title=u"Destacat",
        description=u"Noticia destacada",
        required=False,
    )

alsoProvides(INewDestacada, form.IFormFieldProvider)
