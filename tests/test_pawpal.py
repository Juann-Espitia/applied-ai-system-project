import pytest
from pawpal_system import Owner, Pet, CareTask, DayScheduler


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def owner():
    return Owner(name="Jordan", available_start="08:00", available_end="20:00")


@pytest.fixture
def pet(owner):
    return Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3.0, owner=owner)


@pytest.fixture
def scheduler(pet):
    return DayScheduler(pet=pet)


# ── CareTask: mark_complete ───────────────────────────────────────────────────

def test_task_starts_as_pending():
    task = CareTask(title="Morning walk", duration_minutes=30)
    assert task.status == "pending"


def test_mark_complete_changes_status():
    task = CareTask(title="Morning walk", duration_minutes=30)
    task.mark_complete()
    assert task.status == "complete"


def test_mark_complete_is_idempotent():
    task = CareTask(title="Feeding", duration_minutes=10)
    task.mark_complete()
    task.mark_complete()
    assert task.status == "complete"


# ── DayScheduler: task count ──────────────────────────────────────────────────

def test_scheduler_starts_empty(scheduler):
    assert len(scheduler.tasks) == 0


def test_adding_task_increases_count(scheduler):
    scheduler.add_task(CareTask(title="Walk", duration_minutes=30))
    assert len(scheduler.tasks) == 1


def test_adding_multiple_tasks_increases_count(scheduler):
    scheduler.add_task(CareTask(title="Walk",    duration_minutes=30))
    scheduler.add_task(CareTask(title="Feeding", duration_minutes=10))
    scheduler.add_task(CareTask(title="Meds",    duration_minutes=5))
    assert len(scheduler.tasks) == 3


def test_removing_task_decreases_count(scheduler):
    scheduler.add_task(CareTask(title="Walk", duration_minutes=30))
    scheduler.add_task(CareTask(title="Feeding", duration_minutes=10))
    scheduler.remove_task("Walk")
    assert len(scheduler.tasks) == 1


def test_removing_nonexistent_task_returns_false(scheduler):
    scheduler.add_task(CareTask(title="Walk", duration_minutes=30))
    result = scheduler.remove_task("Grooming")
    assert result is False
    assert len(scheduler.tasks) == 1
