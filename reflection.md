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

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
