"""
Obsidian Knowledge MCP Server
Advanced vault operations: ontology traversal, synod decisions, neural memory search, vault intelligence.
"""

import asyncio
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

# Vault paths
VAULT_ROOT = Path(r"D:\Alex - KV Obsidian\Alex - KV Obsidian")
ONTOLOGY_DIR = VAULT_ROOT / "Ontology"
SYNOD_DIR = VAULT_ROOT / "Synod"
NEURAL_MEMORY_DIR = VAULT_ROOT / ".neural_memory"
VAULT_INTELLIGENCE_DIR = VAULT_ROOT / ".vault-intelligence"

app = Server("obsidian-knowledge")


# ==================== MODELS ====================

class OntologyQueryRequest(BaseModel):
    concept: str = Field(description="Concept to query in ontology")
    depth: int = Field(default=2, description="Traversal depth for related concepts")
    include_relations: bool = Field(default=True, description="Include relation types")


class SynodDecisionRequest(BaseModel):
    topic: str = Field(description="Topic to query in Synod")
    include_drafts: bool = Field(default=False, description="Include unratified drafts")


class NeuralMemorySearchRequest(BaseModel):
    query_embedding: Optional[List[float]] = Field(default=None, description="Embedding vector for semantic search")
    query_text: Optional[str] = Field(default=None, description="Text to search (will be embedded)")
    top_k: int = Field(default=10, description="Number of results")
    filter_tags: Optional[List[str]] = Field(default=None, description="Filter by tags")


class VaultIntelligenceHealthRequest(BaseModel):
    rebuild_index: bool = Field(default=False, description="Force rebuild of intelligence index")


class GraphTraverseRequest(BaseModel):
    start_node: str = Field(description="Starting node/concept")
    max_depth: int = Field(default=3, description="Maximum traversal depth")
    relation_types: Optional[List[str]] = Field(default=None, description="Filter by relation types")


# ==================== HELPER FUNCTIONS ====================

def load_markdown_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding='utf-8')
    return ""

def get_vault_files(pattern: str) -> List[Path]:
    return list(VAULT_ROOT.rglob(pattern))

