"""
测试 dates.utils 模块

测试日期处理工具函数。
"""

from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

from dong.dates.utils import (
    DateUtils,
    WeekStart,
    date_range,
    relative_date,
    _days_in_month,
)


class TestWeekStart:
    """测试 WeekStart 枚举。"""

    def test_monday_value(self) -> None:
        """测试 MONDAY 值。"""
        assert WeekStart.MONDAY == "monday"

    def test_sunday_value(self) -> None:
        """测试 SUNDAY 值。"""
        assert WeekStart.SUNDAY == "sunday"

    def test_saturday_value(self) -> None:
        """测试 SATURDAY 值。"""
        assert WeekStart.SATURDAY == "saturday"


class TestDateUtilsTodayYesterdayTomorrow:
    """测试 DateUtils 基础日期方法。"""

    def test_today_returns_date(self) -> None:
        """测试 today 返回 date 对象。"""
        result = DateUtils.today()
        assert isinstance(result, date)
        # 验证是今天（允许一定的时间差）
        today = date.today()
        assert result == today

    def test_yesterday_is_one_day_ago(self) -> None:
        """测试 yesterday 是一天前。"""
        result = DateUtils.yesterday()
        today = date.today()
        expected = today - timedelta(days=1)
        assert result == expected

    def test_tomorrow_is_one_day_ahead(self) -> None:
        """测试 tomorrow 是一天后。"""
        result = DateUtils.tomorrow()
        today = date.today()
        expected = today + timedelta(days=1)
        assert result == expected


class TestDateUtilsWeek:
    """测试 DateUtils 周相关方法。"""

    def test_this_week_monday_start(self) -> None:
        """测试本周（周一开始）。"""
        start, end = DateUtils.this_week(WeekStart.MONDAY)

        # 验证是周一到周日
        assert start.weekday() == 0  # 周一
        assert end.weekday() == 6  # 周日

        # 验证包含今天
        today = date.today()
        assert start <= today <= end

    def test_this_week_sunday_start(self) -> None:
        """测试本周（周日开始）。"""
        start, end = DateUtils.this_week(WeekStart.SUNDAY)

        # 验证是周日到周六
        assert start.weekday() == 6  # 周日
        assert end.weekday() == 5  # 周六

        # 验证包含今天
        today = date.today()
        assert start <= today <= end

    def test_this_week_saturday_start(self) -> None:
        """测试本周（周六开始）。"""
        start, end = DateUtils.this_week(WeekStart.SATURDAY)

        # 验证是周六到周五
        assert start.weekday() == 5  # 周六
        assert end.weekday() == 4  # 周五

        # 验证包含今天
        today = date.today()
        assert start <= today <= end

    def test_this_week_default_is_monday(self) -> None:
        """测试本周默认从周一开始。"""
        start1, _ = DateUtils.this_week()
        start2, _ = DateUtils.this_week(WeekStart.MONDAY)
        assert start1 == start2

    def test_last_week_is_seven_days_ago(self) -> None:
        """测试上周是 7 天前。"""
        this_start, this_end = DateUtils.this_week()
        last_start, last_end = DateUtils.last_week()

        # 验证上周是本周减去 7 天
        expected_start = this_start - timedelta(weeks=1)
        expected_end = this_end - timedelta(weeks=1)

        assert last_start == expected_start
        assert last_end == expected_end


