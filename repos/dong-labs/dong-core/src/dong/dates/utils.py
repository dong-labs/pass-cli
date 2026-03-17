"""
日期处理工具函数

提供常用的日期处理功能，简化 CLI 工具中的日期操作。

Examples:
    ```python
    from dong.dates import DateUtils, date_range

    # 获取今天
    today = DateUtils.today()

    # 获取本周日期范围
    week_start, week_end = DateUtils.this_week()

    # 生成本月所有日期
    for day in date_range(*DateUtils.this_month()):
        print(day)
    ```
"""

from datetime import date, datetime, timedelta
from typing import Literal
from enum import StrEnum


class WeekStart(StrEnum):
    """一周开始日的定义"""

    MONDAY = "monday"
    SUNDAY = "sunday"
    SATURDAY = "saturday"


class DateUtils:
    """
    日期工具类

    提供静态方法用于获取常用的日期范围。
    所有方法返回 date 对象，不包含时间部分。
    """

    @staticmethod
    def today() -> date:
        """
        获取今天的日期

        Returns:
            今天的 date 对象
        """
        return date.today()

    @staticmethod
    def yesterday() -> date:
        """
        获取昨天的日期

        Returns:
            昨天的 date 对象
        """
        return date.today() - timedelta(days=1)

    @staticmethod
    def tomorrow() -> date:
        """
        获取明天的日期

        Returns:
            明天的 date 对象
        """
        return date.today() + timedelta(days=1)

    @staticmethod
    def this_week(
        week_start: WeekStart = WeekStart.MONDAY,
    ) -> tuple[date, date]:
        """
        获取本周的日期范围

        Args:
            week_start: 一周的开始日，默认为周一

        Returns:
            (周开始日期, 周结束日期) 的元组

        Examples:
            ```python
            # 周一开始（默认）
            start, end = DateUtils.this_week()

            # 周日开始
            start, end = DateUtils.this_week(week_start=WeekStart.SUNDAY)
            ```
        """
        today = date.today()
        weekday = today.weekday()  # Monday = 0, Sunday = 6

        match week_start:
            case WeekStart.MONDAY:
                days_to_subtract = weekday
            case WeekStart.SUNDAY:
                days_to_subtract = (weekday + 1) % 7
            case WeekStart.SATURDAY:
                days_to_subtract = (weekday + 2) % 7
            case _:
                days_to_subtract = weekday

        start = today - timedelta(days=days_to_subtract)
        end = start + timedelta(days=6)
        return start, end

    @staticmethod
    def last_week(
        week_start: WeekStart = WeekStart.MONDAY,
    ) -> tuple[date, date]:
        """
        获取上周的日期范围

        Args:
            week_start: 一周的开始日，默认为周一

        Returns:
            (周开始日期, 周结束日期) 的元组
        """
        start, end = DateUtils.this_week(week_start)
        last_week_start = start - timedelta(weeks=1)
        last_week_end = end - timedelta(weeks=1)
        return last_week_start, last_week_end

    @staticmethod
    def this_month() -> tuple[date, date]:
        """
        获取本月的日期范围

        Returns:
            (月初日期, 月末日期) 的元组

        Examples:
            ```python
            # 假设今天是 2024-01-15
            start, end = DateUtils.this_month()
            # start = 2024-01-01, end = 2024-01-31
            ```
        """
        today = date.today()
        first_day = date(today.year, today.month, 1)

        # 获取下个月第一天，再减一天得到本月最后一天
        if today.month == 12:
            next_month_first = date(today.year + 1, 1, 1)
        else:
            next_month_first = date(today.year, today.month + 1, 1)

        last_day = next_month_first - timedelta(days=1)
        return first_day, last_day

    @staticmethod
    def last_month() -> tuple[date, date]:
        """
        获取上月的日期范围

        Returns:
            (月初日期, 月末日期) 的元组
        """
        first_day, last_day = DateUtils.this_month()

        # 上月最后日 = 本月第一日 - 1
        last_month_last = first_day - timedelta(days=1)

        # 上月第一日
        last_month_first = date(
            last_month_last.year,
            last_month_last.month,
            1,
        )

        return last_month_first, last_month_last

    @staticmethod
    def this_quarter() -> tuple[date, date]:
        """
        获取本季度的日期范围

        Returns:
            (季度开始日期, 季度结束日期) 的元组

        Examples:
            ```python
            # 假设今天是 2024-02-15
            start, end = DateUtils.this_quarter()
            # start = 2024-01-01, end = 2024-03-31
            ```
        """
        today = date.today()
        quarter = (today.month - 1) // 3 + 1
        quarter_start_month = (quarter - 1) * 3 + 1
        quarter_end_month = quarter * 3

        start = date(today.year, quarter_start_month, 1)

        # 计算季度最后一天
        if quarter_end_month == 12:
            end = date(today.year, 12, 31)
        else:
            next_month = date(today.year, quarter_end_month + 1, 1)
            end = next_month - timedelta(days=1)

        return start, end

    @staticmethod
    def this_year() -> tuple[date, date]:
        """
        获取本年的日期范围

        Returns:
            (年初日期, 年末日期) 的元组
        """
        today = date.today()
        start = date(today.year, 1, 1)
        end = date(today.year, 12, 31)
        return start, end

    @staticmethod
    def parse(date_str: str) -> date:
        """
        解析日期字符串

        支持多种格式：
        - YYYY-MM-DD
        - YYYY/MM/DD
        - today, yesterday, tomorrow
        - this week, this month, this year

        Args:
            date_str: 日期字符串

        Returns:
            解析后的 date 对象

        Raises:
            ValueError: 无法解析日期字符串
        """
        date_str = date_str.strip().lower()

        # 关键词
        keywords = {
            "today": DateUtils.today,
            "yesterday": DateUtils.yesterday,
            "tomorrow": DateUtils.tomorrow,
        }
        if date_str in keywords:
            return keywords[date_str]()

        # 范围关键词 - 返回起始日期
        if date_str == "this week":
            return DateUtils.this_week()[0]
        if date_str == "this month":
            return DateUtils.this_month()[0]
        if date_str == "this year":
            return DateUtils.this_year()[0]

        # 标准格式
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"无法解析日期: {date_str}")

    @staticmethod
    def format(date_obj: date, fmt: str = "%Y-%m-%d") -> str:
        """
        格式化日期为字符串

        Args:
            date_obj: 日期对象
            fmt: 格式字符串，默认为 "%Y-%m-%d"

        Returns:
            格式化后的日期字符串
        """
        return date_obj.strftime(fmt)