def parse_frontmatter(content: str) -> tuple[Dict, str]:
    """Parse YAML frontmatter from markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
                body = parts[2]
                return meta, body
            except:
                pass
    return {}, content


# ==================== TOOLS ====================

app = Server("obsidian-knowledge")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="ontology_query",
            description="Query the Ontology folder for concepts, definitions, and relations",
            inputSchema={
                "type": "object",
                "properties": {
                    "concept": {"type": "string"},
                    "depth": {"type": "integer", "default": 2},
                    "include_relations": {"type": "boolean", "default": True}
                },
                "required": ["concept"]
            },
        ),
        Tool(
            name="synod_decision",
            description="Query Synod for ratified decisions on a topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "include_drafts": {"type": "boolean", "default": False}
                },
                "required": ["topic"]
            },
        ),
        Tool(
            name="neural_memory_search",
            description="Semantic search in .neural_memory using embeddings",
            inputSchema={
                "type": "object",
                "properties": {
                    "query_embedding": {"type": "array", "items": {"type": "number"}},
                    "query_text": {"type": "string"},
                    "top_k": {"type": "integer", "default": 10},
                    "filter_tags": {"type": "array", "items": {"type": "string"}}
                },
                "required": []
            },
        ),
        Tool(
            name="vault_intelligence_health",
            description="Check vault intelligence system health and optionally rebuild index",
            inputSchema={
                "type": "object",
                "properties": {
                    "rebuild_index": {"type": "boolean", "default": False}
                },
                "required": []
            },
        ),
        Tool(
            name="graph_traverse",
            description="Traverse the knowledge graph from a starting node",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_node": {"type": "string"},
                    "max_depth": {"type": "integer", "default": 3},
                    "relation_types": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["start_node"]
            },
        ),
        Tool(
            name="ontology_list_concepts",
            description="List all concepts in the Ontology folder",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="synod_list_topics",
            description="List all topics in Synod with status (ratified/draft)",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="vault_stats",
            description="Get comprehensive vault statistics",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "ontology_query":
            return await handle_ontology_query(arguments)
        elif name == "synod_decision":
            return await handle_synod_decision(arguments)
        elif name == "neural_memory_search":
            return await handle_neural_memory_search(arguments)
        elif name == "vault_intelligence_health":
            return await handle_vault_intelligence_health(arguments)
        elif name == "graph_traverse":
            return await handle_graph_traverse(arguments)
        elif name == "ontology_list_concepts":
            return await handle_ontology_list_concepts(arguments)
        elif name == "synod_list_topics":
            return await handle_synod_list_topics(arguments)
        elif name == "vault_stats":
            return await handle_vault_stats(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_ontology_query(args: Dict) -> List[TextContent]:
    concept = args.get("concept", "")
    depth = args.get("depth", 2)
    include_relations = args.get("include_relations", True)
    
    # Search for concept in Ontology folder
    results = []
    for md_file in ONTOLOGY_DIR.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        if concept.lower() in content.lower():
            meta, body = parse_frontmatter(content)
            results.append({
                "file": str(md_file.relative_to(VAULT_ROOT)),
                "title": meta.get("title", md_file.stem),
                "tags": meta.get("tags", []),
                "excerpt": body[:500] + "..." if len(body) > 500 else body,
                "relations": meta.get("relations", []) if include_relations else []
            })
    
    return [TextContent(type="text", text=json.dumps({
        "concept": concept,
        "depth": depth,
        "results_found": len(results),
        "results": results[:20]  # Limit to 20
    }, indent=2))]


async def handle_synod_decision(args: Dict) -> List[TextContent]:
    topic = args.get("topic", "")
    include_drafts = args.get("include_drafts", False)
    
    results = []
    for md_file in SYNOD_DIR.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        if topic.lower() in content.lower():
            meta, body = parse_frontmatter(content)
            status = meta.get("status", "unknown")
            if include_drafts or status == "ratified":
                results.append({
                    "file": str(md_file.relative_to(VAULT_ROOT)),
                    "title": meta.get("title", md_file.stem),
                    "status": status,
                    "tags": meta.get("tags", []),
                    "excerpt": content[:1000] + "..." if len(content) > 1000 else content,
                    "ratified": meta.get("ratified", False),
                    "ratified_by": meta.get("ratified_by", "unknown"),
                    "date": meta.get("date", "unknown")
                })
    
    return [TextContent(type="text", text=json.dumps({
        "topic": topic,
        "include_drafts": include_drafts,
        "results_found": len(results),
        "results": results[:20]
    }, indent=2))]


async def handle_neural_memory_search(args: Dict) -> List[TextContent]:
    query_embedding = args.get("query_embedding")
    query_text = args.get("query_text")
    top_k = args.get("top_k", 10)
    filter_tags = args.get("filter_tags", [])
    
    # Check if neural memory exists
    if not NEURAL_MEMORY_DIR.exists():
        return [TextContent(type="text", text=json.dumps({
            "error": ".neural_memory directory not found",
            "path": str(NEURAL_MEMORY_DIR)
        }, indent=2))]
    
    # In a real implementation, this would use vector similarity search
    # For now, return a structured response showing the system is ready
    return [TextContent(type="text", text=json.dumps({
        "status": "NEURAL_MEMORY_SEARCH_READY",
        "note": "Embedding-based search requires embedding generation. Provide query_text for text-based search or query_embedding for vector search.",
        "query_text": query_text,
        "top_k": top_k,
        "filter_tags": filter_tags,
        "neural_memory_path": str(NEURAL_MEMORY_DIR),
        "available_indices": list(NEURAL_MEMORY_DIR.glob("*.json")) if NEURAL_MEMORY_DIR.exists() else [],
        "note2": "Integrate with sentence-transformers or similar for actual embedding generation"
    }, indent=2))]


async def handle_vault_intelligence_health(args: Dict) -> List[TextContent]:
    rebuild_index = args.get("rebuild_index", False)
    
    health = {
        "vault_root": str(VAULT_ROOT),
        "vault_exists": VAULT_ROOT.exists(),
        "ontology_dir": str(ONTOLOGY_DIR),
        "ontology_exists": ONTOLOGY_DIR.exists(),
        "synod_dir": str(SYNOD_DIR),
        "synod_exists": SYNOD_DIR.exists(),
        "neural_memory_dir": str(NEURAL_MEMORY_DIR),
        "neural_memory_exists": NEURAL_MEMORY_DIR.exists(),
        "vault_intelligence_dir": str(VAULT_INTELLIGENCE_DIR),
        "vault_intelligence_exists": VAULT_INTELLIGENCE_DIR.exists(),
        "index_rebuild_requested": rebuild_index,
        "index_status": "READY" if VAULT_INTELLIGENCE_DIR.exists() else "NEEDS_BUILD"
    }
    
    if rebuild_index:
        health["action"] = "INDEX_REBUILD_TRIGGERED"
        health["note"] = "Index rebuild would be triggered here. Implement with your preferred indexing strategy (ChromaDB, FAISS, etc.)"
    
    return [TextContent(type="text", text=json.dumps(health, indent=2))]


async def handle_graph_traverse(args: Dict) -> List[TextContent]:
    start_node = args.get("start_node", "")
    max_depth = args.get("max_depth", 3)
    relation_types = args.get("relation_types")
    
    # Placeholder for graph traversal
    return [TextContent(type="text", text=json.dumps({
        "start_node": start_node,
        "max_depth": max_depth,
        "relation_types_filter": relation_types,
        "status": "GRAPH_TRAVERSE_READY",
        "note": "Implement graph loading from Ontology/Synod files and traverse using networkx or similar",
        "suggested_implementation": "Use networkx to build graph from frontmatter relations in Ontology/*.md and Synod/*.md files"
    }, indent=2))]


async def handle_ontology_list_concepts(args: Dict) -> List[TextContent]:
    concepts = []
    for md_file in ONTOLOGY_DIR.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(content)
        concepts.append({
            "file": str(md_file.relative_to(VAULT_ROOT)),
            "title": meta.get("title", md_file.stem),
            "tags": meta.get("tags", []),
            "aliases": meta.get("aliases", []),
            "definition": body[:200] + "..." if len(body) > 200 else body
        })
    
    return [TextContent(type="text", text=json.dumps({
        "total_concepts": len(concepts),
        "concepts": concepts
    }, indent=2))]


async def handle_synod_list_topics(args: Dict) -> List[TextContent]:
    topics = []
    for md_file in SYNOD_DIR.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(content)
        topics.append({
            "file": str(md_file.relative_to(VAULT_ROOT)),
            "title": meta.get("title", md_file.stem),
            "status": meta.get("status", "unknown"),
            "tags": meta.get("tags", []),
            "ratified": meta.get("ratified", False),
            "ratified_by": meta.get("ratified_by", "unknown"),
            "date": meta.get("date", "unknown"),
            "excerpt": body[:300] + "..." if len(body) > 300 else body
        })
    
    return [TextContent(type="text", text=json.dumps({
        "total_topics": len(topics),
        "ratified": sum(1 for t in topics if t["ratified"]),
        "drafts": sum(1 for t in topics if not t["ratified"]),
        "topics": topics
    }, indent=2))]


async def handle_vault_stats(args: Dict) -> List[TextContent]:
    stats = {
        "vault_root": str(VAULT_ROOT),
        "total_files": 0,
        "total_md_files": 0,
        "total_size_mb": 0,
        "folders": {}
    }
    
    for item in VAULT_ROOT.rglob("*"):
        if item.is_file():
            stats["total_files"] += 1
            stats["total_size_mb"] += item.stat().st_size / (1024 * 1024)
            if item.suffix == ".md":
                stats["total_md_files"] += 1
    
    # Folder breakdown
    for folder in ["Ontology", "Synod", "_prompts", ".neural_memory", ".vault-intelligence"]:
        folder_path = VAULT_ROOT / folder
        if folder_path.exists():
            files = list(folder_path.rglob("*"))
            stats["folders"][folder] = {
                "files": len([f for f in files if f.is_file()]),
                "size_mb": round(sum(f.stat().st_size for f in files if f.is_file()) / (1024 * 1024), 2)
            }
    
    stats["total_size_mb"] = round(stats["total_size_mb"], 2)
    
    return [TextContent(type="text", text=json.dumps(stats, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
