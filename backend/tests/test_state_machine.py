from app.models.enums import ApplicationStatus as S
from app.services.application_service import ALLOWED_TRANSITIONS

def test_every_status_has_an_entry():
    assert set(ALLOWED_TRANSITIONS) == set(S)

def test_final_states_have_no_exists():
    assert ALLOWED_TRANSITIONS[S.OFFER] == set()
    assert ALLOWED_TRANSITIONS[S.REJECTED] == set()