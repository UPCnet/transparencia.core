# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.site import ISiteSchema

from Products.CMFPlone.utils import _createObjectByType

import logging
import transaction
import pkg_resources

from genweb.core.interfaces import IHomePage
from zope.component.hooks import getSite

from zope.interface import alsoProvides 
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs

from datetime import datetime
from plone.dexterity.utils import createContentInContainer

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True
    from plone.dexterity.utils import createContentInContainer

def createOrGetObject(context, newid, title, type_name):
    if newid in context.contentIds():
        obj = context[newid]
    else:
        obj = createContentInContainer(context, type_name, title=title, checkConstrains=False)
        transaction.savepoint()
        if obj.id != newid:
            context.manage_renameObject(obj.id, newid)
        obj.reindexObject()
    return obj

def newCollection(context, newid, title, query=None):
    collection = createOrGetObject(context, newid, title, u'Collection')
    if query is not None:            
        collection.query = query
        collection.reindexObject()
    return collection

def newFolder(context, newid, title, type_name=u'Folder'):
    return createOrGetObject(context, newid, title, type_name)


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('transparencia.core_various.txt') is None:
        return

    # Add additional setup code here
    #
    # portal = context.getSite()
    # logger = logging.getLogger(__name__)
    # transforms = getToolByName(portal, 'portal_transforms')
    # transform = getattr(transforms, 'safe_html')
    # valid = transform.get_parameter_value('valid_tags')
    # nasty = transform.get_parameter_value('nasty_tags')
    #import ipdb; ipdb.set_trace()

    
    portal = context.getSite()
    
    # Delete old AT folders
    if getattr(portal, 'events', None):
        if portal.events.__class__.__name__ == 'Folder':
            portal.manage_delObjects(['events'])

    if getattr(portal, 'news', None):
        if portal.news.__class__.__name__ == 'Folder':
            portal.manage_delObjects(['news'])

    if getattr(portal, 'Members', None):
        if portal.Members.__class__.__name__ == 'ATFolder':
            portal.manage_delObjects(['Members'])

    # if getattr(portal, 'front-page', None):
    #     if portal['front-page'].__class__.__name__ == 'ATDocument':

    #         portal.manage_delObjects(['front-page'])

    urltool = getToolByName(portal, 'portal_url')
    portal_catalog = getToolByName(portal, 'portal_catalog')
    path = urltool.getPortalPath() 

   
    if HAS_DXCT:       
        portal = getSite()
        pl = getToolByName(portal, 'portal_languages')
        workflowTool = getToolByName(portal, "portal_workflow")   
        if getattr(portal, 'front-page', False):
            portal.manage_delObjects('front-page')
            frontpage = createContentInContainer(portal, 'Document', title=u"front-page", checkConstraints=False)
            alsoProvides(frontpage, IHomePage)
            frontpage.exclude_from_nav = True
            frontpage.language = pl.getDefaultLanguage()
            workflowTool.doActionFor(frontpage, "publish")
            frontpage.reindexObject()
        # Set the default page to the homepage view
        portal.setDefaultPage('homepage')             
    else:
        return 'This site has no p.a.contenttypes installed.'
        
    transaction.commit()   