"""add 命令"""

import typer
from datetime import datetime, timedelta
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


def _generate_notes(
    region: str = None,
    job: str = None,
    tech_level: str = None,
    needs: str = None,
    communication: str = None,
) -> str:
    """生成结构化 notes"""
    notes_parts = []
    
    # 会员画像
    if region or job or tech_level:
        notes_parts.append("## 会员画像")
        if region:
            notes_parts.append(f"- 地区：{region}")
        if job:
            notes_parts.append(f"- 职业：{job}")
        if tech_level:
            level_map = {
                "beginner": "初学者",
                "intermediate": "中级",
                "advanced": "高级",
            }
            notes_parts.append(f"- 技术水平：{level_map.get(tech_level, tech_level)}")
        notes_parts.append("")
    
    # 核心需求
    if needs:
        notes_parts.append("## 核心需求")
        for i, need in enumerate(needs.split(","), 1):
            need = need.strip()
            if need:
                notes_parts.append(f"{i}. {need}")
        notes_parts.append("")
    
    # 沟通记录
    if communication:
        notes_parts.append("## 沟通记录")
        notes_parts.append(f"- {datetime.now().strftime('%Y-%m-%d')}：{communication}")
        notes_parts.append("")
    
    return "\n".join(notes_parts) if notes_parts else None


@json_output
def add(
    name: str = typer.Argument(..., help="会员姓名"),
    wechat: str = typer.Option(None, "--wechat", "-w", help="微信号"),
    phone: str = typer.Option(None, "--phone", help="手机号"),
    email: str = typer.Option(None, "--email", "-e", help="邮箱"),
    account_id: str = typer.Option(None, "--account", "-a", help="用户账号 ID"),
    member_type: str = typer.Option("yearly", "--type", "-t", help="会员类型: yearly(年费)/lifetime(永久)"),
    project: str = typer.Option("donglijuan", "--project", help="项目名称，默认 donglijuan"),
    join_date: str = typer.Option(None, "--join", "-j", help="加入日期 (YYYY-MM-DD)，默认今天"),
    expire_date: str = typer.Option(None, "--expire", "-x", help="到期日期 (YYYY-MM-DD)，年费默认一年后"),
    price: float = typer.Option(499, "--price", help="金额，默认 499"),
    source: str = typer.Option(None, "--source", "-s", help="来源"),
    # 新增字段
    region: str = typer.Option(None, "--region", "-r", help="地区"),
    job: str = typer.Option(None, "--job", help="职业"),
    tech_level: str = typer.Option(None, "--tech-level", help="技术水平: beginner/intermediate/advanced"),
    needs: str = typer.Option(None, "--needs", help="核心需求（逗号分隔）"),
    communication: str = typer.Option(None, "--comm", help="本次沟通摘要"),
    notes: str = typer.Option(None, "--notes", "-n", help="自定义备注（会追加到自动生成的内容后）"),
):
    """添加会员
    
    会员类型：
    - yearly: 年费会员（默认），到期日期默认一年后
    - lifetime: 永久会员，无到期日期
    
    会员画像字段：
    - region: 地区（如：北京、上海）
    - job: 职业（如：程序员、老师）
    - tech_level: 技术水平（beginner/intermediate/advanced）
    
    需求收集：
    - needs: 核心需求，逗号分隔（如："课件制作,公文写作"）
    - communication: 本次沟通摘要
    
    示例：
    dong-member add 郭铭 --wechat guoming9335 --price 199 \\
      --region "山西运城" --job "乡村老师" --tech-level intermediate \\
      --needs "课件制作,公文写作" --comm "老用户，想提升工作效率"
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
    
    # 验证技术水平
    if tech_level and tech_level not in ["beginner", "intermediate", "advanced"]:
        raise DongError("INVALID_TECH_LEVEL", "技术水平必须是 beginner/intermediate/advanced")
    
    # 生成结构化 notes
    auto_notes = _generate_notes(
        region=region,
        job=job,
        tech_level=tech_level,
        needs=needs,
        communication=communication,
    )
    
    # 合并自定义 notes
    final_notes = auto_notes
    if notes:
        if auto_notes:
            final_notes = f"{auto_notes}\n\n{notes}"
        else:
            final_notes = notes
    
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO members (name, wechat, phone, email, account_id, member_type, project, join_date, expire_date, price, source, region, job, tech_level, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, wechat, phone, email, account_id, member_type, project, join_date, expire_date, price, source, region, job, tech_level, final_notes))
        
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
        "region": region,
        "job": job,
        "tech_level": tech_level,
        "notes": final_notes,
    }
