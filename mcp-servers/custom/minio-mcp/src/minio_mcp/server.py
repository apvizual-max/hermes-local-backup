"""
MinIO MCP Server
MinIO/S3-compatible object storage management.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("minio-mcp")


# ==================== MODELS ====================

class BucketCreateRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    region: str = Field(default="us-east-1", description="Region")
    object_lock: bool = Field(default=False, description="Enable object lock")


class BucketRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    force: bool = Field(default=False, description="Force delete (delete all objects first)")


class BucketPolicyRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    policy: Dict[str, Any] = Field(description="Bucket policy document")


class BucketLifecycleRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    rules: List[Dict[str, Any]] = Field(description="Lifecycle rules")


class BucketReplicationRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    role: str = Field(description="IAM role ARN")
    rules: List[Dict[str, Any]] = Field(description="Replication rules")


class BucketNotificationRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    topic: str = Field(description="Topic ARN")
    events: List[str] = Field(description="Event types")
    filter_prefix: str = Field(default="", description="Key prefix filter")
    filter_suffix: str = Field(default="", description="Key suffix filter")


class ObjectListRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    prefix: str = Field(default="", description="Key prefix")
    delimiter: str = Field(default="/", description="Delimiter")
    max_keys: int = Field(default=1000, description="Max keys")
    continuation_token: Optional[str] = Field(default=None, description="Continuation token")


class ObjectGetRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    version_id: Optional[str] = Field(default=None, description="Specific version")


class ObjectPutRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    body: str = Field(description="Object body")
    content_type: Optional[str] = Field(default=None, description="Content type")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="User metadata")


class ObjectDeleteRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    version_id: Optional[str] = Field(default=None, description="Specific version")


class ObjectCopyRequest(BaseModel):
    source_bucket: str = Field(description="Source bucket")
    source_key: str = Field(description="Source key")
    dest_bucket: str = Field(description="Destination bucket")
    dest_key: str = Field(description="Destination key")


class PresignedUrlRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    method: str = Field(default="GET", description="HTTP method")
    expires_in: int = Field(default=3600, description="Expiration in seconds")


class MultipartUploadInitRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    content_type: str = Field(default="application/octet-stream", description="Content type")


class MultipartUploadPartRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    upload_id: str = Field(description="Upload ID")
    part_number: int = Field(description="Part number")
    body: str = Field(description="Part body")


class MultipartUploadCompleteRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    upload_id: str = Field(description="Upload ID")
    parts: List[Dict[str, Any]] = Field(description="Parts list")


class MultipartUploadAbortRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    upload_id: str = Field(description="Upload ID")


class VersioningRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    status: str = Field(description="Status: Enabled, Suspended")


class VersionsListRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    prefix: str = Field(default="", description="Key prefix")
    max_versions: int = Field(default=1000, description="Max versions")


class ACLRequest(BaseModel):
    bucket: str = Field(description="Bucket name")
    key: str = Field(description="Object key")
    acl: str = Field(description="ACL: private, public-read, public-read-write, authenticated-read, aws-exec-read, bucket-owner-read, bucket-owner-full-control")


# ==================== SERVER ====================

app = Server("minio-mcp")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="bucket_list",
            description="List all buckets",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="bucket_create",
            description="Create a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "region": {"type": "string", "default": "us-east-1"},
                    "object_lock": {"type": "boolean", "default": False}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_delete",
            description="Delete a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "force": {"type": "boolean", "default": False}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_policy_get",
            description="Get bucket policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_policy_set",
            description="Set bucket policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "policy": {"type": "object"}
                },
                "required": ["bucket", "policy"]
            },
        ),
        Tool(
            name="bucket_policy_delete",
            description="Delete bucket policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_lifecycle_get",
            description="Get bucket lifecycle configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_lifecycle_set",
            description="Set bucket lifecycle configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "rules": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["bucket", "rules"]
            },
        ),
        Tool(
            name="bucket_replication_get",
            description="Get bucket replication configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_replication_set",
            description="Set bucket replication configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "role": {"type": "string"},
                    "rules": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["bucket", "role", "rules"]
            },
        ),
        Tool(
            name="bucket_notification_get",
            description="Get bucket notification configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="bucket_notification_set",
            description="Set bucket notification configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "topic": {"type": "string"},
                    "events": {"type": "array", "items": {"type": "string"}},
                    "filter_prefix": {"type": "string", "default": ""},
                    "filter_suffix": {"type": "string", "default": ""}
                },
                "required": ["bucket", "topic", "events"]
            },
        ),
        Tool(
            name="object_list",
            description="List objects in bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "prefix": {"type": "string", "default": ""},
                    "delimiter": {"type": "string", "default": "/"},
                    "max_keys": {"type": "integer", "default": 1000},
                    "continuation_token": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="object_get",
            description="Get object",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "version_id": {"type": "string"}
                },
                "required": ["bucket", "key"]
            },
        ),
        Tool(
            name="object_put",
            description="Put object",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "body": {"type": "string"},
                    "content_type": {"type": "string"},
                    "metadata": {"type": "object"}
                },
                "required": ["bucket", "key", "body"]
            },
        ),
        Tool(
            name="object_delete",
            description="Delete object",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "version_id": {"type": "string"}
                },
                "required": ["bucket", "key"]
            },
        ),
        Tool(
            name="object_copy",
            description="Copy object",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_bucket": {"type": "string"},
                    "source_key": {"type": "string"},
                    "dest_bucket": {"type": "string"},
                    "dest_key": {"type": "string"}
                },
                "required": ["source_bucket", "source_key", "dest_bucket", "dest_key"]
            },
        ),
        Tool(
            name="presigned_url",
            description="Generate presigned URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "method": {"type": "string", "enum": ["GET", "PUT", "POST", "DELETE", "HEAD"], "default": "GET"},
                    "expires_in": {"type": "integer", "default": 3600}
                },
                "required": ["bucket", "key"]
            },
        ),
        Tool(
            name="multipart_upload_init",
            description="Initiate multipart upload",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "content_type": {"type": "string", "default": "application/octet-stream"}
                },
                "required": ["bucket", "key"]
            },
        ),
        Tool(
            name="multipart_upload_part",
            description="Upload multipart part",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "upload_id": {"type": "string"},
                    "part_number": {"type": "integer"},
                    "body": {"type": "string"}
                },
                "required": ["bucket", "key", "upload_id", "part_number", "body"]
            },
        ),
        Tool(
            name="multipart_upload_complete",
            description="Complete multipart upload",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "upload_id": {"type": "string"},
                    "parts": {"type": "array", "items": {"type": "object", "properties": {"ETag": {"type": "string"}, "PartNumber": {"type": "integer"}}}}
                },
                "required": ["bucket", "key", "upload_id", "parts"]
            },
        ),
        Tool(
            name="multipart_upload_abort",
            description="Abort multipart upload",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "upload_id": {"type": "string"}
                },
                "required": ["bucket", "key", "upload_id"]
            },
        ),
        Tool(
            name="versioning_get",
            description="Get bucket versioning status",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="versioning_set",
            description="Set bucket versioning",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "status": {"type": "string", "enum": ["Enabled", "Suspended"]}
                },
                "required": ["bucket", "status"]
            },
        ),
        Tool(
            name="versions_list",
            description="List object versions",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "prefix": {"type": "string", "default": ""},
                    "max_versions": {"type": "integer", "default": 1000}
                },
                "required": ["bucket"]
            },
        ),
        Tool(
            name="acl_get",
            description="Get object ACL",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"}
                },
                "required": ["bucket", "key"]
            },
        ),
        Tool(
            name="acl_put",
            description="Set object ACL",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "key": {"type": "string"},
                    "acl": {"type": "string", "enum": ["private", "public-read", "public-read-write", "authenticated-read", "aws-exec-read", "bucket-owner-read", "bucket-owner-full-control"]}
                },
                "required": ["bucket", "key", "acl"]
            },
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
        if name == "bucket_list":
            return await handle_bucket_list(arguments)
        elif name == "bucket_create":
            return await handle_bucket_create(arguments)
        elif name == "bucket_delete":
            return await handle_bucket_delete(arguments)
        elif name == "bucket_policy_get":
            return await handle_bucket_policy_get(arguments)
        elif name == "bucket_policy_set":
            return await handle_bucket_policy_set(arguments)
        elif name == "bucket_policy_delete":
            return await handle_bucket_policy_delete(arguments)
        elif name == "bucket_lifecycle_get":
            return await handle_bucket_lifecycle_get(arguments)
        elif name == "bucket_lifecycle_set":
            return await handle_bucket_lifecycle_set(arguments)
        elif name == "bucket_replication_get":
            return await handle_bucket_replication_get(arguments)
        elif name == "bucket_replication_set":
            return await handle_bucket_replication_set(arguments)
        elif name == "bucket_notification_get":
            return await handle_bucket_notification_get(arguments)
        elif name == "bucket_notification_set":
            return await handle_bucket_notification_set(arguments)
        elif name == "object_list":
            return await handle_object_list(arguments)
        elif name == "object_get":
            return await handle_object_get(arguments)
        elif name == "object_put":
            return await handle_object_put(arguments)
        elif name == "object_delete":
            return await handle_object_delete(arguments)
        elif name == "object_copy":
            return await handle_object_copy(arguments)
        elif name == "presigned_url":
            return await handle_presigned_url(arguments)
        elif name == "multipart_upload_init":
            return await handle_multipart_upload_init(arguments)
        elif name == "multipart_upload_part":
            return await handle_multipart_upload_part(arguments)
        elif name == "multipart_upload_complete":
            return await handle_multipart_upload_complete(arguments)
        elif name == "multipart_upload_abort":
            return await handle_multipart_upload_abort(arguments)
        elif name == "versioning_get":
            return await handle_versioning_get(arguments)
        elif name == "versioning_set":
            return await handle_versioning_set(arguments)
        elif name == "versions_list":
            return await handle_versions_list(arguments)
        elif name == "acl_get":
            return await handle_acl_get(arguments)
        elif name == "acl_put":
            return await handle_acl_put(arguments)
        elif name == "health_check":
            return await handle_health_check(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER ====================

import os
import boto3
from botocore.config import Config

MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
MINIO_REGION = os.environ.get("MINIO_REGION", "us-east-1")

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name=MINIO_REGION,
        config=Config(signature_version="s3v4")
    )


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_bucket_list(args: Dict) -> List[TextContent]:
    client = get_s3_client()
    try:
        result = client.list_buckets()
        return [TextContent(type="text", text=json.dumps({
            "buckets": [{"name": b["Name"], "creation_date": str(b["CreationDate"])} for b in result["Buckets"]]
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_create(args: Dict) -> List[TextContent]:
    req = BucketCreateRequest(**arguments)
    client = get_s3_client()
    try:
        if req.region == "us-east-1":
            client.create_bucket(Bucket=req.bucket)
        else:
            client.create_bucket(Bucket=req.bucket, CreateBucketConfiguration={"LocationConstraint": req.region})
        if req.object_lock:
            client.put_object_lock_configuration(Bucket=req.bucket, ObjectLockConfiguration={"ObjectLockEnabled": "Enabled"})
        return [TextContent(type="text", text=json.dumps({"status": "CREATED", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_delete(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        if req.force:
            # Delete all objects first
            paginator = get_s3_client().get_paginator("list_object_versions")
            for page in paginator.paginate(Bucket=req.bucket):
                for version in page.get("Versions", []):
                    client.delete_object(Bucket=req.bucket, Key=version["Key"], VersionId=version["VersionId"])
                for marker in page.get("DeleteMarkers", []):
                    client.delete_object(Bucket=req.bucket, Key=marker["Key"], VersionId=marker["VersionId"])
        client.delete_bucket(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps({"status": "DELETED", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_policy_get(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_bucket_policy(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps(json.loads(result["Policy"]), indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_policy_set(args: Dict) -> List[TextContent]:
    req = BucketPolicyRequest(**arguments)
    client = get_s3_client()
    try:
        client.put_bucket_policy(Bucket=req.bucket, Policy=json.dumps(req.policy))
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_policy_delete(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        client.delete_bucket_policy(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps({"status": "DELETED", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_lifecycle_get(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_bucket_lifecycle_configuration(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_lifecycle_set(args: Dict) -> List[TextContent]:
    req = BucketLifecycleRequest(**arguments)
    client = get_s3_client()
    try:
        client.put_bucket_lifecycle_configuration(Bucket=req.bucket, LifecycleConfiguration={"Rules": req.rules})
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_replication_get(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_bucket_replication(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_replication_set(args: Dict) -> List[TextContent]:
    req = BucketReplicationRequest(**arguments)
    client = get_s3_client()
    try:
        client.put_bucket_replication(
            Bucket=req.bucket,
            ReplicationConfiguration={"Role": req.role, "Rules": req.rules}
        )
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_notification_get(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_bucket_notification_configuration(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bucket_notification_set(args: Dict) -> List[TextContent]:
    req = BucketNotificationRequest(**arguments)
    client = get_s3_client()
    try:
        config = {
            "TopicConfigurations": [{
                "TopicArn": req.topic,
                "Events": req.events,
                "Filter": {"Key": {"FilterRules": []}}
            }]
        }
        if req.filter_prefix or req.filter_suffix:
            rules = []
            if req.filter_prefix:
                rules.append({"Name": "prefix", "Value": req.filter_prefix})
            if req.filter_suffix:
                rules.append({"Name": "suffix", "Value": req.filter_suffix})
            config["TopicConfigurations"][0]["Filter"] = {"Key": {"FilterRules": rules}}
        
        client.put_bucket_notification_configuration(Bucket=req.bucket, NotificationConfiguration=config)
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_object_list(args: Dict) -> List[TextContent]:
    req = ObjectListRequest(**arguments)
    client = get_s3_client()
    try:
        params = {"Bucket": req.bucket, "MaxKeys": req.max_keys}
        if req.prefix:
            params["Prefix"] = req.prefix
        if req.delimiter:
            params["Delimiter"] = req.delimiter
        if req.continuation_token:
            params["ContinuationToken"] = req.continuation_token
        
        result = client.list_objects_v2(**params)
        return [TextContent(type="text", text=json.dumps({
            "objects": [{"key": o["Key"], "size": o["Size"], "last_modified": str(o["LastModified"]), "etag": o["ETag"]} for o in result.get("Contents", [])],
            "prefixes": result.get("CommonPrefixes", []),
            "is_truncated": result.get("IsTruncated", False),
            "next_continuation_token": result.get("NextContinuationToken")
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_object_get(args: Dict) -> List[TextContent]:
    req = ObjectGetRequest(**arguments)
    client = get_s3_client()
    try:
        params = {"Bucket": req.bucket, "Key": req.key}
        if req.version_id:
            params["VersionId"] = req.version_id
        result = client.get_object(**params)
        body = result["Body"].read().decode("utf-8")
        return [TextContent(type="text", text=json.dumps({
            "bucket": req.bucket,
            "key": req.key,
            "version_id": result.get("VersionId"),
            "content_type": result.get("ContentType"),
            "content_length": result.get("ContentLength"),
            "last_modified": str(result.get("LastModified")),
            "etag": result.get("ETag"),
            "metadata": result.get("Metadata", {}),
            "body": body
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_object_put(args: Dict) -> List[TextContent]:
    req = ObjectPutRequest(**arguments)
    client = get_s3_client()
    try:
        params = {"Bucket": req.bucket, "Key": req.key, "Body": req.body.encode() if isinstance(req.body, str) else req.body}
        if req.content_type:
            params["ContentType"] = req.content_type
        if req.metadata:
            params["Metadata"] = req.metadata
        result = client.put_object(**params)
        return [TextContent(type="text", text=json.dumps({
            "status": "UPLOADED",
            "bucket": req.bucket,
            "key": req.key,
            "etag": result.get("ETag"),
            "version_id": result.get("VersionId")
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_object_delete(args: Dict) -> List[TextContent]:
    req = ObjectDeleteRequest(**arguments)
    client = get_s3_client()
    try:
        params = {"Bucket": req.bucket, "Key": req.key}
        if req.version_id:
            params["VersionId"] = req.version_id
        client.delete_object(**params)
        return [TextContent(type="text", text=json.dumps({"status": "DELETED", "bucket": req.bucket, "key": req.key}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_object_copy(args: Dict) -> List[TextContent]:
    req = ObjectCopyRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.copy_object(
            CopySource={"Bucket": req.source_bucket, "Key": req.source_key},
            Bucket=req.dest_bucket,
            Key=req.dest_key
        )
        return [TextContent(type="text", text=json.dumps({
            "status": "COPIED",
            "source": f"{req.source_bucket}/{req.source_key}",
            "dest": f"{req.dest_bucket}/{req.dest_key}",
            "etag": result.get("CopyObjectResult", {}).get("ETag")
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_presigned_url(args: Dict) -> List[TextContent]:
    req = PresignedUrlRequest(**arguments)
    client = get_s3_client()
    try:
        url = client.generate_presigned_url(
            ClientMethod=req.method.lower() + "_object",
            Params={"Bucket": req.bucket, "Key": req.key},
            ExpiresIn=req.expires_in
        )
        return [TextContent(type="text", text=json.dumps({"url": url, "method": req.method, "expires_in": req.expires_in}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_multipart_upload_init(args: Dict) -> List[TextContent]:
    req = MultipartUploadInitRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.create_multipart_upload(Bucket=req.bucket, Key=req.key, ContentType=req.content_type)
        return [TextContent(type="text", text=json.dumps({
            "bucket": req.bucket,
            "key": req.key,
            "upload_id": result["UploadId"]
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_multipart_upload_part(args: Dict) -> List[TextContent]:
    req = MultipartUploadPartRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.upload_part(
            Bucket=req.bucket,
            Key=req.key,
            UploadId=req.upload_id,
            PartNumber=req.part_number,
            Body=req.body.encode() if isinstance(req.body, str) else req.body
        )
        return [TextContent(type="text", text=json.dumps({
            "etag": result["ETag"],
            "part_number": req.part_number
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_multipart_upload_complete(args: Dict) -> List[TextContent]:
    req = MultipartUploadCompleteRequest(**arguments)
    client = get_s3_client()
    try:
        parts = [{"ETag": p["ETag"], "PartNumber": p["PartNumber"]} for p in req.parts]
        result = client.complete_multipart_upload(
            Bucket=req.bucket,
            Key=req.key,
            UploadId=req.upload_id,
            MultipartUpload={"Parts": parts}
        )
        return [TextContent(type="text", text=json.dumps({
            "status": "COMPLETED",
            "bucket": req.bucket,
            "key": req.key,
            "etag": result.get("ETag"),
            "location": result.get("Location")
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_multipart_upload_abort(args: Dict) -> List[TextContent]:
    req = MultipartUploadAbortRequest(**arguments)
    client = get_s3_client()
    try:
        client.abort_multipart_upload(Bucket=req.bucket, Key=req.key, UploadId=req.upload_id)
        return [TextContent(type="text", text=json.dumps({"status": "ABORTED", "bucket": req.bucket, "key": req.key}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_versioning_get(args: Dict) -> List[TextContent]:
    req = BucketRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_bucket_versioning(Bucket=req.bucket)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_versioning_set(args: Dict) -> List[TextContent]:
    req = VersioningRequest(**arguments)
    client = get_s3_client()
    try:
        client.put_bucket_versioning(Bucket=req.bucket, VersioningConfiguration={"Status": req.status})
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket, "versioning": req.status}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_versions_list(args: Dict) -> List[TextContent]:
    req = VersionsListRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.list_object_versions(Bucket=req.bucket, Prefix=req.prefix, MaxKeys=req.max_versions)
        versions = []
        for v in result.get("Versions", []):
            versions.append({"key": v["Key"], "version_id": v["VersionId"], "is_latest": v["IsLatest"], "size": v["Size"], "last_modified": str(v["LastModified"])})
        for dm in result.get("DeleteMarkers", []):
            versions.append({"key": dm["Key"], "version_id": dm["VersionId"], "is_delete_marker": True})
        return [TextContent(type="text", text=json.dumps({"versions": versions}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_acl_get(args: Dict) -> List[TextContent]:
    req = ACLRequest(**arguments)
    client = get_s3_client()
    try:
        result = client.get_object_acl(Bucket=req.bucket, Key=req.key)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_acl_put(args: Dict) -> List[TextContent]:
    req = ACLRequest(**arguments)
    client = get_s3_client()
    try:
        client.put_object_acl(Bucket=req.bucket, Key=req.key, ACL=req.acl)
        return [TextContent(type="text", text=json.dumps({"status": "SET", "bucket": req.bucket, "key": req.key, "acl": req.acl}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health_check(args: Dict) -> List[TextContent]:
    try:
        client = get_s3_client()
        client.list_buckets()
        return [TextContent(type="text", text=json.dumps({"healthy": True, "status": "OK"}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"healthy": False, "error": str(e)}, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
