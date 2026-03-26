"""add 命令"""

import typer
from datetime import datetime, timedelta
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


@json_output
def add(
    name: str = typer.Argument(..., help="会员姓名"),
    wechat: str = typer.Option(None, "--wechat", "-w", help="微信号"),
    phone: str = typer.Option(None, "--phone", "-p", help="手机号"),
    email: str = typer.Option(None, "--email", "-e", help="邮箱"),
    account_id: str = typer.Option(None, "--account", "-a", help="用户账号 ID"),
    member_type: str = typer.Option("yearly", "--type", "-t", help="会员类型: yearly(年费)/lifetime(永久)"),
    project: str = typer.Option("donglijuan", "--project", help="项目名称，默认 donglijuan"),
    join_date: str = typer.Option(None, "--join", "-j", help="加入日期 (YYYY-MM-DD)，默认今天"),
    expire_date: str = typer.Option(None, "--expire", "-x", help="到期日期 (YYYY-MM-DD)，年费默认一年后"),
    price: float = typer.Option(499, "--price", help="金额，默认 499"),
    source: str = typer.Option(None, "--source", "-s", help="来源"),
    notes: str = typer.Option(None, "--notes", "-n", help="备注"),
):
    """添加会员
    
    会员类型：
    - yearly: 年费会员（默认），到期日期默认一年后
    - lifetime: 永久会员，无到期日期
    """
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-member init")
    
    # 默认加入日期为今天
    if not join_date:
        join_date = datetime.now().strftime("%Y-%m-%d")
    
    # 根据会员类型设置到期日期
    if member_type == "lifetime":
        expire_date = None  # 永久会员无到期日期
    elif not expire_date:
        # 年费会员默认一年后
        expire_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    
    # 验证日期格式
    try:
        datetime.strptime(join_date, "%Y-%m-%d")
        if expire_date:
            datetime.strptime(expire_date, "%Y-%m-%d")
    except ValueError:
        raise DongError("INVALID_DATE", "日期格式错误，请使用 YYYY-MM-DD")
    
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO members (name, wechat, phone, email, account_id, member_type, project, join_date, expire_date, price, source, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, wechat, phone, email, account_id, member_type, project, join_date, expire_date, price, source, notes))
        
        member_id = cur.lastrowid
    
    return {
        "id": member_id,
        "name": name,
        "wechat": wechat,
        "account_id": account_id,
        "member_type": member_type,
        "project": project,
        "join_date": join_date,
        "expire_date": expire_date,
        "price": price,
    }
