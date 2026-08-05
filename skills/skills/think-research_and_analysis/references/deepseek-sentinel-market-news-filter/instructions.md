# Sub-Skill: deepseek-sentinel-market-news-filter

* **Description:** 🟢 NICE‑TO‑HAVE SKILLS: Filters financial news headlines through the 963‑proverb matrix, flagging only those that align with sacred logic (ignoring hype and fear).

---

6. Title: deepseek-sentinel-market-news-filter

Description: 🟢 NICE‑TO‑HAVE SKILLS:  Filters financial news headlines through the 963‑proverb matrix, flagging only those that align with sacred logic (ignoring hype and fear).

INSTRUCTION:

TRIGGER: Popy provides a news headline or asks "filtreaza stirea".
1. DECOMPOSE headline into key claims: asset, direction, reason, sentiment.
2. TEST each claim against relevant proverbs (e.g., "Zorii te mint" for early predictions, "Lacomia pierde omenia" for greed signals).
3. IF any proverb violated → OUTPUT: "Reject – hype/fear. Proverb violated: [proverb]."
4. IF all proverbs satisfied → OUTPUT: "Accept – signal aligns with sacred logic."
5. SHORT comment: "Can be considered, but verify with your own analysis."