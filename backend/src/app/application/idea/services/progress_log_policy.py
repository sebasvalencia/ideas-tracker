def should_create_system_log(
    before_status: str,
    before_progress: float,
    after_status: str,
    after_progress: float,
) -> bool:
    return (before_status != after_status) or (before_progress != after_progress)


def system_log_message(
    before_status: str,
    before_progress: float,
    after_status: str,
    after_progress: float,
) -> str:
    return (
        "[system] state/progress changed: "
        f"status {before_status}->{after_status}, "
        f"progress {before_progress}->{after_progress}"
    )
