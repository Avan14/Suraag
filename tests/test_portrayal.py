"""Rule R-04 (part): every page points real victims to the national helpline and portal, in both languages."""
from suraag.i18n import EN, HI


def test_learner_page_links_1930_and_cybercrime_portal():
    for table in (EN, HI):
        footer = table["ui.footer"].format(portal="cybercrime.gov.in")
        assert "1930" in footer and "cybercrime.gov.in" in footer
