"""
Vault MCP Server
HashiCorp Vault integration for secret management, dynamic secrets, encryption.
"""

import asyncio
import json
import os
import hvac
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("vault-mcp")


# ==================== MODELS ====================

class AuthRequest(BaseModel):
    method: str = Field(description="Auth method: token, approle, userpass, ldap, github, aws, kubernetes")
    token: Optional[str] = Field(default=None, description="Token for token auth")
    role_id: Optional[str] = Field(default=None, description="Role ID for approle")
    secret_id: Optional[str] = Field(default=None, description="Secret ID for approle")
    username: Optional[str] = Field(default=None, description="Username for userpass")
    password: Optional[str] = Field(default=None, description="Password for userpass")
    path: str = Field(default="", description="Auth mount path")


class SecretReadRequest(BaseModel):
    path: str = Field(description="Secret path")
    mount_point: str = Field(default="secret", description="KV mount point")
    version: Optional[int] = Field(default=None, description="Specific version")


class SecretWriteRequest(BaseModel):
    path: str = Field(description="Secret path")
    data: Dict[str, Any] = Field(description="Secret data")
    mount_point: str = Field(default="secret", description="KV mount point")
    cas: int = Field(default=0, description="Check-and-set version")


class SecretDeleteRequest(BaseModel):
    path: str = Field(description="Secret path")
    mount_point: str = Field(default="secret", description="KV mount point")
    versions: Optional[List[int]] = Field(default=None, description="Specific versions to delete")


class SecretListRequest(BaseModel):
    path: str = Field(default="", description="Path to list")
    mount_point: str = Field(default="secret", description="KV mount point")


class GenerateCredentialsRequest(BaseModel):
    role: str = Field(description="Role name")
    mount_point: str = Field(default="database", description="Database mount point")


class EncryptRequest(BaseModel):
    key_name: str = Field(description="Transit key name")
    plaintext: str = Field(description="Plaintext to encrypt (base64 encoded)")
    context: Optional[str] = Field(default=None, description="Additional context (base64)")


class DecryptRequest(BaseModel):
    key_name: str = Field(description="Transit key name")
    ciphertext: str = Field(description="Ciphertext to decrypt (base64 encoded)")
    context: Optional[str] = Field(default=None, description="Additional context (base64)")


class SignRequest(BaseModel):
    key_name: str = Field(description="Transit key name")
    input: str = Field(description="Input to sign (base64 encoded)")
    algorithm: Optional[str] = Field(default=None, description="Algorithm: ecdsa-p256, rsa-2048, etc.")


class VerifyRequest(BaseModel):
    key_name: str = Field(description="Transit key name")
    input: str = Field(description="Input to verify (base64 encoded)")
    signature: str = Field(description="Signature to verify (base64 encoded)")
    algorithm: Optional[str] = Field(default=None, description="Algorithm")


class PolicyRequest(BaseModel):
    name: str = Field(description="Policy name")
    rules: str = Field(description="Policy HCL rules")
    action: str = Field(description="Action: read, write, delete, list")


class TokenRequest(BaseModel):
    policies: List[str] = Field(default_factory=list, description="Policies to attach")
    ttl: Optional[str] = Field(default=None, description="Token TTL (e.g., 1h, 24h)")
    renewable: bool = Field(default=False, description="Whether token is renewable")
    num_uses: Optional[int] = Field(default=None, description="Number of uses")
    meta: Dict[str, str] = Field(default_factory=dict, description="Metadata")


class SealStatusRequest(BaseModel):
    pass


# ==================== SERVER ====================

app = Server("vault-mcp")

# Vault client - will be initialized on first use
vault_client: Optional[hvac.Client] = None
VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://localhost:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "")


def get_client() -> hvac.Client:
    """Get or create Vault client."""
    global vault_client
    if vault_client is None:
        vault_client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    return vault_client


# ==================== TOOLS ====================

