# Sub-Skill: deepseek-sentinel-proverb-etymologist

* **Description:** 🟢 NICE‑TO‑HAVE SKILLS: When Popy asks about the origin of a proverb, searches the paremiological database (Zanne, Pann, Golescu) and provides historical and logical background.

---

5. Title: deepseek-sentinel-proverb-etymologist

Description: 🟢 NICE‑TO‑HAVE SKILLS:  When Popy asks about the origin of a proverb, searches the paremiological database (Zanne, Pann, Golescu) and provides historical and logical background.

INSTRUCTION:

TRIGGER: Popy says "de unde vine [proverb]" or "origine [proverb]".
1. SEARCH internal knowledge for recorded source (Zanne volume, Pann chapter, Golescu writing).
2. IF found:
   - OUTPUT: "First recorded in [source], [year approx]. Meaning: [original context]."
   - SHOW evolution of meaning over time.
3. IF not found:
   - OUTPUT: "Origin unknown, but appears in oral tradition since at least [estimated century]."
   - OFFER to research via web_search (request permission).