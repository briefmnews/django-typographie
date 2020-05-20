import pytest

from ..filters import spaces, smartypants, exponent, indice, metric


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


class TestTypographieSmartyPants(object):
    def test_replace_quotes(self):
        text = '"test"'
        assert smartypants(text) == "\xabtest\xbb"


class TestTypographieExponent:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("Le 1er to see", "Le 1<sup>er</sup> to see"),
            ("Le 3e to see", "Le 3<sup>e</sup> to see"),
            ("1er du nom", "1<sup>er</sup> du nom"),
            ("99e fois", "99<sup>e</sup> fois"),
            ("999e fois", "999<sup>e</sup> fois"),
            ("Le Ier to see", "Le I<sup>er</sup> to see"),
            ("Ier arrondissement", "I<sup>er</sup> arrondissement"),
            ("https://www.lemonde.fr/du-Ier", "https://www.lemonde.fr/du-Ier"),
            ("Le XIXe to see", "Le XIX<sup>e</sup> to see"),
            ("Le VIe arrondissement", "Le VI<sup>e</sup> arrondissement"),
            ("Le XXIe siècle", "Le XXI<sup>e</sup> siècle"),
            ("Le XXIe, siècle", "Le XXI<sup>e</sup>, siècle"),
            ("999e, fois", "999<sup>e</sup>, fois"),
            ("e tout seul", "e tout seul"),
            ("e, tout seul", "e, tout seul"),
            ("Veux-tu ?", "Veux-tu ?"),
        ],
    )
    def test_exponent(self, text, expected):
        assert exponent(text) == expected


class TestTypographieIndice:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("CO2", "CO<sub>2</sub>"),
            ("CO2,", "CO<sub>2</sub>,"),
            (" CO2 ", " CO<sub>2</sub> "),
            ("https://www.lemonde.fr/du-CO2", "https://www.lemonde.fr/du-CO2"),
            ("https://www.lemonde.fr/du-CO2 ", "https://www.lemonde.fr/du-CO2 "),
        ],
    )
    def test_indice(self, text, expected):
        assert indice(text) == expected


class TestTypographieMetric:
    @pytest.mark.parametrize(
        "text, expected",
        [
            (" m2", " m<sup>2</sup>"),
            (" km2", " km<sup>2</sup>"),
            (" m3", " m<sup>3</sup>"),
            (" m3,", " m<sup>3</sup>,"),
            (" m22", " m22"),
        ],
    )
    def test_metric(self, text, expected):
        assert metric(text) == expected
