from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IPessoa(model.Schema):
    """Definição de uma pessoa do governo."""


@implementer(IPessoa)
class Pessoa(Container):
    """Uma pessoa do governo"""
