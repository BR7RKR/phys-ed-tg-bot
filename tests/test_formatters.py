import pytest

from engine.exceptions import NegativeTimeError
from utils.formatters import TimeFormatter


class TestTimeFormatter:
    @pytest.mark.parametrize("seconds, expected_time", [
        (100000, "27:46:40"),
        (10073537, "2798:12:17"),
        (3600, "01:00:00")
    ])
    def test_format_time_hours_minutes_seconds(self, seconds, expected_time):
        # act
        result = TimeFormatter.format_time(seconds)
        # assert
        assert result == expected_time

    @pytest.mark.parametrize("seconds, expected_time", [
        (60, "01:00"),
        (3000, "50:00"),
        (3599, "59:59")
    ])
    def test_format_time_minutes_seconds(self, seconds, expected_time):
        # act
        result = TimeFormatter.format_time(seconds)
        # assert
        assert result == expected_time

    @pytest.mark.parametrize("seconds, expected_time", [
        (0, "00"),
        (1, "01"),
        (59, "59")
    ])
    def test_format_time_seconds(self, seconds, expected_time):
        # act
        result = TimeFormatter.format_time(seconds)
        # assert
        assert result == expected_time

    def test_format_time_negative_seconds(self):
        #assert
        seconds = -1
        # act
        with pytest.raises(NegativeTimeError) as exc_info:
            TimeFormatter.format_time(seconds)
        # assert
        assert exc_info.type == NegativeTimeError