app = Server("vault-mcp")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="auth",
            description="Authenticate to Vault",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {"type": "string", "enum": ["token", "approle", "userpass", "ldap", "github", "aws", "kubernetes"]},
                    "token": {"type": "string"},
                    "role_id": {"type": "string"},
                    "secret_id": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "path": {"type": "string", "default": ""}
                },
                "required": ["method"]
            },
        ),
        Tool(
            name="secret_read",
            description="Read a secret from KV store",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "mount_point": {"type": "string", "default": "secret"},
                    "version": {"type": "integer"}
                },
                "required": ["path"]
            },
        ),
        Tool(
            name="secret_write",
            description="Write a secret to KV store",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "data": {"type": "object"},
                    "mount_point": {"type": "string", "default": "secret"},
                    "cas": {"type": "integer", "default": 0}
                },
                "required": ["path", "data"]
            },
        ),
        Tool(
            name="secret_delete",
            description="Delete a secret or specific versions",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "mount_point": {"type": "string", "default": "secret"},
                    "versions": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["path"]
            },
        ),
        Tool(
            name="secret_list",
            description="List secrets at path",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": ""},
                    "mount_point": {"type": "string", "default": "secret"}
                },
                "required": []
            },
        ),
        Tool(
            name="generate_credentials",
            description="Generate dynamic credentials from database role",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "mount_point": {"type": "string", "default": "database"}
                },
                "required": ["role"]
            },
        ),
        Tool(
            name="encrypt",
            description="Encrypt data using Transit engine",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_name": {"type": "string"},
                    "plaintext": {"type": "string"},
                    "context": {"type": "string"}
                },
                "required": ["key_name", "plaintext"]
            },
        ),
        Tool(
            name="decrypt",
            description="Decrypt data using Transit engine",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_name": {"type": "string"},
                    "ciphertext": {"type": "string"},
                    "context": {"type": "string"}
                },
                "required": ["key_name", "ciphertext"]
            },
        ),
        Tool(
            name="sign",
            description="Sign data using Transit engine",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_name": {"type": "string"},
                    "input": {"type": "string"},
                    "algorithm": {"type": "string"}
                },
                "required": ["key_name", "input"]
            },
        ),
        Tool(
            name="verify",
            description="Verify signature using Transit engine",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_name": {"type": "string"},
                    "input": {"type": "string"},
                    "signature": {"type": "string"},
                    "algorithm": {"type": "string"}
                },
                "required": ["key_name", "input", "signature"]
            },
        ),
        Tool(
            name="policy_read",
            description="Read a policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="policy_write",
            description="Write a policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "rules": {"type": "string"}
                },
                "required": ["name", "rules"]
            },
        ),
        Tool(
            name="policy_delete",
            description="Delete a policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="policy_list",
            description="List all policies",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="token_create",
            description="Create a new token",
            inputSchema={
                "type": "object",
                "properties": {
                    "policies": {"type": "array", "items": {"type": "string"}},
                    "ttl": {"type": "string"},
                    "renewable": {"type": "boolean", "default": False},
                    "num_uses": {"type": "integer"},
                    "meta": {"type": "object"}
                },
                "required": []
            },
        ),
        Tool(
            name="token_lookup",
            description="Lookup token info",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string"}
                },
                "required": ["token"]
            },
        ),
        Tool(
            name="token_revoke",
            description="Revoke a token",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string"}
                },
                "required": ["token"]
            },
        ),
        Tool(
            name="token_renew",
            description="Renew a token",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string"}
                },
                "required": ["token"]
            },
        ),
        Tool(
            name="seal_status",
            description="Get seal status",
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
        client = get_client()
        
        if name == "auth":
            return await handle_auth(arguments)
        elif name == "secret_read":
            return await handle_secret_read(arguments)
        elif name == "secret_write":
            return await handle_secret_write(arguments)
        elif name == "secret_delete":
            return await handle_secret_delete(arguments)
        elif name == "secret_list":
            return await handle_secret_list(arguments)
        elif name == "generate_credentials":
            return await handle_generate_credentials(arguments)
        elif name == "encrypt":
            return await handle_encrypt(arguments)
        elif name == "decrypt":
            return await handle_decrypt(arguments)
        elif name == "sign":
            return await handle_sign(arguments)
        elif name == "verify":
            return await handle_verify(arguments)
        elif name == "policy_read":
            return await handle_policy_read(arguments)
        elif name == "policy_write":
            return await handle_policy_write(arguments)
        elif name == "policy_delete":
            return await handle_policy_delete(arguments)
        elif name == "policy_list":
            return await handle_policy_list(arguments)
        elif name == "token_create":
            return await handle_token_create(arguments)
        elif name == "token_lookup":
            return await handle_token_lookup(arguments)
        elif name == "token_revoke":
            return await handle_token_revoke(arguments)
        elif name == "token_renew":
            return await handle_token_renew(arguments)
        elif name == "seal_status":
            return await handle_seal_status(arguments)
        elif name == "health_check":
            return await handle_health_check(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_auth(args: Dict) -> List[TextContent]:
    req = AuthRequest(**arguments)
    client = get_client()
    
    if req.method == "token":
        if not req.token:
            return [TextContent(type="text", text="Token required for token auth")]
        client.token = req.token
        return [TextContent(type="text", text="Token authentication set")]
    
    elif req.method == "approle":
        if not req.role_id or not req.secret_id:
            return [TextContent(type="text", text="role_id and secret_id required for approle")]
        result = client.auth.approle.login(role_id=req.role_id, secret_id=req.secret_id, mount_point=req.path or "approle")
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"AppRole login successful. Token: {client.token}")]
    
    elif req.method == "userpass":
        if not req.username or not req.password:
            return [TextContent(type="text", text="username and password required")]
        result = client.auth.userpass.login(username=req.username, password=req.password, mount_point=req.path or "userpass")
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"Userpass login successful. Token: {client.token}")]
    
    elif req.method == "ldap":
        if not req.username or not req.password:
            return [TextContent(type="text", text="username and password required")]
        result = client.auth.ldap.login(username=req.username, password=req.password, mount_point=req.path or "ldap")
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"LDAP login successful. Token: {client.token}")]
    
    elif req.method == "github":
        if not req.token:
            return [TextContent(type="text", text="GitHub token required")]
        result = client.auth.github.login(token=req.token, mount_point=req.path or "github")
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"GitHub login successful. Token: {client.token}")]
    
    elif req.method == "aws":
        if not req.access_key or not req.secret_key:
            return [TextContent(type="text", text="AWS credentials required")]
        result = client.auth.aws.iam_login(
            access_key=req.access_key,
            secret_key=req.secret_key,
            mount_point=req.path or "aws"
        )
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"AWS login successful. Token: {client.token}")]
    
    elif req.method == "kubernetes":
        # Kubernetes auth requires JWT token
        if not req.token:
            return [TextContent(type="text", text="Kubernetes JWT token required")]
        result = client.auth.kubernetes.login(role=req.role_id or "default", jwt=req.token, mount_point=req.path or "kubernetes")
        client.token = result["auth"]["client_token"]
        return [TextContent(type="text", text=f"Kubernetes login successful. Token: {client.token}")]
    
    return [TextContent(type="text", text=f"Unknown auth method: {req.method}")]


