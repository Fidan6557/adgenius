import pytest

from prompts import facebook_prompt, instagram_prompt, tiktok_prompt


@pytest.mark.parametrize(
    "prompt_factory",
    [instagram_prompt, facebook_prompt, tiktok_prompt],
)
def test_azerbaijani_language_instruction(prompt_factory):
    system, _ = prompt_factory("Luna Coffee", "Yulaf südlü latte", "az")

    assert "exclusively in flawless, natural Azerbaijani" in system
    assert "Do not use Turkish words" in system


@pytest.mark.parametrize(
    "prompt_factory",
    [instagram_prompt, facebook_prompt, tiktok_prompt],
)
def test_english_language_instruction(prompt_factory):
    system, user = prompt_factory("Luna Coffee", "Oat milk latte", "en")

    assert "exclusively in natural, fluent English" in system
    assert "exclusively in flawless, natural Azerbaijani" not in system
    assert "Language: flawless Azerbaijani only" not in user


def test_facebook_examples_follow_selected_language():
    _, az_user = facebook_prompt("Luna Coffee", "Latte", "az")
    _, en_user = facebook_prompt("Luna Coffee", "Latte", "en")

    assert "Bu yazın ən gözəl seçimi artıq burada." in az_user
    assert "This season’s most exciting choice is already here." in en_user
    assert "Bu yazın ən gözəl seçimi artıq burada." not in en_user


def test_tiktok_examples_follow_selected_language():
    _, az_user = tiktok_prompt("Narin Studio", "Boyunbağı", "az")
    _, en_user = tiktok_prompt("Narin Studio", "Necklace", "en")

    assert "Hamı məndən soruşdu haradan aldım" in az_user
    assert "Everyone asked me where I got it" in en_user
    assert "Hamı məndən soruşdu haradan aldım" not in en_user
