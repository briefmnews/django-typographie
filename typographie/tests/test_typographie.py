import pytest

from ..filters import spaces, smartypants
from ..typographie import typographie


class TestTypographieSpaces:
    def test_div(self):
        text = "<div>un test : test</div>"
        assert spaces(text) == "<div>un test\xa0: test</div>"

    def test_column(self):
        text = "un test : test"
        assert spaces(text) == "un test\xa0: test"

    def test_column_with_tags(self):
        text = '<a href="">un test</a> : test'
        assert spaces(text) == '<a href="">un test</a>\xa0: test'

    def test_semi_column(self):
        text = "un test ; test"
        assert spaces(text) == "un test\xa0; test"

    def test_semi_column_with_tags(self):
        text = '<a href="">un test</a> ; test'
        assert spaces(text) == '<a href="">un test</a>\xa0; test'

    def test_exclamation_mark(self):
        text = "un test ! test"
        assert spaces(text) == "un test\xa0! test"

    def test_exclamation_mark_with_tags(self):
        text = '<a href="">un test</a> ! test'
        assert spaces(text) == '<a href="">un test</a>\xa0! test'

    def test_interrogation_mark(self):
        text = "un test ! test"
        assert spaces(text) == "un test\xa0! test"

    def test_interrogation_mark_with_tags(self):
        text = '<a href="">un test</a> ? test'
        assert spaces(text) == '<a href="">un test</a>\xa0? test'

    def test_closing_quotation_mark_with_period(self):
        text = "\xabtest\xbb."
        assert spaces(text) == "\xab\xa0test\xa0\xbb."

    def test_quotation_mark_with_quote(self):
        text = "\xabactualité\xbb</a>."
        assert spaces(text) == "\xab\xa0actualité\xa0\xbb</a>."

    def test_with_quote(self):
        text = "<strong>\xabtest\xbb</strong>."
        assert spaces(text) == "<strong>\xab\xa0test\xa0\xbb</strong>."

    def test_nonbreakable_after_digit(self):
        text = "10 personnes"
        assert spaces(text) == "10\xa0personnes"

    def test_nonbreakable_between_digits(self):
        text = "10 000"
        assert spaces(text) == "10\xa0000"

    def test_nonbreakable_between_digit_percent(self):
        text = "10%"
        assert spaces(text) == "10\xa0%"
        text = "10 %"
        assert spaces(text) == "10\xa0%"

    def test_ampersand(self):
        text = "To test with an ampersand h&m for example"

        assert spaces(text) == "To test with an ampersand h&m for example"

    def test_date_comma_percentage(self):
        text = "En 2018, 51% de la population"
        assert spaces(text) == "En 2018, 51\xa0% de la population"

    def test_percentage_with_comma(self):
        text = "On compte 61,4% de la population"
        assert spaces(text) == "On compte 61,4\xa0% de la population"


class TestTypographieCbReContentBetweenTags:
    @pytest.mark.parametrize(
        "text, expected",
        [("En 2018, 51% de la population", "En 2018, 51\xa0% de la population")],
    )
    def test_cb_re_content_between_tags(self, text, expected):
        assert typographie(text) == expected

    @pytest.mark.parametrize(
        "text, expected",
        [
            ("Le 1er to see", "Le 1<sup>er</sup> to see"),
            ("Le 3e to see", "Le 3<sup>e</sup>\xa0to see"),
            ("1er du nom", "1<sup>er</sup> du nom"),
            ("99e fois", "99<sup>e</sup>\xa0fois"),
            ("999e fois", "999<sup>e</sup>\xa0fois"),
            ("Le Ier to see", "Le I<sup>er</sup> to see"),
            ("Ier arrondissement", "I<sup>er</sup> arrondissement"),
            ("https://www.lemonde.fr/du-Ier", "https://www.lemonde.fr/du-Ier"),
            ("Le XIXe to see", "Le XIX<sup>e</sup>\xa0to see"),
            ("Le VIe arrondissement", "Le VI<sup>e</sup>\xa0arrondissement"),
            ("Le XXIe siècle", "Le XXI<sup>e</sup>\xa0siècle"),
            ("Le XXIe, siècle", "Le XXI<sup>e</sup>, siècle"),
            ("Le XVIIIe, siècle", "Le XVIII<sup>e</sup>, siècle"),
            ("999e, fois", "999<sup>e</sup>, fois"),
            ("e tout seul", "e tout seul"),
            ("e, tout seul", "e, tout seul"),
            ("Veux-tu ?", "Veux-tu\xa0?"),
            (
                "<a title='Le 26e rapport'>Ceci est une 26e rapport</a>",
                "<a title='Le 26e rapport'>Ceci est une 26<sup>e</sup>\xa0rapport</a>",
            ),
        ],
    )
    def test_exponent(self, text, expected):
        assert typographie(text) == expected

    @pytest.mark.parametrize(
        "text, expected",
        [
            ("CO2", "CO<sub>2</sub>"),
            ("CO2,", "CO<sub>2</sub>,"),
            ("Le CO2 test", "Le CO<sub>2</sub>\xa0test"),
            ("https://www.lemonde.fr/du-CO2", "https://www.lemonde.fr/du-CO2"),
            ("CO2</strong>", "CO<sub>2</sub></strong>"),
            ("(CO2)", "(CO<sub>2</sub>)"),
        ],
    )
    def test_indice(self, text, expected):
        assert typographie(text) == expected

    @pytest.mark.parametrize(
        "text, expected",
        [
            ("m2", "m<sup>2</sup>"),
            ("m2)", "m<sup>2</sup>)"),
            ("km2", "km<sup>2</sup>"),
            ("m3", "m<sup>3</sup>"),
            ("Un volume de 23 m3,", "Un volume de 23\xa0m<sup>3</sup>,"),
            ("m22", "m22"),
            (
                "Un espace de 34 m2 de surface",
                "Un espace de 34\xa0m<sup>2</sup>\xa0de surface",
            ),
        ],
    )
    def test_metric(self, text, expected):
        assert typographie(text) == expected


class TestTypographieSmartyPants(object):
    def test_replace_quotes(self):
        text = '"test"'
        assert smartypants(text) == "\xabtest\xbb"
