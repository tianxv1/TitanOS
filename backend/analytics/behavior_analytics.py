"""
Behavior Analytics - 用户行为分析引擎
支持学习时间统计、活跃时间分析、项目投入追踪、目标完成率计算
生成周报、月报，并提供可视化数据
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict
import json
import os


@dataclass
class ActivitySession:
    """活动会话"""
    id: str
    activity_type: str  # learning, project, goal, chat, etc.
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "activity_type": self.activity_type,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_minutes": self.duration_minutes,
            "metadata": self.metadata
        }


@dataclass
class BehaviorMetrics:
    """行为指标"""
    total_learning_time: float = 0.0  # minutes
    total_project_time: float = 0.0
    total_chat_sessions: int = 0
    total_memories_created: int = 0
    goals_completed: int = 0
    goals_created: int = 0
    active_days: int = 0
    avg_daily_activity: float = 0.0
    peak_activity_hour: int = 0
    streak_days: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_learning_time": round(self.total_learning_time, 1),
            "total_project_time": round(self.total_project_time, 1),
            "total_chat_sessions": self.total_chat_sessions,
            "total_memories_created": self.total_memories_created,
            "goals_completed": self.goals_completed,
            "goals_created": self.goals_created,
            "active_days": self.active_days,
            "avg_daily_activity": round(self.avg_daily_activity, 1),
            "peak_activity_hour": self.peak_activity_hour,
            "streak_days": self.streak_days
        }


@dataclass
class WeeklyReport:
    """周报"""
    week_start: datetime
    week_end: datetime
    metrics: BehaviorMetrics
    daily_breakdown: Dict[str, float]  # day -> activity minutes
    top_activities: List[Dict[str, Any]]
    achievements: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "week_start": self.week_start.isoformat(),
            "week_end": self.week_end.isoformat(),
            "metrics": self.metrics.to_dict(),
            "daily_breakdown": self.daily_breakdown,
            "top_activities": self.top_activities,
            "achievements": self.achievements,
            "recommendations": self.recommendations
        }


@dataclass
class MonthlyReport:
    """月报"""
    month: int
    year: int
    metrics: BehaviorMetrics
    weekly_summaries: List[Dict[str, Any]]
    category_distribution: Dict[str, float]
    growth_trend: List[float]
    insights: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "month": self.month,
            "year": self.year,
            "metrics": self.metrics.to_dict(),
            "weekly_summaries": self.weekly_summaries,
            "category_distribution": self.category_distribution,
            "growth_trend": self.growth_trend,
            "insights": self.insights
        }


class BehaviorAnalytics:
    """行为分析引擎"""

    def __init__(self, storage_path: str = "database/behavior_analytics.json"):
        self.storage_path = storage_path
        self.sessions: List[ActivitySession] = []
        self.daily_activities: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for session_data in data.get("sessions", []):
                        session = ActivitySession(
                            id=session_data["id"],
                            activity_type=session_data["activity_type"],
                            start_time=datetime.fromisoformat(session_data["start_time"]),
                            end_time=datetime.fromisoformat(session_data["end_time"]) if session_data.get("end_time") else None,
                            duration_minutes=session_data.get("duration_minutes", 0),
                            metadata=session_data.get("metadata", {})
                        )
                        self.sessions.append(session)
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "sessions": [s.to_dict() for s in self.sessions],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def start_session(self, activity_type: str, metadata: Dict[str, Any] = None) -> ActivitySession:
        """开始一个活动会话"""
        import uuid
        session = ActivitySession(
            id=str(uuid.uuid4()),
            activity_type=activity_type,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        self.sessions.append(session)
        self._save()
        return session

    def end_session(self, session_id: str) -> Optional[ActivitySession]:
        """结束活动会话"""
        for session in self.sessions:
            if session.id == session_id and session.end_time is None:
                session.end_time = datetime.now()
                session.duration_minutes = (session.end_time - session.start_time).total_seconds() / 60
                
                # 记录每日活动
                date_key = session.start_time.strftime("%Y-%m-%d")
                self.daily_activities[date_key][session.activity_type] += session.duration_minutes
                
                self._save()
                return session
        return None

    def record_activity(self, activity_type: str, duration_minutes: float, 
                        timestamp: datetime = None, metadata: Dict[str, Any] = None):
        """记录活动（不需要会话）"""
        import uuid
        timestamp = timestamp or datetime.now()
        session = ActivitySession(
            id=str(uuid.uuid4()),
            activity_type=activity_type,
            start_time=timestamp,
            end_time=timestamp + timedelta(minutes=duration_minutes),
            duration_minutes=duration_minutes,
            metadata=metadata or {}
        )
        self.sessions.append(session)
        
        date_key = timestamp.strftime("%Y-%m-%d")
        self.daily_activities[date_key][activity_type] += duration_minutes
        
        self._save()

    def get_metrics(self, start_date: datetime = None, end_date: datetime = None) -> BehaviorMetrics:
        """获取行为指标"""
        metrics = BehaviorMetrics()
        
        # 过滤时间范围
        sessions = self.sessions
        if start_date:
            sessions = [s for s in sessions if s.start_time >= start_date]
        if end_date:
            sessions = [s for s in sessions if s.start_time <= end_date]

        # 计算各项指标
        hour_counts = defaultdict(int)
        active_dates = set()

        for session in sessions:
            if session.activity_type == "learning":
                metrics.total_learning_time += session.duration_minutes
            elif session.activity_type == "project":
                metrics.total_project_time += session.duration_minutes
            elif session.activity_type == "chat":
                metrics.total_chat_sessions += 1
            elif session.activity_type == "memory":
                metrics.total_memories_created += 1
            elif session.activity_type == "goal_completed":
                metrics.goals_completed += 1
            elif session.activity_type == "goal_created":
                metrics.goals_created += 1

            hour_counts[session.start_time.hour] += 1
            active_dates.add(session.start_time.strftime("%Y-%m-%d"))

        metrics.active_days = len(active_dates)
        
        if metrics.active_days > 0:
            total_time = metrics.total_learning_time + metrics.total_project_time
            metrics.avg_daily_activity = total_time / metrics.active_days

        if hour_counts:
            metrics.peak_activity_hour = max(hour_counts.keys(), key=lambda h: hour_counts[h])

        # 计算连续活跃天数
        metrics.streak_days = self._calculate_streak()

        return metrics

    def _calculate_streak(self) -> int:
        """计算连续活跃天数"""
        if not self.daily_activities:
            return 0

        today = datetime.now().date()
        streak = 0
        current_date = today

        while True:
            date_key = current_date.strftime("%Y-%m-%d")
            if date_key in self.daily_activities and sum(self.daily_activities[date_key].values()) > 0:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break

        return streak

    def get_weekly_report(self, week_start: datetime = None) -> WeeklyReport:
        """生成周报"""
        if week_start is None:
            # 默认从本周一开始
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

        week_end = week_start + timedelta(days=7)
        metrics = self.get_metrics(week_start, week_end)

        # 每日分解
        daily_breakdown = {}
        for i in range(7):
            day = week_start + timedelta(days=i)
            date_key = day.strftime("%Y-%m-%d")
            daily_breakdown[day.strftime("%A")] = sum(self.daily_activities.get(date_key, {}).values())

        # 顶级活动
        activity_totals = defaultdict(float)
        for session in self.sessions:
            if week_start <= session.start_time < week_end:
                activity_totals[session.activity_type] += session.duration_minutes

        top_activities = [
            {"type": k, "duration": round(v, 1)}
            for k, v in sorted(activity_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

        # 成就
        achievements = self._generate_achievements(metrics)

        # 建议
        recommendations = self._generate_recommendations(metrics)

        return WeeklyReport(
            week_start=week_start,
            week_end=week_end,
            metrics=metrics,
            daily_breakdown=daily_breakdown,
            top_activities=top_activities,
            achievements=achievements,
            recommendations=recommendations
        )

    def get_monthly_report(self, year: int = None, month: int = None) -> MonthlyReport:
        """生成月报"""
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        # 计算月份开始和结束
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1)
        else:
            month_end = datetime(year, month + 1, 1)

        metrics = self.get_metrics(month_start, month_end)

        # 周摘要
        weekly_summaries = []
        current_week = month_start
        while current_week < month_end:
            week_report = self.get_weekly_report(current_week)
            weekly_summaries.append({
                "week_start": current_week.strftime("%Y-%m-%d"),
                "total_activity": sum(week_report.daily_breakdown.values()),
                "top_activity": week_report.top_activities[0] if week_report.top_activities else None
            })
            current_week += timedelta(days=7)

        # 类别分布
        category_distribution = {}
        for date_key, activities in self.daily_activities.items():
            date = datetime.strptime(date_key, "%Y-%m-%d")
            if month_start <= date < month_end:
                for activity_type, duration in activities.items():
                    category_distribution[activity_type] = category_distribution.get(activity_type, 0) + duration

        # 归一化
        total = sum(category_distribution.values())
        if total > 0:
            category_distribution = {k: round(v / total * 100, 1) for k, v in category_distribution.items()}

        # 成长趋势（每周总活动时间）
        growth_trend = [s["total_activity"] for s in weekly_summaries]

        # 洞察
        insights = self._generate_insights(metrics, category_distribution, growth_trend)

        return MonthlyReport(
            month=month,
            year=year,
            metrics=metrics,
            weekly_summaries=weekly_summaries,
            category_distribution=category_distribution,
            growth_trend=growth_trend,
            insights=insights
        )

    def _generate_achievements(self, metrics: BehaviorMetrics) -> List[str]:
        """生成成就"""
        achievements = []

        if metrics.streak_days >= 7:
            achievements.append(f"连续活跃 {metrics.streak_days} 天")
        if metrics.total_learning_time >= 600:  # 10 hours
            achievements.append(f"学习时长超过 {int(metrics.total_learning_time / 60)} 小时")
        if metrics.goals_completed >= 5:
            achievements.append(f"完成 {metrics.goals_completed} 个目标")
        if metrics.total_memories_created >= 50:
            achievements.append(f"创建了 {metrics.total_memories_created} 条记忆")
        if metrics.total_chat_sessions >= 20:
            achievements.append(f"进行了 {metrics.total_chat_sessions} 次对话")

        return achievements

    def _generate_recommendations(self, metrics: BehaviorMetrics) -> List[str]:
        """生成建议"""
        recommendations = []

        if metrics.streak_days == 0:
            recommendations.append("开始你的第一个活跃日吧！")
        elif metrics.streak_days < 3:
            recommendations.append("保持连续活跃，建立习惯！")

        if metrics.total_learning_time < 120:  # 2 hours
            recommendations.append("增加学习时间，建议每天至少学习30分钟")

        if metrics.goals_created > metrics.goals_completed * 2:
            recommendations.append("你有未完成的目标，建议专注于完成现有目标")

        if metrics.peak_activity_hour < 6 or metrics.peak_activity_hour > 22:
            recommendations.append("注意作息时间，建议在正常时间段进行活动")

        if not recommendations:
            recommendations.append("继续保持良好的习惯！")

        return recommendations

    def _generate_insights(self, metrics: BehaviorMetrics, 
                           category_distribution: Dict[str, float],
                           growth_trend: List[float]) -> List[str]:
        """生成洞察"""
        insights = []

        # 活动类型分析
        if category_distribution:
            top_category = max(category_distribution.keys(), key=lambda k: category_distribution[k])
            insights.append(f"本月主要活动是 {top_category}，占比 {category_distribution[top_category]}%")

        # 成长趋势分析
        if len(growth_trend) >= 2:
            if growth_trend[-1] > growth_trend[0]:
                insights.append("活动时间呈上升趋势，继续保持！")
            elif growth_trend[-1] < growth_trend[0]:
                insights.append("活动时间有所下降，建议增加投入")

        # 目标完成率
        if metrics.goals_created > 0:
            completion_rate = metrics.goals_completed / metrics.goals_created * 100
            insights.append(f"目标完成率: {round(completion_rate, 1)}%")

        # 活跃度分析
        if metrics.active_days > 0:
            insights.append(f"本月活跃 {metrics.active_days} 天，日均活动 {round(metrics.avg_daily_activity, 1)} 分钟")

        return insights

    def get_activity_chart_data(self, days: int = 30) -> Dict[str, Any]:
        """获取活动图表数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        labels = []
        data = []

        current = start_date
        while current <= end_date:
            date_key = current.strftime("%Y-%m-%d")
            labels.append(current.strftime("%m/%d"))
            data.append(sum(self.daily_activities.get(date_key, {}).values()))
            current += timedelta(days=1)

        return {
            "labels": labels,
            "data": data,
            "total": sum(data),
            "average": round(sum(data) / len(data), 1) if data else 0
        }

    def get_category_breakdown(self, days: int = 30) -> Dict[str, Any]:
        """获取活动类别分解"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        category_totals = defaultdict(float)

        for session in self.sessions:
            if start_date <= session.start_time <= end_date:
                category_totals[session.activity_type] += session.duration_minutes

        total = sum(category_totals.values())
        
        return {
            "categories": dict(category_totals),
            "percentages": {k: round(v / total * 100, 1) if total > 0 else 0 
                          for k, v in category_totals.items()},
            "total_minutes": round(total, 1)
        }

    def get_hourly_distribution(self, days: int = 30) -> Dict[str, Any]:
        """获取每小时活动分布"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        hourly_counts = defaultdict(int)

        for session in self.sessions:
            if start_date <= session.start_time <= end_date:
                hourly_counts[session.start_time.hour] += 1

        # 填充缺失的小时
        for hour in range(24):
            if hour not in hourly_counts:
                hourly_counts[hour] = 0

        return {
            "labels": [f"{h:02d}:00" for h in range(24)],
            "data": [hourly_counts[h] for h in range(24)],
            "peak_hour": max(hourly_counts.keys(), key=lambda h: hourly_counts[h]) if hourly_counts else 0
        }
