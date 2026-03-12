"""
Root-level conftest.py — re-exports all shared fixtures from tests/conftest.py
so that pytest discovers them for tests in any app subdirectory (e.g. comments/tests/).
"""

from tests.conftest import (  # noqa: F401 — re-export for pytest fixture discovery
    EditionFactory,
    PhotoFactory,
    VideoFactory,
    CommentFactory,
    HomePageContentFactory,
    RulesPageContentFactory,
    edition,
    photo,
    video,
    comment,
    homepage_content,
    rules_content,
    client,
    api_client,
)
