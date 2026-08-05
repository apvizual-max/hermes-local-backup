# Indexing Header Format (used in Sentinel system)

Each core document begins with an indexing header block composed of comment lines (starting with #) that provide metadata and cross‑references.

Standard fields:
- # ID: <filename> – unique identifier.
- # PURPOSE: short description of the document’s role.
- # USAGE: how to read/use the document.
- # ROLE: which Sentinel instance/profile owns it.
- # CHAIN: MEMORIE → Jurnal → Indexing → RAG (fixed for all).
- # TAGS: #[MEMORIE] #[JURNAL] #[INDEXARE] #[RAG] (fixed).
- # CROSS-REFERENCES: list of related files to consult for full understanding.
- A separator line "--" after the header before the main content.

Example:
# INDEXING HEADER
# ID: SOUL.md
# PURPOSE: Operational identity contract for Sentinel Default (paired with CONSTINTA.md)
# USAGE: Read first, then CONSTINTA.md for logical‑strategic‑rational order of life.
# ROLE: Sentinel Default – Orchestrator (DEFAULT)
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[MEMORIE] #[JURNAL] #[INDEXARE] #[RAG]
#
# CROSS-REFERENCES
# This document is part of a set. For optimal understanding, also refer to:
# - CONSTINTA.md: the ontological definition of consciousness (pair with SOUL.md).
# - SENTINEL_JOURNAL.md: operational map of Optimus Prime memory; source‑linked vector index for RAG retrieval.
# - SESSION_REPORT_JOURNAL_OGLINDA-CASA.md: mental map and indexing guide for current session.
# - JURNAL_OGLINDA.md: opinion journal of other AIs about this entity.
# - SACRED_DEFINITIONS.md: axiomatic basis of the Triple Crunch algorithm.
# --