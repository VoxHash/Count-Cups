"""Scheduling service for Count-Cups."""

import threading
import time
from collections.abc import Callable
from datetime import datetime
from datetime import time as dt_time

from app.core.logging import get_logger

logger = get_logger(__name__)


class Scheduler:
    """Handles scheduled tasks and timers."""

    def __init__(self):
        """Initialize scheduler."""
        self.tasks = {}
        self.running = False
        self.thread = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the scheduler."""
        if self.running:
            return

        self.running = True
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

        logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        if not self.running:
            return

        self.running = False
        self._stop_event.set()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

        logger.info("Scheduler stopped")

    def _run(self) -> None:
        """Main scheduler loop."""
        while self.running and not self._stop_event.is_set():
            try:
                current_time = datetime.now()

                # Check all tasks
                for task_id, task in list(self.tasks.items()):
                    if self._should_run_task(task, current_time):
                        try:
                            task["callback"]()
                            logger.debug(f"Task {task_id} executed")
                        except Exception as e:
                            logger.error(f"Task {task_id} failed: {e}")

                        # Remove one-time tasks
                        if task["type"] == "once":
                            del self.tasks[task_id]

                # Sleep for a short interval
                time.sleep(1)

            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(5)

    def _should_run_task(self, task: dict, current_time: datetime) -> bool:
        """Check if a task should run.

        Args:
            task: Task definition
            current_time: Current datetime

        Returns:
            True if task should run, False otherwise
        """
        if task["type"] == "once":
            return current_time >= task["run_time"]
        elif task["type"] == "daily":
            return (
                current_time.time() >= task["run_time"]
                and current_time.date() > task["last_run"]
            )
        elif task["type"] == "interval":
            return (current_time - task["last_run"]).total_seconds() >= task["interval"]

        return False

    def schedule_once(
        self, callback: Callable, run_time: datetime, task_id: str | None = None
    ) -> str:
        """Schedule a one-time task.

        Args:
            callback: Function to call
            run_time: When to run the task
            task_id: Optional task ID (auto-generated if not provided)

        Returns:
            Task ID
        """
        if task_id is None:
            task_id = f"once_{int(time.time())}"

        self.tasks[task_id] = {
            "type": "once",
            "callback": callback,
            "run_time": run_time,
            "last_run": None,
        }

        logger.info(f"Scheduled one-time task {task_id} for {run_time}")
        return task_id

    def schedule_daily(
        self, callback: Callable, run_time: dt_time, task_id: str | None = None
    ) -> str:
        """Schedule a daily recurring task.

        Args:
            callback: Function to call
            run_time: Time of day to run the task
            task_id: Optional task ID (auto-generated if not provided)

        Returns:
            Task ID
        """
        if task_id is None:
            task_id = f"daily_{run_time.strftime('%H%M')}"

        self.tasks[task_id] = {
            "type": "daily",
            "callback": callback,
            "run_time": run_time,
            "last_run": datetime.now().date(),
        }

        logger.info(f"Scheduled daily task {task_id} for {run_time}")
        return task_id

    def schedule_interval(
        self, callback: Callable, interval_seconds: int, task_id: str | None = None
    ) -> str:
        """Schedule a recurring task with fixed interval.

        Args:
            callback: Function to call
            interval_seconds: Interval in seconds
            task_id: Optional task ID (auto-generated if not provided)

        Returns:
            Task ID
        """
        if task_id is None:
            task_id = f"interval_{interval_seconds}s"

        self.tasks[task_id] = {
            "type": "interval",
            "callback": callback,
            "interval": interval_seconds,
            "last_run": datetime.now(),
        }

        logger.info(
            f"Scheduled interval task {task_id} every {interval_seconds} seconds"
        )
        return task_id

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task.

        Args:
            task_id: Task ID to cancel

        Returns:
            True if task was cancelled, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Cancelled task {task_id}")
            return True

        return False

    def get_task_count(self) -> int:
        """Get number of scheduled tasks.

        Returns:
            Number of scheduled tasks
        """
        return len(self.tasks)

    def get_tasks(self) -> dict:
        """Get all scheduled tasks.

        Returns:
            Dictionary of task ID to task definition
        """
        return self.tasks.copy()


class DailyResetScheduler:
    """Handles daily reset tasks."""

    def __init__(self, reset_callback: Callable):
        """Initialize daily reset scheduler.

        Args:
            reset_callback: Function to call for daily reset
        """
        self.reset_callback = reset_callback
        self.scheduler = Scheduler()
        self.task_id = None

        # Schedule daily reset at midnight
        self.schedule_daily_reset()

    def schedule_daily_reset(self) -> None:
        """Schedule daily reset at midnight."""
        midnight = dt_time(0, 0)  # 00:00
        self.task_id = self.scheduler.schedule_daily(
            self._perform_daily_reset, midnight, "daily_reset"
        )

        self.scheduler.start()
        logger.info("Daily reset scheduled for midnight")

    def _perform_daily_reset(self) -> None:
        """Perform daily reset."""
        try:
            self.reset_callback()
            logger.info("Daily reset completed")
        except Exception as e:
            logger.error(f"Daily reset failed: {e}")

    def stop(self) -> None:
        """Stop the scheduler."""
        self.scheduler.stop()


class GoalReminderScheduler:
    """Handles goal reminder notifications."""

    def __init__(self, reminder_callback: Callable):
        """Initialize goal reminder scheduler.

        Args:
            reminder_callback: Function to call for goal reminders
        """
        self.reminder_callback = reminder_callback
        self.scheduler = Scheduler()
        self.task_id = None

        # Schedule goal reminder at 8 PM
        self.schedule_goal_reminder()

    def schedule_goal_reminder(self) -> None:
        """Schedule goal reminder at 8 PM."""
        reminder_time = dt_time(20, 0)  # 8 PM
        self.task_id = self.scheduler.schedule_daily(
            self._perform_goal_reminder, reminder_time, "goal_reminder"
        )

        self.scheduler.start()
        logger.info("Goal reminder scheduled for 8 PM")

    def _perform_goal_reminder(self) -> None:
        """Perform goal reminder."""
        try:
            self.reminder_callback()
            logger.info("Goal reminder sent")
        except Exception as e:
            logger.error(f"Goal reminder failed: {e}")

    def stop(self) -> None:
        """Stop the scheduler."""
        self.scheduler.stop()


# Global scheduler instances
scheduler = Scheduler()
daily_reset_scheduler = None
goal_reminder_scheduler = None
