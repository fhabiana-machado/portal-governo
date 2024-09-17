from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from portal.governo.content.pessoa import Pessoa
from zope.component import createObject

import pytest


CONTENT_TYPE = "Pessoa"


@pytest.fixture
def payload() -> dict:
    """Return a payload to create a new pessoa."""
    return {
        "type": "Pessoa",
        "id": "artur-lemos",
        "title": "Artur Lemos",
        "description": (
            "Advogado formado pela Pontifícia Universidade Católica do "
            "Rio Grande do Sul (PUCRS), tem especialização em Direito do Trabalho "
            "e Processual do Trabalho"
        ),
        "email": "gabinete@casacivil.rs.gov.br",
        "telefone": "5132104193",
    }


@pytest.fixture()
def content(portal, payload) -> Pessoa:
    with api.env.adopt_roles(["Manager"]):
        content = api.content.create(container=portal, **payload)
    return content


class TestPessoa:
    @pytest.fixture(autouse=True)
    def _setup(self, get_fti, portal):
        self.fti = get_fti(CONTENT_TYPE)
        self.portal = portal

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Pessoa)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
            "plone.leadimage",
            "portal.governo.behavior.contato",
            "portal.governo.behavior.endereco",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "role,allowed",
        [
            ["Manager", True],
            ["Site Administrator", True],
            ["Editor", True],
            ["Contributor", True],
        ],
    )
    def test_create(self, payload, role, allowed):
        with api.env.adopt_roles([role]):
            if allowed:
                content = api.content.create(container=self.portal, **payload)
                assert content.portal_type == CONTENT_TYPE
                assert isinstance(content, Pessoa)
            else:
                with pytest.raises(Unauthorized):
                    api.content.create(container=self.portal, **payload)