def date_range(
    start: date,
    end: date,
    inclusive: bool = True,
) -> list[date]:
    """
    生成日期范围内的所有日期

    Args:
        start: 开始日期
        end: 结束日期
        inclusive: 是否包含结束日期，默认为 True

    Returns:
        日期列表

    Examples:
        ```python
        from dong.dates import date_range
        from datetime import date

        # 生成 2024-01-01 到 2024-01-03 的所有日期
        dates = date_range(date(2024, 1, 1), date(2024, 1, 3))
        # [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)]

        # 不包含结束日期
        dates = date_range(date(2024, 1, 1), date(2024, 1, 3), inclusive=False)
        # [date(2024, 1, 1), date(2024, 1, 2)]
        ```
    """
    if inclusive:
        end = end + timedelta(days=1)

    days = (end - start).days
    if days < 0:
        return []

    return [start + timedelta(days=i) for i in range(days)]


def relative_date(
    base: date | None = None,
    *,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
) -> date:
    """
    计算相对日期

    Args:
        base: 基准日期，默认为今天
        years: 年份偏移量
        months: 月份偏移量
        weeks: 周偏移量
        days: 天偏移量

    Returns:
        计算后的日期

    Examples:
        ```python
        from dong.dates import relative_date

        # 下个月今天
        next_month = relative_date(months=1)

        # 三周前
        three_weeks_ago = relative_date(weeks=-3)

        # 明年这个时候
        next_year = relative_date(years=1)
        ```
    """
    base = base or date.today()

    # 处理年月（需要手动计算，因为 timedelta 不支持）
    if years != 0 or months != 0:
        # 计算总月数
        total_months = base.year * 12 + base.month - 1
        total_months += years * 12 + months

        new_year = total_months // 12
        new_month = total_months % 12 + 1

        # 处理日期溢出（如 1月31日 + 1个月）
        new_day = min(base.day, _days_in_month(new_year, new_month))
        base = date(new_year, new_month, new_day)

    # 处理周和日
    delta = timedelta(weeks=weeks, days=days)
    return base + delta


def _days_in_month(year: int, month: int) -> int:
    """获取指定月份的天数"""
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - timedelta(days=1)).day
