import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Literal

import pandas as pd


class DocumentCache:
    def __init__(
        self, db_path: str | Path = ".lablens_cache/processed_docs.db"
    ) -> None:
        """Initialize the document cache

        Args:
            db_path: The path to the database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _create_table(self) -> None:
        """Create the processed_documents table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_documents (
                    document_id TEXT PRIMARY KEY,
                    document_source TEXT UNIQUE,
                    document_type TEXT CHECK(document_type IN ('url', 'pdf')),
                    processed_at TEXT
                )
                """
            )

    def is_processed(self, document_id: str) -> bool:
        """Check if a document has been processed

        Args:
            document_id: The ID of the document to check

        Returns:
            bool: True if the document has been processed, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM processed_documents WHERE document_id = ?",
                (document_id,),
            )
            return cursor.fetchone() is not None

    def get_document_source(self, document_id: str) -> str | None:
        """Get the document source for a given document_id. Returns None if not found"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT document_source FROM processed_documents WHERE document_id = ?",
                (document_id,),
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def add_document(
        self,
        document_id: str,
        document_source: str,
        document_type: Literal["url", "pdf"],
    ) -> None:
        """Add or refresh a processed document in the cache.

        A reprocessed source replaces its previous document ID. Reusing an ID
        for a renamed source refreshes its metadata. Conflicting identities
        raise ``sqlite3.IntegrityError`` and leave the transaction unchanged.

        Args:
            document_id: The ID of the document to add.
            document_source: The source of the document to add (URL or file path).
            document_type: The type of the document to add (url or pdf).
        """
        if document_type not in ("url", "pdf"):
            raise ValueError("Invalid document_type. Use 'url' or 'pdf'.")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO processed_documents
                (document_id, document_source, document_type, processed_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(document_id) DO UPDATE SET
                    document_source = excluded.document_source,
                    document_type = excluded.document_type,
                    processed_at = excluded.processed_at
                ON CONFLICT(document_source) DO UPDATE SET
                    document_id = excluded.document_id,
                    document_type = excluded.document_type,
                    processed_at = excluded.processed_at
                """,
                (
                    document_id,
                    document_source,
                    document_type,
                    datetime.now().isoformat(),
                ),
            )

    def remove_document(self, document_id: str) -> bool:
        """Remove a document from the cache.

        Args:
            document_id: The ID of the document to remove.

        Returns:
            True if document was removed, False if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM processed_documents WHERE document_id = ?", (document_id,)
            )
            return cursor.rowcount > 0

    def to_dataframe(self) -> pd.DataFrame:
        """Retrieve all processed documents as a pandas DataFrame.

        Returns:
            pd.DataFrame: A pandas DataFrame containing all processed documents.
        """
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(
                "SELECT * FROM processed_documents ORDER BY processed_at DESC", conn
            )

    def clear(self) -> None:
        """Clear the cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM processed_documents")
            conn.commit()
