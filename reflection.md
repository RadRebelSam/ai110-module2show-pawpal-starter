# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The core design of PawPal+ focuses on three actions the user should be able to perform easily:
1. The user should enter basic owner and pet information so the system can understand context, such as preferences and available time.
2. The user should add and manage pet care tasks (like walks, feeding, meds, enrichment, and grooming) with key details such as duration and priority.
3. The user should generate and review a daily plan that schedules tasks based on constraints and priorities, with a clear explanation of why the plan was chosen.

Building Blocks
1. PetOwner
   Attributes: name, daily_time_available, preferences (morning/evening, avoid late walks), contact_info (optional)
   Methods: update_preferences(), set_time_available(), get_constraints()
2. Pet
   Attributes: name, species, age, weight (optional), special_needs (diet/medical), energy_level
   Methods: update_profile(), add_special_need(), remove_special_need()
3. CareTask
   Attributes: title (Walk, Feed, Meds), category, duration_minutes, priority, due_window (morning/afternoon/evening), frequency, is_completed
   Methods: mark_complete(), mark_incomplete(), update_priority(), update_duration(), fits_time_window()
4. TaskList (or TaskManager)
   Attributes: tasks (list of CareTask)
   Methods: add_task(), edit_task(), delete_task(), get_pending_tasks(), sort_by_priority(), filter_by_category()
5. ConstraintSet (or SchedulerConstraints)
   Attributes: time_available, owner_preferences, must_do_tasks, max_tasks_per_day (optional)
   Methods: validate_task(task), is_feasible(task), score_task(task)
6. Scheduler
   Attributes: constraints, task_manager, planning_date
   Methods: generate_daily_plan(), rank_tasks(), resolve_conflicts(), explain_selection(task)
7. DailyPlan
   Attributes: date, scheduled_items (task + time slot), unscheduled_items, total_time_used
   Methods: add_scheduled_task(), remove_task(), get_summary(), get_reasoning()
8. PawPalApp (controller/UI bridge)
   Attributes: owner, pet, task_manager, scheduler, current_plan
   Methods: collect_user_input(), save_task_changes(), build_plan(), display_plan()

For my initial UML design, I separated the system into classes with clear responsibilities so each part of PawPal+ had one main job. PetOwner stores owner context (available time and preferences), and Pet stores pet-specific details (species, age, needs). CareTask represents one care activity with scheduling properties like duration, priority, and due window.

I used TaskManager to handle task collection operations (add, edit, remove, filter, and sort), and ConstraintSet to represent planning limits such as total available time, preferences, and must-do tasks. The Scheduler is the core decision-making class that ranks tasks, resolves conflicts, and builds a feasible daily schedule. The output is stored in DailyPlan, which keeps scheduled vs. unscheduled tasks and summary/reasoning information. Finally, PawPalApp acts as the controller between the UI and backend logic by collecting input, triggering scheduling, and displaying results.

This structure helped me keep data modeling, scheduling logic, and UI coordination separated, making the system easier to test and extend.

**b. Design changes**

Yes, my design changed during implementation. I initially planned separate classes like `TaskManager`, `ConstraintSet`, and `DailyPlan`, but for this scope I merged most of that behavior into `Owner` and `Scheduler` to keep the code compact and easy to test. The biggest practical change was introducing `time_of_day`, `last_completed_on`, and recurrence helper methods directly on `Task`, because that made sorting, due checks, and recurring task generation much cleaner than scattering date/time logic across multiple controller-style classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler currently focuses on constraints that are easy for a pet owner to understand and verify:

- Task time (`time_of_day`) for chronological planning.
- Completion status (pending vs completed) for what should appear in active views.
- Frequency (`daily`, `weekly`, `monthly`) and `last_completed_on` for due-task behavior.
- Multi-pet filtering, so an owner can focus on one pet or view all pets together.

