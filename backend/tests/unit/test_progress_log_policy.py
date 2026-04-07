from src.app.application.idea.services.progress_log_policy import should_create_system_log, system_log_message


def test_auto_log_only_when_real_change() -> None:
    assert should_create_system_log("idea", 0.0, "in_progress", 10.0) is True
    assert should_create_system_log("idea", 0.0, "idea", 0.0) is False


def test_system_log_message_contains_before_and_after_values() -> None:
    msg = system_log_message("idea", 0.0, "in_progress", 25.0)
    assert "status idea->in_progress" in msg
    assert "progress 0.0->25.0" in msg
