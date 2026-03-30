from pawpal_system import Owner, Pet, CareTask, DayScheduler

# ── Owner ─────────────────────────────────────────────────────────────────────
jordan = Owner(
    name="Jordan",
    available_start="08:00",
    available_end="20:00",
    preferred_walk_time="morning",
)

print(jordan)
print(f"Available minutes today: {jordan.available_minutes}\n")

# ── Pets ──────────────────────────────────────────────────────────────────────
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3.0, owner=jordan)
luna  = Pet(name="Luna",  species="cat", breed="Siamese",   age_years=5.0, owner=jordan)

print(mochi)
print(f"  Needs walk: {mochi.needs_walk()}")
print(luna)
print(f"  Needs walk: {luna.needs_walk()}\n")

# ── Scheduler for Mochi ───────────────────────────────────────────────────────
mochi_scheduler = DayScheduler(pet=mochi)

mochi_scheduler.add_task(CareTask(
    title="Morning walk",
    duration_minutes=30,
    priority="high",
    category="walk",
    notes="Around the park",
))
mochi_scheduler.add_task(CareTask(
    title="Breakfast feeding",
    duration_minutes=10,
    priority="high",
    category="feeding",
))
mochi_scheduler.add_task(CareTask(
    title="Flea medication",
    duration_minutes=5,
    priority="medium",
    category="medication",
    notes="Monthly dose",
))
mochi_scheduler.add_task(CareTask(
    title="Playtime / enrichment",
    duration_minutes=20,
    priority="low",
    category="enrichment",
))

# ── Scheduler for Luna ────────────────────────────────────────────────────────
luna_scheduler = DayScheduler(pet=luna)

luna_scheduler.add_task(CareTask(
    title="Breakfast feeding",
    duration_minutes=10,
    priority="high",
    category="feeding",
))
luna_scheduler.add_task(CareTask(
    title="Brush coat",
    duration_minutes=15,
    priority="medium",
    category="grooming",
))
luna_scheduler.add_task(CareTask(
    title="Evening play",
    duration_minutes=20,
    priority="low",
    category="enrichment",
))

# ── Build & print schedules ───────────────────────────────────────────────────
mochi_scheduler.build_schedule()
luna_scheduler.build_schedule()

print("=" * 50)
print(mochi_scheduler.view_day())

unscheduled = mochi_scheduler.unscheduled_tasks()
if unscheduled:
    print(f"\nDid not fit: {', '.join(t.title for t in unscheduled)}")

print()
print("=" * 50)
print(luna_scheduler.view_day())

unscheduled = luna_scheduler.unscheduled_tasks()
if unscheduled:
    print(f"\nDid not fit: {', '.join(t.title for t in unscheduled)}")
