import pytest

from prompts import facebook_prompt, instagram_prompt, tiktok_prompt


@pytest.mark.parametrize(
    "prompt_factory",
    [instagram_prompt, facebook_prompt, tiktok_prompt],
)
def test_english_language_instruction(prompt_factory):
    system, user = prompt_factory("Luna Coffee", "Oat milk latte")

    assert "exclusively in natural, fluent English" in system
    assert "exclusively in flawless, natural Azerbaijani" not in system
    assert "Language: flawless Azerbaijani only" not in user


def test_facebook_examples_are_in_english():
    _, user = facebook_prompt("Luna Coffee", "Latte")

    assert "This season’s most exciting choice is already here." in user


def test_tiktok_examples_are_in_english():
    _, user = tiktok_prompt("Narin Studio", "Necklace")

    assert "Everyone asked me where I got it" in user