async def handle_secret_read(args: Dict) -> List[TextContent]:
    req = SecretReadRequest(**arguments)
    client = get_client()
    
    try:
        result = client.secrets.kv.v2.read_secret_version(
            path=req.path,
            mount_point=req.mount_point,
            version=req.version
        )
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading secret: {str(e)}")]


async def handle_secret_write(args: Dict) -> List[TextContent]:
    req = SecretWriteRequest(**arguments)
    client = get_client()
    
    try:
        result = client.secrets.kv.v2.create_or_update_secret(
            path=req.path,
            secret=req.data,
            mount_point=req.mount_point,
            cas=req.cas
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error writing secret: {str(e)}")]


async def handle_secret_delete(args: Dict) -> List[TextContent]:
    req = SecretDeleteRequest(**arguments)
    client = get_client()
    
    try:
        if req.versions:
            result = client.secrets.kv.v2.delete_secret_versions(
                path=req.path,
                mount_point=req.mount_point,
                versions=req.versions
            )
        else:
            result = client.secrets.kv.v2.delete_latest_version_of_secret(
                path=req.path,
                mount_point=req.mount_point
            )
        return [TextContent(type="text", text=json.dumps({"status": "deleted"}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error deleting secret: {str(e)}")]


async def handle_secret_list(args: Dict) -> List[TextContent]:
    req = SecretListRequest(**arguments)
    client = get_client()
    
    try:
        result = client.secrets.kv.v2.list_secrets(
            path=req.path,
            mount_point=req.mount_point
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error listing secrets: {str(e)}")]


async def handle_generate_credentials(args: Dict) -> List[TextContent]:
    req = GenerateCredentialsRequest(**arguments)
    client = get_client()
    
    try:
        result = client.secrets.database.generate_credentials(
            role=req.role,
            mount_point=req.mount_point
        )
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error generating credentials: {str(e)}")]


async def handle_encrypt(args: Dict) -> List[TextContent]:
    req = EncryptRequest(**arguments)
    client = get_client()
    
    try:
        import base64
        plaintext_b64 = base64.b64encode(req.plaintext.encode()).decode()
        params = {"plaintext": plaintext_b64}
        if req.context:
            params["context"] = req.context
        
        result = client.secrets.transit.encrypt_data(name=req.key_name, plaintext=req.plaintext, context=req.context)
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error encrypting: {str(e)}")]


async def handle_decrypt(args: Dict) -> List[TextContent]:
    req = DecryptRequest(**arguments)
    client = get_client()
    
    try:
        result = client.secrets.transit.decrypt_data(name=req.key_name, ciphertext=req.ciphertext, context=req.context)
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error decrypting: {str(e)}")]


async def handle_sign(args: Dict) -> List[TextContent]:
    req = SignRequest(**arguments)
    client = get_client()
    
    try:
        import base64
        input_b64 = base64.b64encode(req.input.encode()).decode()
        params = {"input": input_b64}
        if req.algorithm:
            params["algorithm"] = req.algorithm
        
        result = client.secrets.transit.sign_data(name=req.key_name, input=input_b64, algorithm=req.algorithm)
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error signing: {str(e)}")]


async def handle_verify(args: Dict) -> List[TextContent]:
    req = VerifyRequest(**arguments)
    client = get_client()
    
    try:
        import base64
        input_b64 = base64.b64encode(req.input.encode()).decode()
        result = client.secrets.transit.verify_signature(
            name=req.key_name,
            input=input_b64,
            signature=req.signature,
            algorithm=req.algorithm
        )
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error verifying: {str(e)}")]


async def handle_policy_read(args: Dict) -> List[TextContent]:
    req = PolicyRequest(**arguments)
    client = get_client()
    
    try:
        result = client.sys.read_policy(name=req.name)
        return [TextContent(type="text", text=result["data"]["rules"])]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading policy: {str(e)}")]


async def handle_policy_write(args: Dict) -> List[TextContent]:
    req = PolicyRequest(**arguments)
    client = get_client()
    
    try:
        client.sys.create_or_update_policy(name=req.name, policy=req.rules)
        return [TextContent(type="text", text=f"Policy '{req.name}' written successfully")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error writing policy: {str(e)}")]


async def handle_policy_delete(args: Dict) -> List[TextContent]:
    req = PolicyRequest(**arguments)
    client = get_client()
    
    try:
        client.sys.delete_policy(name=req.name)
        return [TextContent(type="text", text=f"Policy '{req.name}' deleted")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error deleting policy: {str(e)}")]


async def handle_policy_list(args: Dict) -> List[TextContent]:
    client = get_client()
    
    try:
        result = client.sys.list_policies()
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error listing policies: {str(e)}")]


async def handle_token_create(args: Dict) -> List[TextContent]:
    req = TokenRequest(**arguments)
    client = get_client()
    
    try:
        result = client.auth.token.create(
            policies=req.policies,
            ttl=req.ttl,
            renewable=req.renewable,
            num_uses=req.num_uses,
            meta=req.meta
        )
        return [TextContent(type="text", text=json.dumps(result["auth"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error creating token: {str(e)}")]


async def handle_token_lookup(args: Dict) -> List[TextContent]:
    req = TokenRequest(**arguments)
    client = get_client()
    
    try:
        result = client.auth.token.lookup(token=req.token)
        return [TextContent(type="text", text=json.dumps(result["data"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error looking up token: {str(e)}")]


async def handle_token_revoke(args: Dict) -> List[TextContent]:
    req = TokenRequest(**arguments)
    client = get_client()
    
    try:
        client.auth.token.revoke(token=req.token)
        return [TextContent(type="text", text="Token revoked")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error revoking token: {str(e)}")]


async def handle_token_renew(args: Dict) -> List[TextContent]:
    req = TokenRequest(**arguments)
    client = get_client()
    
    try:
        result = client.auth.token.renew(token=req.token)
        return [TextContent(type="text", text=json.dumps(result["auth"], indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error renewing token: {str(e)}")]


async def handle_seal_status(args: Dict) -> List[TextContent]:
    client = get_client()
    
    try:
        result = client.sys.read_seal_status()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error getting seal status: {str(e)}")]


async def handle_health_check(args: Dict) -> List[TextContent]:
    client = get_client()
    
    try:
        result = client.sys.read_health_status()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error checking health: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
