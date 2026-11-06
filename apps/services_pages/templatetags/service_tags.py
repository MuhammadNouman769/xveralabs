"""{{ text|richtext }}: turns dashboard-managed text into safe HTML.
Everything is HTML-escaped first, so nobody can inject scripts. Only the markup below is converted."""
import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+|/[^\s)]*|#[^\s)]*|mailto:[^\s)]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_OL = re.compile(r"^\d+[.)]\s+(.*)")


def _inline(s):
    s = escape(s)
    s = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return _BOLD.sub(r"<strong>\1</strong>", s)


@register.filter
def richtext(value):
    out, para, items, kind = [], [], [], None

    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        nonlocal kind
        if items:
            out.append(f"<{kind}>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + f"</{kind}>")
            items.clear()
        kind = None

    for raw in (value or "").replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line:
            flush_para(); flush_list(); continue
        if line.startswith("## "):
            flush_para(); flush_list(); out.append("<h3>" + _inline(line[3:]) + "</h3>"); continue
        if line.startswith(("- ", "* ")):
            flush_para()
            if kind != "ul":
                flush_list(); kind = "ul"
            items.append(line[2:]); continue
        m = _OL.match(line)
        if m:
            flush_para()
            if kind != "ol":
                flush_list(); kind = "ol"
            items.append(m.group(1)); continue
        flush_list(); para.append(line)
    flush_para(); flush_list()
    return mark_safe("".join(out))