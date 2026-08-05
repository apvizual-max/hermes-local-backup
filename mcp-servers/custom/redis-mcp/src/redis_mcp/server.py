"""
Redis MCP Server
Redis cache management, pub/sub, streams, and clustering.
"""

import asyncio
import json
import redis.asyncio as redis
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("redis-mcp")

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="key_get",
            description="Get key value",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="key_set",
            description="Set key value",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                    "ex": {"type": "integer", "description": "Expire in seconds"},
                    "px": {"type": "integer", "description": "Expire in milliseconds"},
                    "nx": {"type": "boolean", "default": False, "description": "Only set if not exists"},
                    "xx": {"type": "boolean", "default": False, "description": "Only set if exists"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "value"]
            },
        ),
        Tool(
            name="key_delete",
            description="Delete key(s)",
            inputSchema={
                "type": "object",
                "properties": {
                    "keys": {"type": "array", "items": {"type": "string"}},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["keys"]
            },
        ),
        Tool(
            name="key_exists",
            description="Check if key exists",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="key_expire",
            description="Set key expiration",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "seconds": {"type": "integer"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "seconds"]
            },
        ),
        Tool(
            name="key_ttl",
            description="Get key TTL",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="key_type",
            description="Get key type",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="keys_scan",
            description="Scan keys matching pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "default": "*"},
                    "count": {"type": "integer", "default": 100},
                    "db": {"type": "integer", "default": 0}
                },
                "required": []
            },
        ),
        Tool(
            name="hash_set",
            description="Set hash field(s)",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "field": {"type": "string"},
                    "value": {"type": "string"},
                    "mapping": {"type": "object", "description": "Multiple field-value pairs"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="hash_get",
            description="Get hash field(s)",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "field": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="hash_getall",
            description="Get all hash fields",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="list_push",
            description="Push to list",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "values": {"type": "array", "items": {"type": "string"}},
                    "side": {"type": "string", "enum": ["left", "right"], "default": "right"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "values"]
            },
        ),
        Tool(
            name="list_pop",
            description="Pop from list",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "side": {"type": "string", "enum": ["left", "right"], "default": "left"},
                    "count": {"type": "integer", "default": 1},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="list_range",
            description="Get list range",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "start": {"type": "integer", "default": 0},
                    "end": {"type": "integer", "default": -1},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="set_add",
            description="Add to set",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "values": {"type": "array", "items": {"type": "string"}},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "values"]
            },
        ),
        Tool(
            name="set_members",
            description="Get set members",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="sorted_set_add",
            description="Add to sorted set",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "members": {"type": "array", "items": {"type": "object", "properties": {"score": {"type": "number"}, "member": {"type": "string"}}}},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "members"]
            },
        ),
        Tool(
            name="sorted_set_range",
            description="Get sorted set range",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "start": {"type": "integer", "default": 0},
                    "end": {"type": "integer", "default": -1},
                    "with_scores": {"type": "boolean", "default": True},
                    "desc": {"type": "boolean", "default": False},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="stream_add",
            description="Add to stream",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "fields": {"type": "object"},
                    "maxlen": {"type": "integer"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "fields"]
            },
        ),
        Tool(
            name="stream_read",
            description="Read from stream",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "count": {"type": "integer", "default": 10},
                    "block": {"type": "integer"},
                    "last_id": {"type": "string", "default": "0-0"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="stream_consumer_group_create",
            description="Create consumer group",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "group": {"type": "string"},
                    "id": {"type": "string", "default": "0"},
                    "mkstream": {"type": "boolean", "default": True},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "group"]
            },
        ),
        Tool(
            name="stream_consumer_read",
            description="Read from consumer group",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "group": {"type": "string"},
                    "consumer": {"type": "string"},
                    "count": {"type": "integer", "default": 10},
                    "block": {"type": "integer"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["key", "group", "consumer"]
            },
        ),
        Tool(
            name="pubsub_publish",
            description="Publish to channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "message": {"type": "string"},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["channel", "message"]
            },
        ),
        Tool(
            name="pubsub_subscribe",
            description="Subscribe to channel (returns first message)",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "timeout": {"type": "integer", "default": 5},
                    "db": {"type": "integer", "default": 0}
                },
                "required": ["channel"]
            },
        ),
        Tool(
            name="info",
            description="Get Redis INFO",
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {"type": "string", "enum": ["all", "server", "clients", "memory", "persistence", "stats", "replication", "cpu", "commandstats", "cluster", "keyspace"]}
                },
                "required": []
            },
        ),
        Tool(
            name="config_get",
            description="Get config parameter",
            inputSchema={
                "type": "object",
                "properties": {
                    "parameter": {"type": "string", "default": "*"}
                },
                "required": []
            },
        ),
        Tool(
            name="config_set",
            description="Set config parameter",
            inputSchema={
                "type": "object",
                "properties": {
                    "parameter": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": ["parameter", "value"]
            },
        ),
        Tool(
            name="slowlog_get",
            description="Get slowlog entries",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {"type": "integer", "default": 10}
                },
                "required": []
            },
        ),
        Tool(
            name="memory_usage",
            description="Get memory usage for key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "samples": {"type": "integer", "default": 5}
                },
                "required": ["key"]
            },
        ),
        Tool(
            name="cluster_nodes",
            description="Get cluster nodes",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="cluster_slots",
            description="Get cluster slots",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="health_check",
            description="Health check",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "key_get":
            return await handle_key_get(arguments)
        elif name == "key_set":
            return await handle_key_set(arguments)
        elif name == "key_delete":
            return await handle_key_delete(arguments)
        elif name == "key_exists":
            return await handle_key_exists(arguments)
        elif name == "key_expire":
            return await handle_key_expire(arguments)
        elif name == "key_ttl":
            return await handle_key_ttl(arguments)
        elif name == "key_type":
            return await handle_key_type(arguments)
        elif name == "keys_scan":
            return await handle_keys_scan(arguments)
        elif name == "hash_set":
            return await handle_hash_set(arguments)
        elif name == "hash_get":
            return await handle_hash_get(arguments)
        elif name == "hash_getall":
            return await handle_hash_getall(arguments)
        elif name == "list_push":
            return await handle_list_push(arguments)
        elif name == "list_pop":
            return await handle_list_pop(arguments)
        elif name == "list_range":
            return await handle_list_range(arguments)
        elif name == "set_add":
            return await handle_set_add(arguments)
        elif name == "set_members":
            return await handle_set_members(arguments)
        elif name == "sorted_set_add":
            return await handle_sorted_set_add(arguments)
        elif name == "sorted_set_range":
            return await handle_sorted_set_range(arguments)
        elif name == "stream_add":
            return await handle_stream_add(arguments)
        elif name == "stream_read":
            return await handle_stream_read(arguments)
        elif name == "stream_consumer_group_create":
            return await handle_stream_consumer_group_create(arguments)
        elif name == "stream_consumer_read":
            return await handle_stream_consumer_read(arguments)
        elif name == "pubsub_publish":
            return await handle_pubsub_publish(arguments)
        elif name == "pubsub_subscribe":
            return await handle_pubsub_subscribe(arguments)
        elif name == "info":
            return await handle_info(arguments)
        elif name == "config_get":
            return await handle_config_get(arguments)
        elif name == "config_set":
            return await handle_config_set(arguments)
        elif name == "slowlog_get":
            return await handle_slowlog_get(arguments)
        elif name == "memory_usage":
            return await handle_memory_usage(arguments)
        elif name == "cluster_nodes":
            return await handle_cluster_nodes(arguments)
        elif name == "cluster_slots":
            return await handle_cluster_slots(arguments)
        elif name == "health_check":
            return await handle_health_check(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER ====================

_redis_client = None

async def get_redis_client(db: int = 0):
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=db,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
    return _redis_client


async def get_redis_db(db: int) -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=db,
        password=REDIS_PASSWORD,
        decode_responses=True
    )


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_key_get(args: Dict) -> List[TextContent]:
    req = KeyGetRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        value = await client.get(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "value": value}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_set(args: Dict) -> List[TextContent]:
    req = KeySetRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        result = await client.set(
            req.key, req.value,
            ex=req.ex, px=req.px, nx=req.nx, xx=req.xx
        )
        return [TextContent(type="text", text=json.dumps({"status": "SET" if result else "NOT_SET", "key": req.key}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_delete(args: Dict) -> List[TextContent]:
    req = KeyDeleteRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        deleted = await client.delete(*req.keys)
        return [TextContent(type="text", text=json.dumps({"deleted": deleted, "keys": req.keys}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_exists(args: Dict) -> List[TextContent]:
    req = KeyExistsRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        exists = await client.exists(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "exists": bool(exists)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_expire(args: Dict) -> List[TextContent]:
    req = KeyExpireRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        result = await client.expire(req.key, req.seconds)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "expired": bool(result)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_ttl(args: Dict) -> List[TextContent]:
    req = KeyTTLRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        ttl = await client.ttl(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "ttl": ttl}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_key_type(args: Dict) -> List[TextContent]:
    req = KeyTypeRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        key_type = await client.type(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "type": key_type}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_keys_scan(args: Dict) -> List[TextContent]:
    req = KeysScanRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        keys = []
        async for key in client.scan_iter(match=req.pattern, count=req.count):
            keys.append(key)
            if len(keys) >= req.count:
                break
        return [TextContent(type="text", text=json.dumps({"pattern": req.pattern, "keys": keys, "count": len(keys)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_hash_set(args: Dict) -> List[TextContent]:
    req = HashSetRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        if req.mapping:
            result = await client.hset(req.key, mapping=req.mapping)
        else:
            result = await client.hset(req.key, req.field, req.value)
        return [TextContent(type="text", text=json.dumps({"fields_set": result, "key": req.key}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_hash_get(args: Dict) -> List[TextContent]:
    req = HashGetRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        value = await client.hget(req.key, req.field)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "field": req.field, "value": value}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_hash_getall(args: Dict) -> List[TextContent]:
    req = HashGetAllRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        result = await client.hgetall(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "data": result}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_push(args: Dict) -> List[TextContent]:
    req = ListPushRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        if req.side == "left":
            length = await client.lpush(req.key, *req.values)
        else:
            length = await client.rpush(req.key, *req.values)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "length": length, "pushed": len(req.values)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_pop(args: Dict) -> List[TextContent]:
    req = ListPopRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        if req.side == "left":
            if req.count == 1:
                value = await client.lpop(req.key)
                return [TextContent(type="text", text=json.dumps({"key": req.key, "value": value}, indent=2))]
            else:
                values = await client.lpop(req.key, count=req.count)
                return [TextContent(type="text", text=json.dumps({"key": req.key, "values": values}, indent=2))]
        else:
            if req.count == 1:
                value = await client.rpop(req.key)
                return [TextContent(type="text", text=json.dumps({"key": req.key, "value": value}, indent=2))]
            else:
                values = await client.rpop(req.key, count=req.count)
                return [TextContent(type="text", text=json.dumps({"key": req.key, "values": values}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_range(args: Dict) -> List[TextContent]:
    req = ListRangeRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        values = await client.lrange(req.key, req.start, req.end)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "values": values, "count": len(values)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_set_add(args: Dict) -> List[TextContent]:
    req = SetAddRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        added = await client.sadd(req.key, *req.values)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "added": added}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_set_members(args: Dict) -> List[TextContent]:
    req = SetMembersRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        members = await client.smembers(req.key)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "members": list(members)}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_sorted_set_add(args: Dict) -> List[TextContent]:
    req = SortedSetAddRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        mapping = {m["member"]: m["score"] for m in req.members}
        added = await client.zadd(req.key, mapping)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "added": added}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_sorted_set_range(args: Dict) -> List[TextContent]:
    req = SortedSetRangeRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        if req.desc:
            result = await client.zrevrange(req.key, req.start, req.end, withscores=req.with_scores)
        else:
            result = await client.zrange(req.key, req.start, req.end, withscores=req.with_scores)
        
        if req.with_scores:
            formatted = [{"member": m, "score": s} for m, s in result]
        else:
            formatted = list(result)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "results": formatted}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_stream_add(args: Dict) -> List[TextContent]:
    req = StreamAddRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        msg_id = await client.xadd(req.key, req.fields, maxlen=req.maxlen)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "id": msg_id}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_stream_read(args: Dict) -> List[TextContent]:
    req = StreamReadRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        streams = {req.key: req.last_id}
        result = await client.xread(streams, count=req.count, block=req.block)
        return [TextContent(type="text", text=json.dumps({"results": result}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_stream_consumer_group_create(args: Dict) -> List[TextContent]:
    req = StreamConsumerGroupCreateRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        await client.xgroup_create(req.key, req.group, id=req.id, mkstream=req.mkstream)
        return [TextContent(type="text", text=json.dumps({"status": "CREATED", "key": req.key, "group": req.group}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_stream_consumer_read(args: Dict) -> List[TextContent]:
    req = StreamConsumerReadRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        streams = {req.key: ">"}
        result = await client.xreadgroup(req.group, req.consumer, streams=streams, count=req.count, block=req.block)
        return [TextContent(type="text", text=json.dumps({"results": result}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_pubsub_publish(args: Dict) -> List[TextContent]:
    req = PubSubPublishRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        subscribers = await client.publish(req.channel, req.message)
        return [TextContent(type="text", text=json.dumps({"channel": req.channel, "subscribers": subscribers}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_pubsub_subscribe(args: Dict) -> List[TextContent]:
    req = PubSubSubscribeRequest(**arguments)
    client = await get_redis_db(req.db)
    try:
        pubsub = client.pubsub()
        await pubsub.subscribe(req.channel)
        message = await pubsub.get_message(timeout=req.timeout)
        await pubsub.unsubscribe(req.channel)
        await pubsub.close()
        return [TextContent(type="text", text=json.dumps({"channel": req.channel, "message": message}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_info(args: Dict) -> List[TextContent]:
    req = InfoRequest(**arguments)
    client = await get_redis_db()
    try:
        if req.section:
            result = await client.info(req.section)
        else:
            result = await client.info()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_config_get(args: Dict) -> List[TextContent]:
    req = ConfigGetRequest(**arguments)
    client = await get_redis_db()
    try:
        result = await client.config_get(req.parameter)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_config_set(args: Dict) -> List[TextContent]:
    req = ConfigSetRequest(**arguments)
    client = await get_redis_db()
    try:
        await client.config_set(req.parameter, req.value)
        return [TextContent(type="text", text=json.dumps({"status": "SET", "parameter": req.parameter}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_slowlog_get(args: Dict) -> List[TextContent]:
    req = SlowLogGetRequest(**arguments)
    client = await get_redis_db()
    try:
        entries = await client.slowlog_get(req.count)
        formatted = []
        for entry in entries:
            formatted.append({
                "id": entry["id"],
                "timestamp": entry["start_time"],
                "duration_us": entry["duration"],
                "command": entry["command"]
            })
        return [TextContent(type="text", text=json.dumps(formatted, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_memory_usage(args: Dict) -> List[TextContent]:
    req = MemoryUsageRequest(**arguments)
    client = await get_redis_db()
    try:
        usage = await client.memory_usage(req.key, samples=req.samples)
        return [TextContent(type="text", text=json.dumps({"key": req.key, "bytes": usage}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_cluster_nodes(args: Dict) -> List[TextContent]:
    client = await get_redis_db()
    try:
        nodes = await client.cluster_nodes()
        return [TextContent(type="text", text=json.dumps({"nodes": nodes}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_cluster_slots(args: Dict) -> List[TextContent]:
    client = await get_redis_db()
    try:
        slots = await client.cluster_slots()
        return [TextContent(type="text", text=json.dumps(slots, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health_check(args: Dict) -> List[TextContent]:
    client = await get_redis_db()
    try:
        result = await client.ping()
        return [TextContent(type="text", text=json.dumps({"healthy": result, "status": "OK" if result else "FAIL"}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"healthy": False, "error": str(e)}, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
