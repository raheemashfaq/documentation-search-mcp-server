import trafilatura


def clean_html_to_text(html: str) -> str:
    try:
        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            favor_recall=False
        )

        return text or ""

    except Exception:
        raise