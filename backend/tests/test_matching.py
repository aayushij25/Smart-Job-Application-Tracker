import numpy as np
import pytest

from app.services import matching


def test_cosine_similarity():
    assert matching.cosine_similarity(np.array([1, 2, 3]), np.array([2, 4, 6])) == pytest.approx(1.0)
    assert matching.cosine_similarity(np.array([1, 0]), np.array([0, 1])) == pytest.approx(0.0)


def test_matrix_version_agrees_with_vector_version():
    a = np.array([[1.0, 2.0], [3.0, 1.0]])
    b = np.array([[2.0, 1.0]])
    assert matching.cosine_matrix(a, b)[1, 0] == pytest.approx(matching.cosine_similarity(a[1], b[0]))


def test_aliases_and_word_boundaries():
    assert matching.normalize_skill(" React.js ") == "react"
    assert matching.appears_in("react", "Built UIs with ReactJS")
    assert matching.appears_in("c++", "Experienced in C++ and Python")
    assert not matching.appears_in("java", "Expert in JavaScript")


def test_skill_coverage():
    matched, missing, coverage = matching.skill_coverage(
        ["Python", "Docker", "React.js"], "I use Python and React daily."
    )
    assert matched == ["python", "react"]
    assert missing == ["docker"]
    assert coverage == pytest.approx(2 / 3)


def test_combine():
    assert matching.combine(1.0, 0.0) == pytest.approx(0.6)
    assert matching.combine(0.5, None) == pytest.approx(0.5)