# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from plone.folder.interfaces import IExplicitOrdering
from Acquisition import aq_inner


def orderable(self):
    if IPloneSiteRoot.providedBy(self.context):
        return True
    ordering = self.context.getOrdering()
    return IExplicitOrdering.providedBy(ordering)


def contentsMethod(self):
    context = aq_inner(self.context)
    contentsMethod = context.getFolderContents
    return contentsMethod
