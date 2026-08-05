import os, re, datetime, json, time, sys

BASE = r'C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA\00_KV_SECOND BRAIN'
JOURNAL = r'C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md'
CHECKPOINT = r'C:\Users\apviz\AppData\Local\hermes\process_checkpoint.json'
LOG = r'C:\Users\apviz\AppData\Local\hermes\process_log.txt'

def log(msg):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{timestamp} {msg}\n')
    print(msg, flush=True)

# Load checkpoint
if os.path.exists(CHECKPOINT):
    with open(CHECKPOINT, 'r') as f:
        data = json.load(f)
        start_index = data.get('processed_files', 0)
else:
    start_index = 0

log(f'Resuming from index {start_index}')

# Determine next AMINTIRE number
max_num = 0
if os.path.exists(JOURNAL):
    with open(JOURNAL, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = re.search(r'AMINTIRE-(\d+)', line)
            if m:
                n = int(m.group(1))
                if n > max_num:
                    max_num = n
next_num = max_num + 1
log(f'Next AMINTIRE number: {next_num}')

TODAY = datetime.date.today().isoformat()

ROLE_MAP = {
    '- ORCHESTRATOR - Sys Folder - Hermes Default': 'ORCHESTRATOR',
    '- Skills and MCP Skill Bundles': 'SKILLS',
    'CLI_PRIME_OPPERATIONS - CPO': 'CLI',
    'CODER_OPPERATIOS - CO': 'CODER',
    'COWORK_OPPERATIOS - COW': 'COWORK',
    'POPY_OPPERATIONS - PO': 'POPY',
    'SENTINEL_PRIME_OPPERATIONS - SPO': 'SENTINEL_PRIME'
}

def get_role(folder_name):
    for key, val in ROLE_MAP.items():
        if key in folder_name:
            return val
    return 'UNKNOWN'

# Collect all files
all_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        all_files.append(os.path.join(root, f))
all_files.sort()
total_files = len(all_files)
log(f'Total files: {total_files}')
log(f'Files remaining: {total_files - start_index}')

processed_total = 0
lines_added_total = 0
start_time = time.time()
try:
    for idx in range(start_index, total_files):
        filepath = all_files[idx]
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
        except Exception as e:
            log(f'Skipping {filepath}: {e}')
            continue
        rel_path = os.path.relpath(filepath, BASE)
        first_part = rel_path.split(os.sep)[0] if os.sep in rel_path else rel_path
        role = get_role(first_part)
        for i, line in enumerate(lines, start=1):
            line_stripped = line.rstrip('\n\r')
            if not line_stripped.strip():
                continue
            desc = line_stripped[:100].replace('`', '\\`')
            entry = f'''AMINTIRE-{next_num:03d} — {TODAY} — Line {i} from {rel_path} ({role}): {desc}
TAG-URI: #[LN{i}] #[VAULT:{first_part}] #[ROLE:{role}]
SOURCES:
- `{filepath}`
---
'''
            with open(JOURNAL, 'a', encoding='utf-8') as jf:
                jf.write(entry)
            next_num += 1
            lines_added_total += 1
        processed_total += 1
        if processed_total % 500 == 0:
            elapsed = time.time() - start_time
            log(f'Processed {processed_total} files, added {lines_added_total} lines, next num: {next_num}, elapsed: {elapsed:.1f}s')
            with open(CHECKPOINT, 'w') as f:
                json.dump({'processed_files': start_index + processed_total}, f)
    else:
        # Completed all files
        if os.path.exists(CHECKPOINT):
            os.remove(CHECKPOINT)
        log('All files processed, checkpoint removed.')
finally:
    elapsed_total = time.time() - start_time
    log(f'Finished processing. Total files processed in this run: {processed_total}, lines added: {lines_added_total}, final next num: {next_num}, total elapsed: {elapsed_total:.1f}s')