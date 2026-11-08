"""Regression checks for persistent document-cache identity changes."""

import sqlite3
from pathlib import Path

import pytest

from lablens.ingestion.cache import DocumentCache


def test_reprocessed_source_replaces_its_old_document_id(tmp_path: Path) -> None:
    """A new version of one source must not leave the old ID authoritative."""
    database = tmp_path / "cache.db"
    cache = DocumentCache(database)
    cache.add_document("revision-1", "papers/study.pdf", "pdf")
    cache.add_document("revision-2", "papers/study.pdf", "pdf")

    reopened = DocumentCache(database)
    assert reopened.is_processed("revision-2")
    assert not reopened.is_processed("revision-1")
    assert reopened.get_document_source("revision-2") == "papers/study.pdf"
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM processed_documents"
        ).fetchone() == (1,)


def test_document_id_can_follow_a_renamed_source(tmp_path: Path) -> None:
    """Renaming a source with the same identity refreshes its metadata."""
    cache = DocumentCache(tmp_path / "cache.db")
    cache.add_document("document-1", "papers/before.pdf", "pdf")
    cache.add_document("document-1", "papers/after.pdf", "pdf")

    assert cache.get_document_source("document-1") == "papers/after.pdf"
    assert len(cache.to_dataframe()) == 1


def test_other_sources_survive_a_version_refresh(tmp_path: Path) -> None:
    """Refreshing one paper must preserve unrelated cached sources."""
    cache = DocumentCache(tmp_path / "cache.db")
    cache.add_document("first", "papers/first.pdf", "pdf")
    cache.add_document("other", "https://example.org/article", "url")
    cache.add_document("first-new", "papers/first.pdf", "pdf")

    assert cache.is_processed("other")
    assert cache.get_document_source("other") == "https://example.org/article"
    assert cache.is_processed("first-new")
    assert len(cache.to_dataframe()) == 2


def test_invalid_type_does_not_remove_existing_cache_entry(tmp_path: Path) -> None:
    """A rejected update must leave the previous valid document accessible."""
    cache = DocumentCache(tmp_path / "cache.db")
    cache.add_document("original", "papers/study.pdf", "pdf")

    with pytest.raises(ValueError, match="Invalid document_type"):
        cache.add_document("bad-update", "papers/study.pdf", "image")

    assert cache.is_processed("original")
    assert not cache.is_processed("bad-update")


def test_conflicting_identity_update_is_atomic(tmp_path: Path) -> None:
    """An ambiguous rename must not silently overwrite another document."""
    cache = DocumentCache(tmp_path / "cache.db")
    cache.add_document("first", "papers/first.pdf", "pdf")
    cache.add_document("second", "papers/second.pdf", "pdf")

    with pytest.raises(sqlite3.IntegrityError):
        cache.add_document("first", "papers/second.pdf", "pdf")

    assert cache.get_document_source("first") == "papers/first.pdf"
    assert cache.get_document_source("second") == "papers/second.pdf"
