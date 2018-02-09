from yattag import Doc

from src.dashboard_node import DashboardNode, NodeType
from src.tools import secs_to_str


def _build_leaf_text(tag_method, text_method, leaf: DashboardNode) -> None:
    leaf.week_days = set()
    leaf.last_time = None

    day_goal_secs = leaf.day_goal * 60 if leaf.day_goal is not None else 0
    week_goal_secs = leaf.week_goal * 60 if leaf.week_goal is not None else 0

    text = "{name}: D:{time_today}/{day_goal} W:{time_week}/{week_goal}"\
        .format(name=leaf.name,
                time_today=secs_to_str(leaf.day_time), day_goal=day_goal_secs,
                time_week=secs_to_str(leaf.week_time), week_goal=week_goal_secs)
    if leaf.day_time >= day_goal_secs > 0:
        with tag_method("strike"):
            text_method(text)
    else:
        text_method(text)


def _build_leaf(tag_method, text_method, leaf: DashboardNode) -> None:
    if leaf.link is not None:
        with tag_method("a", href=leaf.link):
            _build_leaf_text(tag_method, text_method, leaf)
    else:
        _build_leaf_text(tag_method, text_method, leaf)


def _build_node(tag_method, text_method, node: DashboardNode) -> None:
    if node.node_type == NodeType.LEAF:
        with tag_method('li'):
            _build_leaf(tag_method, text_method, node)
    else:
        text_method(node.name)
        if node.children is not None and len(node.children) > 0:
            with tag_method('ul'):
                for child in node.children:
                    _build_node(tag_method, text_method, child)


def get_html(node: DashboardNode) -> str:
    doc, tag_method, text_method = Doc().tagtext()

    with tag_method('html'):
        with tag_method('body'):
            with tag_method('ul'):
                with tag_method('li'):
                    _build_node(tag_method, text_method, node)

    return doc.getvalue()
