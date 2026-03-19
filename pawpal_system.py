"""PawPal+ logic layer class skeletons.

This module contains backend classes and method stubs based on the UML design.
"""

from __future__ import annotations


class PetOwner:
    def __init__(
        self,
        name: str,
        daily_time_available: int = 0,
        preferences: list[str] | None = None,
        contact_info: str = "",
    ) -> None:
        self.name = name
        self.daily_time_available = daily_time_available
        self.preferences = preferences or []
        self.contact_info = contact_info

    def update_preferences(self, preferences: list[str]) -> None:
        pass

    def set_time_available(self, minutes: int) -> None:
        pass

    def get_constraints(self) -> "ConstraintSet":
        pass


class Pet:
    def __init__(
        self,
        name: str,
        species: str,
        age: int = 0,
        weight: float = 0.0,
        special_needs: list[str] | None = None,
        energy_level: str = "",
    ) -> None:
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.special_needs = special_needs or []
        self.energy_level = energy_level

    def update_profile(self, name: str, species: str, age: int, weight: float) -> None:
        pass

    def add_special_need(self, need: str) -> None:
        pass

    def remove_special_need(self, need: str) -> None:
        pass


class CareTask:
    def __init__(
        self,
        title: str,
        category: str,
        duration_minutes: int = 0,
        priority: int = 0,
        due_window: str = "",
        frequency: str = "",
        is_completed: bool = False,
    ) -> None:
        self.title = title
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.due_window = due_window
        self.frequency = frequency
        self.is_completed = is_completed

    def mark_complete(self) -> None:
        pass

    def mark_incomplete(self) -> None:
        pass

    def update_priority(self, priority: int) -> None:
        pass

    def update_duration(self, minutes: int) -> None:
        pass

    def fits_time_window(self, window: str) -> bool:
        pass


class TaskManager:
    def __init__(self, tasks: list[CareTask] | None = None) -> None:
        self.tasks = tasks or []

    def add_task(self, task: CareTask) -> None:
        pass

    def edit_task(self, task_id: str, updates: dict) -> None:
        pass

    def delete_task(self, task_id: str) -> None:
        pass

    def get_pending_tasks(self) -> list[CareTask]:
        pass

    def sort_by_priority(self) -> list[CareTask]:
        pass

    def filter_by_category(self, category: str) -> list[CareTask]:
        pass


class ConstraintSet:
    def __init__(
        self,
        time_available: int = 0,
        owner_preferences: list[str] | None = None,
        must_do_tasks: list[CareTask] | None = None,
        max_tasks_per_day: int = 0,
    ) -> None:
        self.time_available = time_available
        self.owner_preferences = owner_preferences or []
        self.must_do_tasks = must_do_tasks or []
        self.max_tasks_per_day = max_tasks_per_day

    def validate_task(self, task: CareTask) -> bool:
        pass

    def is_feasible(self, task: CareTask) -> bool:
        pass

    def score_task(self, task: CareTask) -> float:
        pass


class Scheduler:
    def __init__(
        self,
        constraints: ConstraintSet,
        task_manager: TaskManager,
        planning_date: str = "",
    ) -> None:
        self.constraints = constraints
        self.task_manager = task_manager
        self.planning_date = planning_date

    def generate_daily_plan(self) -> "DailyPlan":
        pass

    def rank_tasks(self) -> list[CareTask]:
        pass

    def resolve_conflicts(self, tasks: list[CareTask]) -> list[CareTask]:
        pass

    def explain_selection(self, task: CareTask) -> str:
        pass


class DailyPlan:
    def __init__(
        self,
        date: str,
        scheduled_items: list[CareTask] | None = None,
        unscheduled_items: list[CareTask] | None = None,
        total_time_used: int = 0,
    ) -> None:
        self.date = date
        self.scheduled_items = scheduled_items or []
        self.unscheduled_items = unscheduled_items or []
        self.total_time_used = total_time_used

    def add_scheduled_task(self, task: CareTask) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_summary(self) -> str:
        pass

    def get_reasoning(self) -> str:
        pass


class PawPalApp:
    def __init__(
        self,
        owner: PetOwner,
        pet: Pet,
        task_manager: TaskManager,
        scheduler: Scheduler,
        current_plan: DailyPlan | None = None,
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.task_manager = task_manager
        self.scheduler = scheduler
        self.current_plan = current_plan

    def collect_user_input(self) -> None:
        pass

    def save_task_changes(self) -> None:
        pass

    def build_plan(self) -> None:
        pass

    def display_plan(self) -> None:
        pass
