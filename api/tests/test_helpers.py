from ..helpers import serialize_bdd_object
from ..models import Episodes


def test_serialize_bdd_object(
    setup, db_manager, expected_episode1_without_relation_dict
):
    session = db_manager.get_session()
    episode = session.query(Episodes).filter(Episodes.id == 1).first()
    assert serialize_bdd_object(episode) == expected_episode1_without_relation_dict
