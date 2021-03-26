import json
import pytest


@pytest.fixture
def real_text_example(example):
    assert example in ["example1", "example2"]

    with open(f"typographie/tests/fixtures/{example}.json") as f:
        example = json.load(f)

    return example
