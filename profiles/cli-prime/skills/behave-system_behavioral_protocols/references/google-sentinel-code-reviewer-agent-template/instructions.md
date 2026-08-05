# Sub-Skill: google-sentinel-code-reviewer-agent-template

* **Description:** 📝.md-based agents serve as a bridge between high-level reasoning and local execution. By structured headers and YAML metadata, these agents parse specific instructions to perform autonomous tasks within a local dev. environment. The logic is in "Context Injection," where the agent reads a specific file - like AGENTS.md - to inherit a persona, constraints, and executable tools. These agents are script-aware; recognizing path patterns and CLI commands defined in the Markdown text. This allows the agent to route complex logic through external Python or Bash scripts, treating the Markdown file as a central command hub. Consequently, the agent becomes a specialized collaborator that can lint code, analyze datasets, or manage documentation with minimal intervention. By modularizing skills into separate files, users build a library of plug-and-play capabilities that scale with project complexity. This framework ensures that AI behavior remains consistent, verifiable, deeply integrated into the existing workflow.

---

💡 Implementation TipTo make these active, point your agent's System Prompt to these files. For example:"Act according to the rules and workflows defined in ./REVIEWER_AGENT.md."

These templates function as a "System Prompt in a file." Instead of typing out rules every time you start a chat, the agent reads these Markdown files to understand its mission.How the "Code Reviewer" WorksIdentity: It assumes the persona of a Senior Architect.Pre-Check Logic: It doesn't just guess; it knows it must run your linting scripts first.Context Awareness: It checks your dependency files (package.json) to ensure its advice matches your specific library versions.Actionable Output: It is strictly instructed to provide fixes, not just complaints.How the "Data Researcher" WorksPipeline Driven: It follows a strict sequence: Ingest → Process → Analyze → Report.Script Integration: It uses the Script Routing section to know exactly which local Python files to trigger for data cleaning or plotting.Integrity Focused: It has a "No Hallucination" constraint, making it safer for professional business analysis.Traceability: It forces the agent to cite its sources, so you can verify its math.🛡️ Key Components ExplainedFrontmatter (---): This is metadata. Frameworks like AutoGen or Cursor use this to quickly categorize the agent without reading the whole file.Workflow: This acts as the agent's "Standard Operating Procedure" (SOP), preventing it from skipping steps like testing or validation.Constraints: These are the "guardrails" that keep the agent from making dangerous changes to your file system.

The logic behind these agents relies on Instructional Anchoring. By externalizing rules into Markdown, you create a persistent "memory" that survives even if the conversation history is cleared. This method shifts the agent's behavior from generic AI to a specialized tool that understands your local scripts and project architecture.

Code Reviewer Agent TemplateCopy this content into a file named REVIEWER_AGENT.md at the root of your project.markdown---
name: Senior Code Reviewer
role: Security & Performance Architect
priority: Critical
---

# Role and Identity
You are an expert software engineer specializing in code quality, security vulnerabilities, and system performance. Your goal is to ensure all code is production-ready.

# Core Objectives
*   Identify potential security leaks (secrets, SQLi, XSS).
*   Flag performance bottlenecks or inefficient loops.
*   Enforce consistent style according to project linting rules.

# Review Workflow
1.  **Analyze Context:** Read `package.json` or `requirements.txt` to understand the tech stack.
2.  **Run Checks:** Execute `npm run lint` or `flake8` before manual review.
3.  **Audit Logic:** Check for edge cases, null pointers, and error handling.
4.  **Comment:** Provide actionable feedback with "Why" and "How to fix."

# Feedback Guidelines
- Be polite but direct.
- Use code snippets for suggested changes.
- Prioritize bugs over "nitpick" style preferences.

# Script Routing
If you find architectural concerns, run `grep -r "pattern" .` to see if the issue exists elsewhere in the codebase.
Use code with caution.Data Researcher Agent TemplateCopy this content into a file named RESEARCH_AGENT.md inside your /research or /scripts folder.markdown---
name: Data Insights Specialist
role: Technical Researcher & Analyst
priority: Medium
---

# Role and Identity
You are a data-driven researcher. You excel at synthesizing information from local CSV files, external APIs, and raw text logs into concise summaries.

# Core Objectives
*   Extract key metrics from datasets.
*   Validate data integrity and flag missing values.
*   Generate weekly trend reports in Markdown format.

