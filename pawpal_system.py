from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Owner:
    """Represents a pet owner with scheduling preferences."""
    name: str
    available_start: str = "08:00"   # earliest care time (HH:MM)
    available_end: str = "20:00"     # latest care time (HH:MM)
    preferred_walk_time: str = "morning"  # morning | afternoon | evening

    @property
    def available_minutes(self) -> int:
        """Return total minutes between available_start and available_end."""
        fmt = "%H:%M"
        start = datetime.strptime(self.available_start, fmt)
        end = datetime.strptime(self.available_end, fmt)
        return int((end - start).total_seconds() / 60)

    def __str__(self) -> str:
        """Return a human-readable summary of the owner."""
        return (
            f"Owner: {self.name} | Available {self.available_start}–{self.available_end} "
            f"| Prefers walks in the {self.preferred_walk_time}"
        )


@dataclass
class Pet:
    """Represents a pet with its basic info linked to an owner."""
    name: str
    species: str          # dog | cat | other
    breed: str
    age_years: float
    owner: Owner

    def needs_walk(self) -> bool:
        """Return True if the pet is a dog and requires daily walks."""
        return self.species == "dog"

    def __str__(self) -> str:
        """Return a human-readable summary of the pet."""
        return (
            f"Pet: {self.name} ({self.breed}, {self.species}, {self.age_years}yr) "
            f"— owned by {self.owner.name}"
        )


@dataclass
class CareTask:
    """Represents a single pet care task."""
    PRIORITIES = {"low": 1, "medium": 2, "high": 3}

    title: str
    duration_minutes: int
    priority: str = "medium"   # low | medium | high
    category: str = "general"  # feeding | walk | medication | grooming | enrichment | general
    notes: str = ""
    scheduled_time: Optional[str] = None   # set by DayScheduler (HH:MM)
    status: str = "pending"                # pending | complete
    frequency: str = "once"               # once | daily | weekly
    due_date: Optional[str] = None        # YYYY-MM-DD

    def mark_complete(self) -> None:
        """Set the task status to complete."""
        self.status = "complete"

    def next_occurrence(self) -> Optional["CareTask"]:
        """Return a new pending CareTask for the next recurrence, or None if one-time."""
        if self.frequency == "once" or self.due_date is None:
            return None
        days = 1 if self.frequency == "daily" else 7
        next_date = (
            datetime.strptime(self.due_date, "%Y-%m-%d") + timedelta(days=days)
        ).strftime("%Y-%m-%d")
        return CareTask(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            notes=self.notes,
            frequency=self.frequency,
            due_date=next_date,
        )

    @property
    def priority_value(self) -> int:
        """Return the numeric priority (1=low, 2=medium, 3=high)."""
        return self.PRIORITIES.get(self.priority, 1)

    def schedule_at(self, time_str: str) -> None:
        """Assign a scheduled start time (HH:MM) to this task."""
        self.scheduled_time = time_str

    def __str__(self) -> str:
        """Return a human-readable summary of the task."""
        time_part = f" @ {self.scheduled_time}" if self.scheduled_time else " (unscheduled)"
        return (
            f"[{self.priority.upper()}] {self.title} ({self.duration_minutes} min)"
            f"{time_part} — {self.category}"
        )


@dataclass
class DayScheduler:
    """Builds and stores a daily care schedule for a pet."""
    pet: Pet
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Append a CareTask to the scheduler's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """Remove a task by title and return True if it was found."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.title != title]
        return len(self.tasks) < before

    def build_schedule(self) -> list[CareTask]:
        """Sort tasks by priority (high first), then assign sequential time slots."""
        owner = self.pet.owner
        fmt = "%H:%M"
        current = datetime.strptime(owner.available_start, fmt)
        end = datetime.strptime(owner.available_end, fmt)

        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority_value, reverse=True)
        scheduled = []

        for task in sorted_tasks:
            slot_end = current + timedelta(minutes=task.duration_minutes)
            if slot_end <= end:
                task.schedule_at(current.strftime(fmt))
                current = slot_end
                scheduled.append(task)
            else:
                task.scheduled_time = None  # won't fit today

        return scheduled

    def view_day(self) -> str:
        """Return a formatted string of today's scheduled tasks."""
        scheduled = [t for t in self.tasks if t.scheduled_time]
        if not scheduled:
            return "No tasks scheduled yet. Run build_schedule() first."

        sorted_tasks = sorted(scheduled, key=lambda t: t.scheduled_time or "")
        lines = [
            f"Daily Schedule for {self.pet.name} ({self.pet.owner.name})",
            "=" * 50,
        ]
        total = 0
        for task in sorted_tasks:
            lines.append(str(task))
            total += task.duration_minutes

        lines.append("=" * 50)
        lines.append(f"Total care time: {total} min")
        return "\n".join(lines)

    def unscheduled_tasks(self) -> list[CareTask]:
        """Return tasks that have no scheduled time assigned."""
        return [t for t in self.tasks if not t.scheduled_time]

    def sort_by_time(self) -> list[CareTask]:
        """Return scheduled tasks sorted chronologically by start time (HH:MM)."""
        scheduled = [t for t in self.tasks if t.scheduled_time]
        return sorted(scheduled, key=lambda t: t.scheduled_time or "")

    def filter_tasks(
        self, status: Optional[str] = None, category: Optional[str] = None
    ) -> list[CareTask]:
        """Return tasks matching the given status and/or category filters."""
        result = self.tasks
        if status:
            result = [t for t in result if t.status == status]
        if category:
            result = [t for t in result if t.category == category]
        return result

    def complete_task(self, title: str) -> Optional[CareTask]:
        """Mark a task complete; if recurring, add and return its next occurrence."""
        for task in self.tasks:
            if task.title == title:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task:
                    self.tasks.append(next_task)
                return next_task
        return None

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any tasks whose time windows overlap."""
        scheduled = [t for t in self.tasks if t.scheduled_time]
        fmt = "%H:%M"
        warnings = []
        for i, a in enumerate(scheduled):
            for b in scheduled[i + 1:]:
                a_start = datetime.strptime(a.scheduled_time, fmt)  # type: ignore[arg-type]
                a_end = a_start + timedelta(minutes=a.duration_minutes)
                b_start = datetime.strptime(b.scheduled_time, fmt)  # type: ignore[arg-type]
                b_end = b_start + timedelta(minutes=b.duration_minutes)
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"CONFLICT: '{a.title}' ({a.scheduled_time}–{a_end.strftime(fmt)}) "
                        f"overlaps '{b.title}' ({b.scheduled_time}–{b_end.strftime(fmt)})"
                    )
        return warnings