class TestDateUtilsMonth:
    """测试 DateUtils 月相关方法。"""

    def test_this_month_first_day(self) -> None:
        """测试本月第一天。"""
        start, _ = DateUtils.this_month()
        today = date.today()

        assert start.day == 1
        assert start.month == today.month
        assert start.year == today.year

    def test_this_month_last_day(self) -> None:
        """测试本月最后一天。"""
        _, end = DateUtils.this_month()
        today = date.today()

        # 验证是本月
        assert end.month == today.month
        assert end.year == today.year

        # 验证最后一天的属性
        next_day = end + timedelta(days=1)
        assert next_day.day == 1  # 第二天是下个月第一天

    def test_this_month_february(self) -> None:
        """测试二月份（闰年）。"""
        # 使用 2024 年闰年的二月
        with patch("dong.dates.utils.date") as mock_date_cls:
            # 只 mock today 方法，保持 date 构造函数正常
            mock_date_cls.today.return_value = date(2024, 2, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_month()

            assert start == date(2024, 2, 1)
            assert end == date(2024, 2, 29)  # 闰年 29 天

    def test_this_month_december(self) -> None:
        """测试12月份（跨年逻辑）。"""
        # 使用 12 月测试跨年到明年 1 月
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 12, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_month()

            assert start == date(2024, 12, 1)
            assert end == date(2024, 12, 31)

    def test_last_month(self) -> None:
        """测试上月。"""
        last_start, last_end = DateUtils.last_month()

        # 验证上月第一天是 1 号
        assert last_start.day == 1

        # 验证上月最后一天
        next_day = last_end + timedelta(days=1)
        assert next_day.day == 1

    def test_last_month_year_boundary(self) -> None:
        """测试跨年边界（去年 12 月）。"""
        # 使用 1 月测试去年 12 月
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 1, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            last_start, last_end = DateUtils.last_month()

            assert last_start == date(2023, 12, 1)
            assert last_end == date(2023, 12, 31)


class TestDateUtilsQuarter:
    """测试 DateUtils 季度相关方法。"""

    def test_this_quarter_q1(self) -> None:
        """测试 Q1（1-3 月）。"""
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 2, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_quarter()

            assert start == date(2024, 1, 1)
            assert end == date(2024, 3, 31)

    def test_this_quarter_q2(self) -> None:
        """测试 Q2（4-6 月）。"""
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 5, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_quarter()

            assert start == date(2024, 4, 1)
            assert end == date(2024, 6, 30)

    def test_this_quarter_q3(self) -> None:
        """测试 Q3（7-9 月）。"""
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 8, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_quarter()

            assert start == date(2024, 7, 1)
            assert end == date(2024, 9, 30)

    def test_this_quarter_q4(self) -> None:
        """测试 Q4（10-12 月）。"""
        with patch("dong.dates.utils.date") as mock_date_cls:
            mock_date_cls.today.return_value = date(2024, 11, 15)
            mock_date_cls.side_effect = lambda *args, **kw: date(*args, **kw)
            start, end = DateUtils.this_quarter()

            assert start == date(2024, 10, 1)
            assert end == date(2024, 12, 31)


class TestDateUtilsYear:
    """测试 DateUtils 年相关方法。"""

    def test_this_year(self) -> None:
        """测试本年。"""
        start, end = DateUtils.this_year()
        today = date.today()

        assert start == date(today.year, 1, 1)
        assert end == date(today.year, 12, 31)


class TestDateUtilsParse:
    """测试 DateUtils.parse 方法。"""

    def test_parse_today_keyword(self) -> None:
        """测试解析 'today' 关键词。"""
        result = DateUtils.parse("today")
        assert result == date.today()

    def test_parse_yesterday_keyword(self) -> None:
        """测试解析 'yesterday' 关键词。"""
        result = DateUtils.parse("yesterday")
        assert result == date.today() - timedelta(days=1)

    def test_parse_tomorrow_keyword(self) -> None:
        """测试解析 'tomorrow' 关键词。"""
        result = DateUtils.parse("tomorrow")
        assert result == date.today() + timedelta(days=1)

    def test_parse_this_week_keyword(self) -> None:
        """测试解析 'this week' 关键词。"""
        result = DateUtils.parse("this week")
        start, _ = DateUtils.this_week()
        assert result == start

    def test_parse_this_month_keyword(self) -> None:
        """测试解析 'this month' 关键词。"""
        result = DateUtils.parse("this month")
        start, _ = DateUtils.this_month()
        assert result == start

    def test_parse_this_year_keyword(self) -> None:
        """测试解析 'this year' 关键词。"""
        result = DateUtils.parse("this year")
        start, _ = DateUtils.this_year()
        assert result == start

    def test_parse_iso_format_yyyy_mm_dd(self) -> None:
        """测试解析 ISO 格式 YYYY-MM-DD。"""
        result = DateUtils.parse("2024-03-15")
        assert result == date(2024, 3, 15)

    def test_parse_slash_format_yyyy_mm_dd(self) -> None:
        """测试解析斜杠格式 YYYY/MM/DD。"""
        result = DateUtils.parse("2024/03/15")
        assert result == date(2024, 3, 15)

    def test_parse_compact_format_yyyymmdd(self) -> None:
        """测试解析紧凑格式 YYYYMMDD。"""
        result = DateUtils.parse("20240315")
        assert result == date(2024, 3, 15)

    def test_parse_with_whitespace(self) -> None:
        """测试解析带空格的输入。"""
        result = DateUtils.parse("  2024-03-15  ")
        assert result == date(2024, 3, 15)

    def test_parse_case_insensitive_keywords(self) -> None:
        """测试关键词大小写不敏感。"""
        result1 = DateUtils.parse("TODAY")
        result2 = DateUtils.parse("Today")
        result3 = DateUtils.parse("today")
        assert result1 == result2 == result3 == date.today()

    def test_parse_invalid_string_raises_error(self) -> None:
        """测试解析无效字符串抛出错误。"""
        with pytest.raises(ValueError, match="无法解析日期"):
            DateUtils.parse("invalid-date")

    def test_parse_invalid_format_raises_error(self) -> None:
        """测试解析无效格式抛出错误。"""
        with pytest.raises(ValueError, match="无法解析日期"):
            DateUtils.parse("15-03-2024")  # 错误的顺序


class TestDateUtilsFormat:
    """测试 DateUtils.format 方法。"""

    def test_format_default_format(self) -> None:
        """测试默认格式。"""
        test_date = date(2024, 3, 15)
        result = DateUtils.format(test_date)
        assert result == "2024-03-15"

    def test_format_custom_format(self) -> None:
        """测试自定义格式。"""
        test_date = date(2024, 3, 15)
        result = DateUtils.format(test_date, "%Y/%m/%d")
        assert result == "2024/03/15"

    def test_format_chinese_format(self) -> None:
        """测试中文格式。"""
        test_date = date(2024, 3, 15)
        result = DateUtils.format(test_date, "%Y年%m月%d日")
        assert result == "2024年03月15日"


class TestDateRange:
    """测试 date_range 函数。"""

    def test_date_range_inclusive(self) -> None:
        """测试包含结束日期的范围。"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)

        result = date_range(start, end, inclusive=True)

        assert len(result) == 3
        assert result[0] == date(2024, 1, 1)
        assert result[1] == date(2024, 1, 2)
        assert result[2] == date(2024, 1, 3)

    def test_date_range_exclusive(self) -> None:
        """测试不包含结束日期的范围。"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)

        result = date_range(start, end, inclusive=False)

        assert len(result) == 2
        assert result[0] == date(2024, 1, 1)
        assert result[1] == date(2024, 1, 2)

    def test_date_range_single_day(self) -> None:
        """测试单日范围。"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 1)

        result = date_range(start, end, inclusive=True)

        assert len(result) == 1
        assert result[0] == start

    def test_date_range_reversed_returns_empty(self) -> None:
        """测试反转范围返回空列表。"""
        start = date(2024, 1, 5)
        end = date(2024, 1, 1)

        result = date_range(start, end)

        assert result == []

    def test_date_range_same_date_exclusive(self) -> None:
        """测试相同日期（不包含）。"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 1)

        result = date_range(start, end, inclusive=False)

        assert result == []

    def test_date_range_week(self) -> None:
        """测试一周范围。"""
        start = date(2024, 1, 1)  # 周一
        end = date(2024, 1, 7)    # 周日

        result = date_range(start, end)

        assert len(result) == 7
        assert result[0].weekday() == 0  # 周一
        assert result[-1].weekday() == 6  # 周日


class TestRelativeDate:
    """测试 relative_date 函数。"""

    def test_relative_date_default_base(self) -> None:
        """测试默认基准日期是今天。"""
        result = relative_date(days=1)
        expected = date.today() + timedelta(days=1)
        assert result == expected

    def test_relative_date_add_days(self) -> None:
        """测试增加天数。"""
        base = date(2024, 1, 1)
        result = relative_date(base, days=5)
        assert result == date(2024, 1, 6)

    def test_relative_date_subtract_days(self) -> None:
        """测试减少天数。"""
        base = date(2024, 1, 10)
        result = relative_date(base, days=-3)
        assert result == date(2024, 1, 7)

    def test_relative_date_add_weeks(self) -> None:
        """测试增加周数。"""
        base = date(2024, 1, 1)
        result = relative_date(base, weeks=2)
        assert result == date(2024, 1, 15)

    def test_relative_date_add_months(self) -> None:
        """测试增加月数。"""
        base = date(2024, 1, 15)
        result = relative_date(base, months=1)
        assert result == date(2024, 2, 15)

    def test_relative_date_subtract_months(self) -> None:
        """测试减少月数。"""
        base = date(2024, 3, 15)
        result = relative_date(base, months=-2)
        assert result == date(2024, 1, 15)

    def test_relative_date_add_years(self) -> None:
        """测试增加年数。"""
        base = date(2024, 1, 15)
        result = relative_date(base, years=1)
        assert result == date(2025, 1, 15)

    def test_relative_date_month_overflow(self) -> None:
        """测试月份溢出（1月31日 + 1个月）。"""
        base = date(2024, 1, 31)
        result = relative_date(base, months=1)
        # 2月没有31天，应该取2月最后一天
        assert result == date(2024, 2, 29)  # 闰年

    def test_relative_date_leap_year_february(self) -> None:
        """测试闰年二月。"""
        base = date(2024, 2, 29)
        result = relative_date(base, years=1)
        # 2025年不是闰年，2月只有28天
        assert result == date(2025, 2, 28)

    def test_relative_date_combined_offset(self) -> None:
        """测试组合偏移量。"""
        base = date(2024, 1, 1)
        result = relative_date(base, years=1, months=2, days=10)
        assert result == date(2025, 3, 11)

    def test_relative_date_year_boundary(self) -> None:
        """测试跨年边界。"""
        base = date(2024, 12, 15)
        result = relative_date(base, months=1)
        assert result == date(2025, 1, 15)


class TestDaysInMonth:
    """测试 _days_in_month 辅助函数。"""

    def test_days_in_january(self) -> None:
        """测试一月天数。"""
        assert _days_in_month(2024, 1) == 31

    def test_days_in_february_leap_year(self) -> None:
        """测试闰年二月天数。"""
        assert _days_in_month(2024, 2) == 29

    def test_days_in_february_non_leap_year(self) -> None:
        """测试非闰年二月天数。"""
        assert _days_in_month(2023, 2) == 28

    def test_days_in_april(self) -> None:
        """测试四月（30天）。"""
        assert _days_in_month(2024, 4) == 30

    def test_days_in_december(self) -> None:
        """测试十二月。"""
        assert _days_in_month(2024, 12) == 31

    def test_days_in_month_year_boundary(self) -> None:
        """测试跨年边界（12月到次年1月）。"""
        assert _days_in_month(2024, 12) == 31
        assert _days_in_month(2025, 1) == 31
