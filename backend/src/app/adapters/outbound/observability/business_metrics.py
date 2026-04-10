from datetime import datetime

from prometheus_client import Counter, Gauge, Histogram

ideas_created_total = Counter(
    "ideas_created_total",
    "Total number of ideas created",
)
ideas_completed_total = Counter(
    "ideas_completed_total",
    "Total number of ideas moved to completed",
)
ideas_rating_sum = Counter(
    "ideas_rating_sum_total",
    "Sum of idea ratings registered",
)
ideas_rating_count = Counter(
    "ideas_rating_count_total",
    "Count of idea ratings registered",
)
ideas_rating_updates_total = Counter(
    "ideas_rating_updates_total",
    "Total number of rating updates",
)
ideas_rating_average = Gauge(
    "ideas_rating_average",
    "Average of idea ratings",
)
idea_cycle_time_seconds = Histogram(
    "idea_cycle_time_seconds",
    "Cycle time from idea creation to completion in seconds",
    buckets=(300, 900, 1800, 3600, 7200, 14400, 28800, 86400, 172800, 604800),
)
_ratings_by_idea: dict[int, int] = {}


def record_idea_created() -> None:
    ideas_created_total.inc()


def record_idea_completed(created_at: datetime | None = None, completed_at: datetime | None = None) -> None:
    ideas_completed_total.inc()
    if created_at is not None and completed_at is not None:
        cycle_seconds = (completed_at - created_at).total_seconds()
        if cycle_seconds >= 0:
            idea_cycle_time_seconds.observe(cycle_seconds)


def _set_average_from_snapshot() -> None:
    if not _ratings_by_idea:
        ideas_rating_average.set(0)
        return
    average = sum(_ratings_by_idea.values()) / len(_ratings_by_idea)
    ideas_rating_average.set(average)


def record_rating_created(idea_id: int, value: int) -> None:
    if idea_id in _ratings_by_idea:
        record_rating_updated(idea_id=idea_id, value=value)
        return
    _ratings_by_idea[idea_id] = value
    ideas_rating_sum.inc(value)
    ideas_rating_count.inc()
    _set_average_from_snapshot()


def record_rating_updated(idea_id: int, value: int) -> None:
    _ratings_by_idea[idea_id] = value
    ideas_rating_updates_total.inc()
    _set_average_from_snapshot()
