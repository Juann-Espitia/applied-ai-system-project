# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design is organized around three core concerns: who is involved (owner and pet), what needs to happen (tasks), and how to plan the day (scheduler). The diagram uses four classes connected by ownership and composition relationships. `Owner` connects to `Pet`, `Pet` connects to `DayScheduler`, and `DayScheduler` aggregates many `CareTask` objects. This gave me a clear separation between data (owner/pet info), work items (tasks), and logic (scheduling).

- What classes did you include, and what responsibilities did you assign to each?

I ended up with four classes instead of three:

1. **`Owner`** — stores the owner's name, daily availability window (start and end time), and preferred walk time. It also computes how many total minutes are available in a day, which the scheduler uses to fit tasks.

2. **`Pet`** — stores the pet's name, species, breed, and age, and holds a reference to its `Owner`. It also has a `needs_walk()` helper that returns `True` for dogs, making it easy to apply species-specific logic later.

3. **`CareTask`** — represents a single care activity (walk, feeding, medication, grooming, etc.) with a title, duration in minutes, priority level (low/medium/high), category, and optional notes. It holds a `scheduled_time` field that gets set once the scheduler assigns it a slot.

4. **`DayScheduler`** — the central coordinator. It holds a reference to the `Pet` (and through it the `Owner`) and manages a list of `CareTask` objects. It exposes `add_task()`, `remove_task()`, `build_schedule()` (which sorts by priority and assigns sequential time slots), and `view_day()` (which prints the final agenda).

**b. Design changes**

- Did your design change during implementation? None
- If yes, describe at least one change and why you made it. N/A

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
