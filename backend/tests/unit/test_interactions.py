"""Unit tests for interaction filtering logic."""

from datetime import datetime

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(
        id=id,
        learner_id=learner_id,
        item_id=item_id,
        kind="attempt",
        created_at=datetime.now(),
    )


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_matches_on_item_id_and_ignores_learner_id() -> None:
    interaction = _make_log(id=1, learner_id=2, item_id=1)
    result = _filter_by_item_id([interaction], 1)
    assert len(result) == 1
    assert result[0].id == interaction.id
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_returns_multiple_matching_interactions() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


def test_filter_returns_mixed_results() -> None:
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 1),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_returns_empty_when_no_match() -> None:
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 3)]
    result = _filter_by_item_id(interactions, 1)
    assert result == []


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interaction = _make_log(id=1, learner_id=2, item_id=1)
    result = _filter_by_item_id([interaction], 1)
    assert len(result) == 1
    assert result[0].id == interaction.id