I prioritized these constraints because they directly affect daily execution: "What do I need to do next, and for which pet?" Advanced preference scoring was intentionally deferred to keep the baseline scheduler reliable and debuggable first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler currently uses a lightweight conflict strategy that checks for exact `HH:MM` matches only, instead of checking full overlap windows based on each task's duration. This means it can quickly warn about obvious collisions without adding much complexity to the starter project, but it may miss partial overlaps (for example, a 07:30 task lasting 30 minutes and a 07:45 task). For this scenario, that tradeoff is reasonable because it keeps runtime logic simple, transparent, and easy to explain while still catching common same-time conflicts across one or multiple pets.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI as a coding copilot in three phases: design translation, implementation acceleration, and test hardening. During design, AI helped convert my UML intent into concrete class methods with typed signatures. During implementation, it was most useful for drafting small algorithmic methods (sorting, filtering, due checks, warning generation). During testing, AI helped propose concise test cases for happy paths and edge cases without overcomplicating fixtures.

The most helpful prompts were specific and constraint-based, for example:
- "Add a scheduler method that sorts `Task` objects by `HH:MM` string time."
- "Create a lightweight conflict warning strategy that does not throw exceptions."
- "Write tests for daily recurrence creation and duplicate-time warnings."

**b. Judgment and verification**

One Copilot-style suggestion I rejected was a heavier conflict detector that tried to model full overlap windows, buffers, and optimization rules in one step. I modified it to a simpler exact-time warning strategy because it matched project scope and kept behavior explainable for users.

I verified each accepted suggestion by:
- Running `python -m pytest` after each meaningful change.
- Running `main.py` to inspect terminal behavior and warning messages.
- Checking that Streamlit output remained user-friendly and did not expose confusing internal details.

Using separate chat sessions for different phases (design, backend logic, UI polish, tests/docs) helped me stay organized by reducing context switching. Each session had a clear objective and acceptance criteria.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion status changes, task list mutation, chronological sorting, filtering by pet/status, due-task calculation, overlap detection, duplicate-time warning detection, recurrence auto-creation, and empty-task edge behavior.

These tests were important because they cover the core promises of the app: producing a usable schedule, handling recurring care reliably, and warning users about schedule risk without crashing.

**b. Confidence**

I am confident that the scheduler is reliable for the implemented scope (about 4/5 confidence), based on passing automated tests and manual verification in terminal and UI.

If I had more time, I would test:
- Invalid time formats entered by users and validation feedback.
- Very large task sets across many pets for performance and readability.
- Exact-time warnings combined with duration-overlap checks to reduce false negatives.
- Recurrence behavior across actual dates/time zones and month boundaries.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the end-to-end consistency between backend logic, tests, and UI presentation. The scheduler methods are now directly reflected in the interface, so users can see the value of the algorithms instead of just storing data.

**b. What you would improve**

In another iteration, I would add stronger input validation (especially time input widgets), richer recurrence rules, and a clearer state model for task instances vs task templates. I would also unify some overlapping scheduler methods to simplify the public API.

**c. Key takeaway**

My key takeaway is that AI is most effective when I stay the lead architect: define boundaries first, ask focused prompts, and verify continuously with tests. AI can accelerate implementation, but system clarity and quality still depend on deliberate human design decisions.

---

## Prompt Comparison (Multi-Model)

For a complex task (rescheduling weekly tasks after completion), I compared responses from two model styles: one OpenAI-style response and one Claude/Gemini-style response.

- The OpenAI-style output was more modular and Pythonic for this project: it proposed a focused method (`create_next_occurrence`) and clean integration inside `Scheduler.complete_task`, with clear boundaries between data behavior and scheduling behavior.
- The Claude/Gemini-style output explored more alternatives and edge-case branches, which was useful for brainstorming, but initially introduced more abstraction than needed for the starter scope.

I chose the modular approach because it preserved readability and testability while still supporting recurrence behavior.
