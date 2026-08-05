# Tempo Configuration Troubleshooting

## Problem
Tempo Docker container fails to start with: `error initialising module: store: failed to create store: unknown backend ""`

## Root Cause
Tempo requires a storage backend — it does NOT have a built-in "memory" or "filesystem" backend in the standard distribution. The config schema varies significantly between versions.

## Version-Specific Notes
- **tempo:v3.0.0+**: Different schema entirely, uses `compactor` and `store` sections
- **tempo:2.5.0**: Works with `storage.trace.backend: s3`
- **tempo:2.4.x**: Same issue as 2.5.0

## Working Config (tempo:2.5.0)

```yaml
auth_enabled: false
server:
  http_listen_port: 3200
distributor:
  receivers:
    otlp:
      protocols:
        grpc:
        http:
storage:
  trace:
    backend: s3
    s3:
      endpoint: host.docker.internal:9000
      bucket: tempo
      access_key: minioadmin
      secret_key: minioadmin
      insecure: true
```

## Key Insights

1. **Must use `host.docker.internal`, NOT `localhost` or `127.0.0.1`** — inside the container, localhost refers to the container itself, not the host where MinIO is running.

2. **Bucket must be pre-created in MinIO**:
   ```bash
   docker exec minio-mcp mc alias set local http://127.0.0.1:9000 minioadmin minioadmin
   docker exec minio-mcp mc mb local/tempo
   ```

3. **Tempo config file must be mounted** into the container:
   ```bash
   docker run -d --name tempo -p 3200:3200 \
     -v "C:/Users/apviz/AppData/Local/hermes/scripts/tempo-config.yaml:/etc/tempo.yaml" \
     grafana/tempo:2.5.0 -config.file=/etc/tempo.yaml
   ```

4. **Do NOT use filesystem backend** — the `traces_directory` and `metrics_directory` fields are NOT valid in tempo 2.5.0's `storage.trace.filesystem` section. The filesystem backend is not supported.

## Working tempo-config.yaml

Located at: `C:\Users\apviz\AppData\Local\hermes\scripts\tempo-config.yaml`
```yaml
auth_enabled: false
server:
  http_listen_port: 3200
distributor:
  receivers:
    otlp:
      protocols:
        grpc:
        http:
storage:
  trace:
    backend: s3
    s3:
      endpoint: host.docker.internal:9000
      bucket: tempo
      access_key: minioadmin
      secret_key: minioadmin
      insecure: true
```
