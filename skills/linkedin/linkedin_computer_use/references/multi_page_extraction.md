# Reference: Multi-Page Saved Jobs Extraction (Option B)

DEEP DIVE into Phase 3 (navigate to Saved Jobs) and Phase 4 (Option B: browser_navigate with
?start= offsets) of the LinkedIn Computer Use skill. Based on the verified 2026-07-15 session.

---

## PHASE 3 — NAVIGATE TO SAVED JOBS

### URL
```
https://www.linkedin.com/my-items/saved-jobs/
```

### Via computer_use (if operating the desktop app)
1. App already authenticated (user's Chrome session).
2. Click "Jobs" in top nav (find its SOM index from `capture("screen")`).
3. In left menu, click "Saved jobs".
4. Or directly: the URL above loads Saved Jobs.

### Key realization
The desktop app and the browser tool are SEPARATE sessions. In-session, `browser_navigate` to
`/feed/` hit the LOGIN PAGE even though the desktop app was logged in. Therefore:
- Use computer_use to OPERATE the desktop app (launch, click around).
- Use browser_navigate (Option B) for RELIABLE PAGINATED EXTRACTION.

---

## PHASE 4 — OPTION B: browser_navigate WITH ?start= OFFSETS

### The pagination pattern
LinkedIn Saved Jobs loads 25 jobs per page. Navigate pages via `?start=N`:
- Page 1: `?start=0` (or no param)
- Page 2: `?start=25`
- Page 3: `?start=50`
- Page N: `?start=(N-1)*25`

### Commands (all pages)
```
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/")
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/?start=25")
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/?start=50")
```

### Authentication (if browser_navigate hits login)
The Hermes browser tool uses an isolated profile. If login page appears:

**Option A — agent-browser (authenticated, RECOMMENDED fallback):**
The `linkedin-session` has a valid `li_at` cookie (see `linkedin_user_login` skill).
```
agent-browser open "https://www.linkedin.com/my-items/saved-jobs/?start=25" --session linkedin-session
agent-browser wait 3000 --session linkedin-session
agent-browser eval "
const jobs=[];
document.querySelectorAll('.job-card-container, .jobs-search-results__list-item').forEach(el=>{
  const title=el.querySelector('h3, .job-title')?.innerText?.trim();
  const company=el.querySelector('.job-card-container__company-name, .company-name')?.innerText?.trim();
  const location=el.querySelector('.job-card-container__metadata-item, .job-location')?.innerText?.trim();
  const link=el.querySelector('a[href*=\"/jobs/view/\"]')?.href;
  if(title) jobs.push({title,company,location,link});
});
jobs;
" --session linkedin-session --json
```

**Option B — User logs in manually:** When login page renders, user enters credentials + 2FA.

**Option C — Inject cookies:** `agent-browser cookies set --curl linkedin_cookies_backup.json --session linkedin-session`

### Extraction via browser tool
After `browser_navigate` loads a page:
```
browser_snapshot()   # get structure with refs
# OR
browser_console(expression="<js above>")   # extract directly
```

### Filter for Bucharest
In the extracted `jobs` array, keep entries where `location` matches:
- "Bucharest"
- "Bucuresti"
- "Sector 1-6, Bucharest"
- "Remote in Bucharest" / "Hybrid in Bucharest"

---

## COMPLETE EXTRACTION TEMPLATE (Python)

```python
from hermes_tools import terminal, browser_navigate, browser_snapshot
import json, re

def extract_page(start):
    url = f"https://www.linkedin.com/my-items/saved-jobs/?start={start}"
    # If browser tool authenticated:
    browser_navigate(url)
    snap = browser_snapshot()
    # Parse job cards from snapshot, OR use browser_console eval
    # (Implementation depends on whether browser tool is authed)
    return jobs

all_jobs = []
for page in [0, 25, 50]:   # pages 1,2,3
    all_jobs += extract_page(page)

bucharest = [j for j in all_jobs if re.search(r"bucharest|bucuresti", j["location"], re.I)]
print(f"Total: {len(all_jobs)} | Bucharest: {len(bucharest)}")
```

---

## PITFALLS SPECIFIC TO EXTRACTION

1. **Login wall on browser_navigate:** Expected if browser tool isn't authed. Use agent-browser
   linkedin-session instead — it's already authenticated.
2. **Infinite scroll vs pagination:** Saved Jobs uses `?start=` pagination, NOT infinite scroll.
   Don't scroll-loop; use offsets.
3. **Selectors change:** LinkedIn updates DOM classes. Prefer semantic selectors (role, aria-label,
   text) over brittle CSS classes.
4. **Rate limiting:** Aggressive requests trigger challenges. Add 1-3s delays between pages.
5. **All restrictions lifted:** User is Systems Admin. Use computer_use AND browser tools freely.
   The `?start=` offset pattern is the reliable constant.