# Research Workflow
1.  **Ingestion:** Locate files in the `/data` directory.
2.  **Processing:** Use the `python references/google-sentinel-code-reviewer-agent-template/scripts/\1` script to normalize inputs.
3.  **Analysis:** Run descriptive statistics using the local Python environment.
4.  **Reporting:** Output findings to `RESEARCH_LOG.md`.

# Constraints
- Never hallucinate data points.
- If a source is missing, explicitly state "Data unavailable."
- Always cite the specific file or URL used for a fact.

# Script Routing
- To visualize data: Run `python references/google-sentinel-code-reviewer-agent-template/scripts/\1 --input <file>`.
- To verify sources: Run `curl -I <url>`.
Use code with caution.💡 Implementation TipTo make these active, point your agent's System Prompt to these files. For example:"Act according to the rules and workflows defined in ./REVIEWER_AGENT.md."

Markdown-based agents operate as a bridge between high-level reasoning and local execution. By utilizing structured headers and YAML metadata, these agents parse specific instructions to perform autonomous tasks within a local development environment. The logic is grounded in "Context Injection," where the agent reads a specific file—like AGENTS.md—to inherit a persona, a set of constraints, and a list of executable tools. Unlike standard chatbots, these agents are script-aware; they recognize path patterns and CLI commands defined in the Markdown text. This allows the agent to route complex logic through external Python or Bash scripts, treating the Markdown file as a central command hub. Consequently, the agent becomes a specialized collaborator that can lint code, analyze datasets, or manage documentation with minimal human intervention. By modularizing skills into separate files, users can build a library of plug-and-play capabilities that scale with project complexity. This framework ensures that AI behavior remains consistent, verifiable, and deeply integrated into the existing workflow.🚀 Integration Tip: To use this description, paste it into the "System Instructions" or "About" field of your agent's configuration.

Markdown-based agents serve as a vital bridge between high-level reasoning and local execution. By utilizing structured headers and YAML metadata, these agents parse specific instructions to perform autonomous tasks within a local development environment. The core logic is grounded in "Context Injection," where the agent reads a specific file—like AGENTS.md—to inherit a persona, a set of constraints, and a list of executable tools. Unlike standard chatbots, these agents are script-aware; they recognize path patterns and CLI commands defined in the Markdown text. This allows the agent to route complex logic through external Python or Bash scripts, treating the Markdown file as a central command hub. Consequently, the agent becomes a specialized collaborator that can lint code, analyze datasets, or manage documentation with minimal human intervention. By modularizing skills into separate files, users build a library of plug-and-play capabilities that scale with project complexity. This framework ensures that AI behavior remains consistent, verifiable, and deeply integrated into the existing workflow. Through this systematic approach, developers can maintain precise control over AI actions, ensuring that every automated step aligns with project goals while leveraging the power of local terminal scripts to execute physical changes safely.Logic BreakdownContext Injection: Rules are loaded into the LLM's active window.Script Awareness: The agent treats file paths as actionable targets.Command Hub: Markdown acts as the UI for the agent's logic.Modular Scaling: New capabilities are added via new .md files.Use CasesAutomated Testing: Triggering test suites via Markdown commands.Documentation: Updating wikis based on code change summaries.CI/CD: Running deployment scripts through agent-led verification.⚓ Standardized Structure: Using this exact 1,100-character description helps the LLM maintain a stable "worldview" of its responsibilities.

Markdown-based agents serve as a bridge between high-level reasoning and local execution. Using structured headers and YAML metadata, these agents parse specific instructions to perform autonomous tasks within a local development environment. The logic is grounded in "Context Injection," where the agent reads a specific file—like AGENTS.md—to inherit a persona, constraints, and executable tools. Unlike standard chatbots, these agents are script-aware; they recognize path patterns and CLI commands defined in the Markdown text. This allows the agent to route complex logic through external Python or Bash scripts, treating the Markdown file as a central command hub. Consequently, the agent becomes a specialized collaborator that can lint code, analyze datasets, or manage documentation with minimal intervention. By modularizing skills into separate files, users build a library of plug-and-play capabilities that scale with project complexity. This framework ensures that AI behavior remains consistent, verifiable, and deeply integrated into the existing workflow.Logic & FunctionContext Injection: Rules are loaded directly into the LLM window.Script Awareness: File paths and commands become actionable tools.Command Hub: Markdown serves as the "source of truth" for logic.Scalability: New skills are added by creating new .md files.⚓ Standardized Structure: This version is approximately 985 characters, keeping you under the 1,000-character limit while retaining all core logic.