# -*- coding: utf-8 -*-
import loremipsum
import requests
import re
from random import choice

import transaction
from five import grok
from zope.interface import Interface
from zope.interface import alsoProvides

from Products.CMFCore.utils import getToolByName
from plone.namedfile.file import NamedBlobImage
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer

from genweb.core.interfaces import IHomePage
from Products.CMFPlone.interfaces import IPloneSiteRoot

from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from genweb.portlets.browser.manager import ISpanStorage

from datetime import datetime
import pkg_resources

from zope.interface import alsoProvides 
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.CMFPlone.utils import _createObjectByType

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True
    from plone.dexterity.utils import createContentInContainer

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

# from serveiesports.theme.portlets.queryportlet import Assignment as QueryPortletAssignment
# from serveiesports.theme.portlets.utils import setupQueryPortlet, setPortletAssignment

class setupHomePage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')
    grok.name("setup-portlets-transparencia")

    def render(self):
        portal = getSite()
        frontpage = portal['front-page']

         # Add portlets programatically
        from plone.app.portlets.portlets.navigation import Assignment as navigationAssignment    
        from vilaix.theme.portlets.noticiaDestacada import Assignment as noticiaDestacadaAssignment 
        from transparencia.theme.portlets.apartat import Assignment as apartatAssignment
    
        
        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager3', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['navegacio'] = navigationAssignment(root='/menu-lateral',topLevel=0, bottomLevel=1)

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager4', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['noticiaDestacada'] = noticiaDestacadaAssignment()   

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager4', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['apartats'] = apartatAssignment()   
        
        target_manager = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        target_manager_assignments = getMultiAdapter((portal, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['navegacioLateral'] = navigationAssignment(root='/menu-lateral',topLevel=0, bottomLevel=1)

     
        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager3')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '3'

        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager4')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '9'       

        return 'Done.'

#Setup inicial per crear continguts al portal de transparencia
class SetupView(grok.View):
    """
    """
    grok.context(Interface)
    grok.require("cmf.ManagePortal")
    grok.name("setup-inicial-transparencia")

    def createOrGetObject(self, context, newid, title, type_name):
        if newid in context.contentIds():
            obj = context[newid]
        else:
            obj = createContentInContainer(context, type_name, title=title, checkConstrains=False)
            transaction.savepoint()
            if obj.id != newid:
                context.manage_renameObject(obj.id, newid)
            obj.reindexObject()
        return obj

    def newCollection(self, context, newid, title, query=None):
        collection = self.createOrGetObject(context, newid, title, u'Collection')
        if query is not None:            
            collection.query = query
            collection.reindexObject()
        return collection

    def newFolder(self, context, newid, title, type_name=u'Folder'):
        return self.createOrGetObject(context, newid, title, type_name)

   
    def publish(self, obj):
        workflow_tool = getToolByName(self.context, "portal_workflow")
        try:
            workflow_tool.doActionFor(obj, "publish")
        except:
            pass

    def render(self):
        """
        """
        portal = getSite()
        frontpage = portal['front-page']  

        urltool = getToolByName(portal, 'portal_url')        
        portal_catalog = getToolByName(portal, 'portal_catalog')
        path = urltool.getPortalPath() 
        workflowTool = getToolByName(portal, "portal_workflow")
        pl = getToolByName(portal, 'portal_languages')

         
        # Delete old AT folders
        if getattr(portal, 'events', None):
            if portal.events.portal_type == 'Folder':
                portal.manage_delObjects(['events'])

        if getattr(portal, 'news', None):
            if portal.news.portal_type== 'Folder':
                portal.manage_delObjects(['news'])


        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/noticies')
        if obj.actual_result_count == 0:
            noticies = self.newFolder(portal, 'noticies', 'Noticies')
            noticies.description = 'Noticies del lloc'
            noticies.exclude_from_nav = True
            self.publish(noticies)

            # Set on them the allowable content types
            behavior = ISelectableConstrainTypes(noticies)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(('News Item', 'Collection'))
            behavior.setImmediatelyAddableTypes(('News Item', 'Collection'))

            noticies_destacades = self.newCollection(noticies, 'noticies-destacades', u'Noticies Destacades', query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']},
                                                                                                                       {u'i': u'review_state', u'o': u'plone.app.querystring.operation.selection.is', u'v': u'published'},
                                                                                                                       {u'i': u'destacat', u'o': u'plone.app.querystring.operation.boolean.isTrue', u'v': u'Sí'}])
            self.publish(noticies_destacades)

            noticies = self.newCollection(noticies, 'noticies', u'Noticies', query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']},
                                                                                      {u'i': u'review_state', u'o': u'plone.app.querystring.operation.selection.is', u'v': u'published'}])
            self.publish(noticies)          
                     
       
        #Menú Lateral       
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/menu-lateral')
        if obj.actual_result_count == 0:
            menu_lateral = self.newFolder(portal, 'menu-lateral', u'Menú lateral')
            menu_lateral.language = pl.getDefaultLanguage()
            menu_lateral.exclude_from_nav = True
            self.publish(menu_lateral)
            alsoProvides(menu_lateral, IHideFromBreadcrumbs)
            menu_lateral.reindexObject()

            lalcaldessa_per_la_transparencia = self.newFolder(menu_lateral, 'lalcaldessa-per-la-transparencia', u'L\'alcaldessa per la transparència')
            lalcaldessa_per_la_transparencia .language = pl.getDefaultLanguage()       
            self.publish(lalcaldessa_per_la_transparencia )
            lalcaldessa_per_la_transparencia .reindexObject() 
            
            els_carrecs_electes_municipals = self.newFolder(menu_lateral, 'els-carrecs-electes-municipals', u'Els càrrecs electes municipals')
            els_carrecs_electes_municipals.language = pl.getDefaultLanguage()       
            self.publish(els_carrecs_electes_municipals)
            els_carrecs_electes_municipals.reindexObject()  

            els_carrecs_de_lliure_designacio = self.newFolder(menu_lateral, 'els-carrecs-de-lliure-designacio', u'Els càrrecs de lliure designació')
            els_carrecs_de_lliure_designacio.language = pl.getDefaultLanguage()       
            self.publish(els_carrecs_de_lliure_designacio)
            els_carrecs_de_lliure_designacio.reindexObject()  

            indicadors_de_transparencia = self.newFolder(menu_lateral, 'indicadors-de-transparencia', u'Indicadors  de  transparència')
            indicadors_de_transparencia.language = pl.getDefaultLanguage()       
            self.publish(indicadors_de_transparencia)
            indicadors_de_transparencia.reindexObject()

            pressupostos_municipals = self.newFolder(menu_lateral, 'pressupostos-municipals', u'Pressupostos municipals')
            pressupostos_municipals.language = pl.getDefaultLanguage()       
            self.publish(pressupostos_municipals)
            pressupostos_municipals.reindexObject()

            patrimoni_municipal = self.newFolder(menu_lateral, 'patrimoni-municipal', u'Patrimoni municipal')
            patrimoni_municipal.language = pl.getDefaultLanguage()       
            self.publish(patrimoni_municipal)
            patrimoni_municipal.reindexObject()

            retiment_de_comptes = self.newFolder(menu_lateral, 'retiment-de-comptes', u'Retiment de comptes')
            retiment_de_comptes.language = pl.getDefaultLanguage()       
            self.publish(retiment_de_comptes)
            retiment_de_comptes.reindexObject()

            dret_dacces_a_la_informacio = self.newFolder(menu_lateral, 'dret-dacces-a-la-informacio', u'Dret d\'accés a la informació')
            dret_dacces_a_la_informacio.language = pl.getDefaultLanguage()       
            self.publish(dret_dacces_a_la_informacio)
            dret_dacces_a_la_informacio.reindexObject()

            dret_dacces_a_la_informacio = self.newFolder(menu_lateral, 'dret-dacces-a-la-informacio', u'Dret d\'accés a la informació')
            dret_dacces_a_la_informacio.language = pl.getDefaultLanguage()       
            self.publish(dret_dacces_a_la_informacio)
            dret_dacces_a_la_informacio.reindexObject()

            llei_de_transparencia = self.newFolder(menu_lateral, 'llei-de-transparencia', u'Llei de transparència')
            llei_de_transparencia.language = pl.getDefaultLanguage()       
            self.publish(llei_de_transparencia)
            llei_de_transparencia.reindexObject()

            novetats = self.newFolder(menu_lateral, 'novetats', u'Novetats')
            novetats.language = pl.getDefaultLanguage()       
            self.publish(novetats)
            novetats.reindexObject()

            enllacos_dinteres = self.newFolder(menu_lateral, 'enllacos-dinteres', u'Enllaços d\'interès')
            enllacos_dinteres.language = pl.getDefaultLanguage()       
            self.publish(enllacos_dinteres)
            enllacos_dinteres.reindexObject()



        
        #Material multimèdia
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia')
        if obj.actual_result_count == 0:
            material_multimedia = self.newFolder(portal, 'material-multimedia', u'Material multimèdia')
            material_multimedia.language = pl.getDefaultLanguage()
            material_multimedia.exclude_from_nav = True
            self.publish(material_multimedia)       
            material_multimedia.reindexObject()

        #Apartats
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/apartats')
        if obj.actual_result_count == 0:     
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()     
            apartats = self.newFolder(material_multimedia, 'apartats', u'Apartats')
            apartats.language = pl.getDefaultLanguage()
            apartats.exclude_from_nav = True
            self.publish(apartats)
            apartats.reindexObject()
        
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(apartats)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Apartat', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Apartat', 'Folder'))
   
        #Slider
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/sliders')
        if obj.actual_result_count == 0:            
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()
            slider = self.newFolder(material_multimedia, 'sliders', u'Sliders')
            slider.language = pl.getDefaultLanguage()
            slider.exclude_from_nav = True
            self.publish(slider)       
            slider.reindexObject()

        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(slider)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Slider', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Slider', 'Folder'))

        # #Banners
        # obj = portal_catalog.searchResults(portal_type = 'Folder',
        #                                     path = path + '/material-multimedia/banners')
        # if obj.actual_result_count == 0:     
        #     res = portal_catalog.searchResults(id = 'material-multimedia')
        #     if res:
        #         material_multimedia = res[0].getObject()     
        #     banners = self.newFolder(material_multimedia, 'banners', u'Banners')
        #     banners.language = pl.getDefaultLanguage()
        #     banners.exclude_from_nav = True
        #     self.publish(banners)       
        #     banners.reindexObject()
      
        # #Carrousel
        # obj = portal_catalog.searchResults(portal_type = 'Folder',
        #                                     path = path + '/material-multimedia/carroussel')
        # if obj.actual_result_count == 0:  
        #     res = portal_catalog.searchResults(id = 'material-multimedia')
        #     if res:
        #         material_multimedia = res[0].getObject()         
        #     carroussel = self.newFolder(material_multimedia, 'carroussel', u'Carroussel')
        #     carroussel.language = pl.getDefaultLanguage()
        #     carroussel.exclude_from_nav = True
        #     self.publish(carroussel)       
        #     carroussel.reindexObject()

        #Imatges Capçalera
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/imatges-capcalera')
        if obj.actual_result_count == 0: 
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()          
            imatges_capcalera = self.newFolder(material_multimedia, 'imatges-capcalera', u'Imatges capçalera')
            imatges_capcalera.language = pl.getDefaultLanguage()
            imatges_capcalera.exclude_from_nav = True
            self.publish(imatges_capcalera)       
            imatges_capcalera.reindexObject()           
      
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(imatges_capcalera)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Image', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Image', 'Folder'))

        # #Banners dreta
        # obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
        #                                         path = path + '/material-multimedia/banners/banners_dreta')
        # if obj.actual_result_count == 0:
        #     _createObjectByType('BannerContainer', banners, 'banners_dreta')  
        #     banners['banners_dreta'].setExcludeFromNav(True)
        #     banners['banners_dreta'].setTitle('Banners-dreta')
        #     banners['banners_dreta'].reindexObject()
        #     workflowTool.doActionFor(banners.banners_dreta, "publish")  


        # #Banners esquerra
        # obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
        #                                         path = path + '/material-multimedia/banners/banners_esquerra')
        # if obj.actual_result_count == 0:
        #     _createObjectByType('BannerContainer', banners, 'banners_esquerra')  
        #     banners['banners_esquerra'].setExcludeFromNav(True)
        #     banners['banners_esquerra'].setTitle('Banners-esquerra')
        #     banners['banners_esquerra'].reindexObject()
        #     workflowTool.doActionFor(banners.banners_esquerra, "publish")          
                
       
        # #Documents
        # obj = portal_catalog.searchResults(portal_type = 'Folder',
        #                                    path = path + '/documents')
        # if obj.actual_result_count == 0:                                
        #     documents = self.newFolder(portal, 'documents', u'Documents')
        #     documents.language = pl.getDefaultLanguage()
        #     documents.exclude_from_nav = True
        #     self.publish(documents)       
        #     documents.reindexObject()    

        # #Directori equipaments
        # obj = portal_catalog.searchResults(portal_type = 'Folder',
        #                                    path = path + '/directori-equipaments')
        # if obj.actual_result_count == 0:    
        #     directori_equipaments = self.newFolder(portal, 'directori-equipaments', u'Directori equipaments')
        #     directori_equipaments.language = pl.getDefaultLanguage()
        #     directori_equipaments.exclude_from_nav = True
        #     self.publish(directori_equipaments)       
        #     directori_equipaments.reindexObject()    

    
        # #Tràmits
        # obj = portal_catalog.searchResults(portal_type = 'Folder',
        #                                    path = path + '/tramits')
        # if obj.actual_result_count == 0:    
        #     tramits = self.newFolder(portal, 'tramits', u'Tràmits')
        #     tramits.language = pl.getDefaultLanguage()
        #     tramits.exclude_from_nav = True
        #     self.publish(tramits)       
        #     tramits.reindexObject()    

        #Categories
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/categories')
        if obj.actual_result_count == 0:    
            categories = self.newFolder(portal, 'categories', u'Categories')
            categories.language = pl.getDefaultLanguage()
            categories.exclude_from_nav = True
            self.publish(categories)       
            categories.reindexObject()   

        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(categories)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Categoria', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Categoria', 'Folder'))

        #Lleis
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/lleis')
        if obj.actual_result_count == 0:    
            lleis = self.newFolder(portal, 'lleis', u'Lleis')
            lleis.language = pl.getDefaultLanguage()
            lleis.exclude_from_nav = True
            self.publish(lleis)       
            lleis.reindexObject()          
  
        
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(lleis)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Llei', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Llei', 'Folder'))


        #Indicadors
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/indicadors')
        if obj.actual_result_count == 0:    
            indicadors = self.newFolder(portal, 'indicadors', u'Indicadors')
            indicadors.language = pl.getDefaultLanguage()
            indicadors.exclude_from_nav = True
            self.publish(indicadors)       
            indicadors.reindexObject()  
        
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(indicadors)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Indicador', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Indicador', 'Folder'))


        #Col·leccions Indicadors
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/col-leccions-indicadors')
        if obj.actual_result_count == 0:    
            coleccions_indicadors = self.newFolder(portal, 'col-leccions-indicadors', u'Col·leccions Indicadors')
            coleccions_indicadors.language = pl.getDefaultLanguage()
            coleccions_indicadors.exclude_from_nav = True
            self.publish(coleccions_indicadors)       
            coleccions_indicadors.reindexObject()      
        
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(coleccions_indicadors)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('Collection', 'Folder'))
        behavior.setImmediatelyAddableTypes(('Collection', 'Folder'))

        
              
                   
        return 'Created'
