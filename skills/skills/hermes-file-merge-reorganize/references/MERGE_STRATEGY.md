# MERGE_STRATEGY.md
# Decision tree and rules for the file merge & reorganize skill

# File Merge Strategy Reference

## Decision Tree

```
For each affected directory:
│
├── Both files exist?
│   ├── YES
│   │   ├── Are they identical? (byte-level)
│   │   │   ├── YES → Delete smaller, rename larger to canonical
│   │   │   └── NO  → Merge (larger = baseline, append unique from smaller)
│   │   │             Then rename merged result to canonical
│   │   └── Is one empty?
│   │       ├── YES → Delete empty, rename the other to canonical
│   │       └── NO  → Full merge procedure
│   └── NO (only one file)
│       └── Rename only → rename to canonical name
│
└── Canonical file already exists?
    ├── YES → Compare with source, merge if different, then delete source
    └── NO  → Rename / create from merge
```

## Merge Rules

1. **Larger file = baseline**: the file with more bytes is always kept as the base
2. **Append unique lines**: from the smaller file, only append lines whose stripped
   content does not already appear anywhere in the baseline
3. **Section headers**: if both files have the same `## Header`, keep only one
4. **Add merge marker**: append a comment line before unique merged content:
   `<!-- Merged from: ORIGINAL_FILENAME.md -->`
5. **Encoding**: always read/write as `utf-8`

## Canonical Name Convention

The canonical (SOT) name for the CONSTINTA concept is: `CONSTINTA.md`

| Legacy Name | Canonical |
|-------------|-----------|
| `CONSTIINTA.md` | `CONSTINTA.md` |
| `CONȘTINȚA.md` | `CONSTINTA.md` |
| `CONŞTINŢA.md` | `CONSTINTA.md` |
| `constiinta.md` | `constinta.md` |

## Scope — Directories to Always Check

```
C:\Users\apviz\AppData\Local\hermes\profiles\assist\
C:\Users\apviz\AppData\Local\hermes\profiles\prime\
C:\Users\apviz\AppData\Local\hermes\profiles\default\
C:\Users\apviz\AppData\Local\hermes\state-snapshots\*\profiles\assist\
C:\Users\apviz\AppData\Local\hermes\state-snapshots\*\profiles\prime\
C:\Users\apviz\AppData\Local\hermes\state-snapshots\*\profiles\default\
C:\Users\apviz\AppData\Local\hermes\backups\*\profiles\*\
C:\Users\apviz\AppData\Local\hermes\skills\*\
```

## Safety Checklist

- [ ] Ran scan (dry-run) and confirmed conflict list
- [ ] Created `.bak` copies of files > 5KB before modifying
- [ ] Verified merged file contains all unique content from both sources
- [ ] Ran post-merge filename verification (0 legacy names)
- [ ] Ran `hermes config` boot test to confirm no regression
