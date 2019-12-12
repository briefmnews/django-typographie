import pytest

from ..filters import spaces, smartypants, exponent, indice
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


class TestTypographieSmartyPants(object):
    def test_replace_quotes(self):
        text = '"test"'
        assert smartypants(text) == "\xabtest\xbb"


class TestTypographieExponent:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("1<sup>er</sup> to see", "1<sup>er</sup>\u00a0to see"),
            ("I<sup>er</sup> to see", "I<sup>er</sup>\u00a0to see"),
            ("1er to see", "1<sup>er</sup>\u00a0to see"),
            ("2nd to see", "2<sup>nd</sup>\u00a0to see"),
            ("XIXe to see", "XIX<sup>e</sup>\u00a0to see"),
        ],
    )
    def test_exponent(self, text, expected):
        assert exponent(text) == expected


class TestTypographieIndice:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("CO2", "CO<sub>2</sub>"),
            (" CO2 ", " CO<sub>2</sub> "),
            ("https://www.lemonde.fr/du-CO2", "https://www.lemonde.fr/du-CO2"),
            ("https://www.lemonde.fr/du-CO2 ", "https://www.lemonde.fr/du-CO2 "),
        ],
    )
    def test_indice(self, text, expected):
        assert indice(text) == expected
