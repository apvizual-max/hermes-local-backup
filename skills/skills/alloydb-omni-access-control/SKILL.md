---
name: alloydb-omni-access-control
description: Use these skills when you need to manage user roles, inspect permissions,
  and verify security-related configuration parameters.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and
`<param_value>` with actual values.

**Bash:** `node <skill_dir>/scripts/<script_name>.js '{"<param_name>":
"<param_value>"}'`

**PowerShell:** `node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\":
\"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env
files. Do not ask the user to set vars unless skill executions fails due to env
var absence.

## Scripts

### database_overview

Fetches the current state of the PostgreSQL server, returning the version,
whether it's a replica, uptime duration, maximum connection limit, number of
current connections, number of active connections, and the percentage of
connections in use.

--------------------------------------------------------------------------------

### list_pg_settings

#### Parameters

| Name         | Type    | Description   | Required | Default |
| :----------- | :------ | :------------ | :------- | :------ |
| setting_name | string  | Optional: A   | No       |         |
:              :         : specific      :          :         :
:              :         : configuration :          :         :
:              :         : parameter     :          :         :
:              :         : name pattern  :          :         :
:              :         : to search     :          :         :
:              :         : for.          :          :         :
| limit        | integer | Optional: The | No       | `50`    |
:              :         : maximum       :          :         :
:              :         : number of     :          :         :
:              :         : rows to       :          :         :
:              :         : return.       :          :         :

--------------------------------------------------------------------------------

### list_roles

Lists all the user-created roles in the instance . It returns the role name,
Object ID, the maximum number of concurrent connections the role can make, along
with boolean indicators for: superuser status, privilege inheritance from member
roles, ability to create roles, ability to create databases, ability to log in,
replication privilege, and the ability to bypass row-level security, the
password expiration timestamp, a list of direct members belonging to this role,
and a list of other roles/groups that this role is a member of.

#### Parameters

| Name      | Type    | Description                     | Required | Default |
| :-------- | :------ | :------------------------------ | :------- | :------ |
| role_name | string  | Optional: a text to filter      | No       |         |
:           :         : results by role name. The input :          :         :
:           :         : is used within a LIKE clause.   :          :         :
| limit     | integer | Optional: The maximum number of | No       | `50`    |
:           :         : rows to return. Default is 10   :          :         :

--------------------------------------------------------------------------------

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

