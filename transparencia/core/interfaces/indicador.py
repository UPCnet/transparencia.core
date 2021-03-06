# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form
from plone.autoform import directives as form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from plone.namedfile.field import NamedBlobFile
from plone.formwidget.querystring.widget import QueryStringFieldWidget
from plone.supermodel import model

from plone.formwidget.namedfile.widget import NamedFileFieldWidget


from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName


from zope.i18nmessageid import MessageFactory
_ = MessageFactory("transparencia")

from plone.directives import form

import datetime
from plone.indexer import indexer


# from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# organizers = SimpleVocabulary(
#     [SimpleTerm(value=u'Bill', title=_(u'Bill')),
#      SimpleTerm(value=u'Bob', title=_(u'Bob')),
#      SimpleTerm(value=u'Jim', title=_(u'Jim'))]
#     )


from zope.schema.interfaces import IVocabularyFactory

class CategoriesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        utool = getToolByName(context, 'portal_url')   
        items = catalog.searchResults(
            portal_type='Categoria',
            review_state = 'published',
            sort_on='idCategoria', 
            sort_order='ascending')

        terms = []
        for item in items:
            obj = item.getObject()
            terms.append(SimpleVocabulary.createTerm(obj.identificador, str(obj.identificador), obj.identificador))
                        
        return SimpleVocabulary(terms)

grok.global_utility(CategoriesVocabulary, name=u"vocabulary.Categories")

class LleisVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        utool = getToolByName(context, 'portal_url')        
        items = catalog.searchResults(
            portal_type='Llei',
            review_state = 'published',
            sort_on='sortable_title', 
            sort_order='ascending')

        terms = []
        for item in items:
            obj = item.getObject()
            terms.append(SimpleVocabulary.createTerm(obj.id, str(obj.id), obj.title_or_id()))
        
        return SimpleVocabulary(terms)

grok.global_utility(LleisVocabulary, name=u"vocabulary.Lleis")


class IIndicador(form.Schema):
    """Una llei
    """

    descripcio_indicador = RichText(
        title=_(u"Descripció indicador"),
        description=_(u"Afegeix un text explicatiu de l'indicador"),
        required=True,
    )

    start = schema.Datetime(
        title=_(u"Data Inici"),
        description=_(u"Afegeix la data inici de vigencia de l'indicador"),
        required=False,
    )

    end = schema.Datetime(
        title=_(u"Data Fi"),
        description=_(u"Afegeix la data fi de vigencia de l'indicador"),
        required=False,
    )


    keywords_categories = schema.List(
        title=u"Categories", 
        description=_(u"Selecciona les categories a les que correspon aquest indicador"),
        value_type=schema.Choice(title=u"Categories", 
                                 vocabulary=u"vocabulary.Categories",
                                 required=True)
    )   

    keywords_llei = schema.List(
        title=u"Lleis", 
        description=_(u"Selecciona les lleis a les que correspon aquest indicador"),
        value_type=schema.Choice(title=u"Lleis", 
                                 vocabulary=u"vocabulary.Lleis",
                                 required=True)
    )

    #Criterios valoración --> por ahora fijos    
    valoracio_publicat = schema.Int(
        title=_(u"Publicat"),
        description=_(u"Afegeix una valoració de 0 a 10"),
        required=True,
    ) 

    valoracio_comprensio = schema.Int(
        title=_(u"Comprensió / infografia"),
        description=_(u"Afegeix una valoració de 0 a 10"),
        required=True,
    ) 

    resultat_agregat = schema.Int(
        title=_(u"Resultat Agregat"),
        description=_(u"El resultat agregat 100%"),
        required=False,
    ) 

    #Ocultar el camp
    form.omitted('resultat_agregat')

@indexer(IIndicador)
def keywords_categories(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``community_type`` value count it and index.
    """    
    return context.keywords_categories
grok.global_adapter(keywords_categories, name='keywords_categories')

@indexer(IIndicador)
def keywords_llei(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``community_type`` value count it and index.
    """       
    return context.keywords_llei
grok.global_adapter(keywords_llei, name='keywords_llei')

#Inicialitzar valors camps

@form.default_value(field=IIndicador['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

@form.default_value(field=IIndicador['valoracio_publicat'])
def valoracio_publicatDefaultValue(data):
    return 0

@form.default_value(field=IIndicador['valoracio_comprensio'])
def valoracio_comprensioDefaultValue(data):
    return 0

# @form.default_value(field=IIndicador['end'])
# def endDefaultValue(data):
#     return datetime.datetime.today()    