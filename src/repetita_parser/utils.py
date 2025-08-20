def is_comment_line(line: str) -> bool:
    """Check if a line is a comment (starts with # after optional whitespace)"""
    return line.strip().startswith("#")


def has_inline_comment(line: str) -> bool:
    """Check if a line has an inline comment (# appears after other content)"""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    return "#" in stripped
