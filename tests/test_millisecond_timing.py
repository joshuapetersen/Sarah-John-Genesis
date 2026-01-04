import pytest

from Millisecond_Timing import MillisecondTimer


def test_reconcile_within_buffer_prefers_predictive():
    actual = MillisecondTimer.get_unix_ms()
    report = MillisecondTimer.reconcile_predictive_time(actual + 100, buffer_ms=200)

    assert report["predictive_within_buffer"] is True
    assert report["authoritative_source"] == "predictive"
    assert report["authoritative_unix_ms"] == report["predictive_unix_ms"]


def test_reconcile_outside_buffer_prefers_actual():
    actual = MillisecondTimer.get_unix_ms()
    report = MillisecondTimer.reconcile_predictive_time(actual + 2000, buffer_ms=200)

    assert report["predictive_within_buffer"] is False
    assert report["authoritative_source"] == "actual"
    assert report["authoritative_unix_ms"] == report["actual_unix_ms"]


def test_sovereign_time_check_includes_drift_and_device_flag():
    report = MillisecondTimer.sovereign_time_reality_check("PC_TERMINAL", drift_threshold_ms=500)

    assert report["device_allowed"] is True
    assert "drift_report" in report
    assert isinstance(report["drift_report"].get("drift_ok"), bool)
