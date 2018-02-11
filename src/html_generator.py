from yattag import Doc

from src.dashboard_node import DashboardNode, NodeType
from src.tools import secs_to_str, weekdays_str, EmptyContext

HTML_STYLE = """
table, th, td {
   border: 1px solid black;
   border-collapse: collapse;
   padding: 3px;
} 
div.main {background:white;width:1024px;right: 0;left: 0;margin-right: auto;margin-left: auto;} 
"""


def _add_tag_sequence(tag_method, text_method, tag: str, texts: list) -> None:
    for text in texts:
        with tag_method(tag):
            text_method(text)


def _build_leaf(tag_method, text_method, leaf: DashboardNode) -> None:
    day_goal_secs = leaf.day_goal * 60 if leaf.day_goal is not None else 0
    week_goal_secs = leaf.week_goal * 60 if leaf.week_goal is not None else 0
    day_goal_str = secs_to_str(day_goal_secs) if day_goal_secs > 0 else "-"
    week_goal_str = secs_to_str(week_goal_secs) if week_goal_secs > 0 else "-"

    with tag_method("tr"):
        with tag_method("td"):
            with (tag_method("a", href=leaf.link) if leaf.link is not None else EmptyContext()):
                with (tag_method("strike")
                      if leaf.day_time >= day_goal_secs > 0 or leaf.week_time >= week_goal_secs > 0
                      else EmptyContext()):
                    text_method(leaf.name)

        last_time_str = leaf.last_time.strftime("%a %d %b  %H:%M") if leaf.last_time is not None else "-"
        days_this_week_list = [weekdays_str[day] for day in leaf.week_days]
        if len(days_this_week_list) > 0:
            days_this_week_str = "{}: {}".format(len(days_this_week_list), ", ".join(days_this_week_list))
        else:
            days_this_week_str = "-"

        _add_tag_sequence(tag_method, text_method, "td",
                          [secs_to_str(leaf.day_time), day_goal_str,
                           secs_to_str(leaf.week_time), week_goal_str,
                           days_this_week_str, last_time_str])


def _build_node(doc, tag_method, text_method, node: DashboardNode, path: str) -> None:
    if node.node_type == NodeType.LEAF:
        _build_leaf(tag_method, text_method, node)
    else:
        if node.have_children_leafs():
            doc.stag("br")
            text_method("{} {}".format(path + " -> " if len(path) > 0 else "", node.name))
        with tag_method("table"):
            if node.have_children_stats():
                with tag_method('tr'):
                    _add_tag_sequence(tag_method, text_method, "th",
                                      ["Name", "Today", "Daily goal", "This week",
                                       "Weekly goal", "Days this week", "Last time"])
            for child in node.children:
                _build_node(doc, tag_method, text_method, child,
                            path="{} {}".format(path + " -> " if len(path) > 0 else "", node.name))


def get_html(node: DashboardNode) -> str:
    doc, tag_method, text_method = Doc().tagtext()

    with tag_method("html"):
        with tag_method("body"), tag_method("div", klass="main"):
            text_method("Select the queue depending on the mood/energy level")
            doc.stag("br")
            with tag_method("style"):
                text_method(HTML_STYLE)
            _build_node(doc, tag_method, text_method, node, path="")

    return doc.getvalue()
