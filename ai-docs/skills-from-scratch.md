---
title: "Building an AI Agent Skill from Scratch: The Fork Terminal Tool"
author: "IndyDevDan"
source_url: "Not provided"
date: "2025-12-16"
original_format: "transcript"
document_type: "technical_walkthrough"
word_count_estimate: 5500
confidence_level: "high"
keywords: ["agentic engineering", "LLM skills", "cursor IDE", "progressive disclosure", "fork terminal", "Claude Code", "Gemini CLI", "Astral UV"]
glossary_terms: ["Agent Skill", "Progressive Disclosure", "In-loop Agentic Coding", "Context Window", "Astral UV", "Cookbook Pattern", "Pivot File"]
key_quotes_count: 4
processing_notes:
  extraction_confidence: 
    structure: "high"
    glossary: "high"
    quotes: "high"
  glossary_sources:
    successful: ["Agent Skill", "Progressive Disclosure", "Context Window", "Astral UV"]
    context_derived: ["Cookbook Pattern", "Pivot File"]
  structural_changes: ["Linearized the build process from the conversational flow", "Corrected transcript errors (e.g., 'Asian forward' to 'Agent forward', 'cloud code' to 'Claude Code')"]
  ambiguity_flags: []
---

# Building an AI Agent Skill from Scratch: The Fork Terminal Tool

## Executive Summary
This technical walkthrough details the engineering process of building a custom "Skill" for AI agents from the ground up, specifically creating a **Fork Terminal Tool**. The author, IndyDevDan, advocates for "in-loop agentic coding," where the engineer actively plans and orchestrates the AI's output rather than passively relying on it.

The core objective is to create a reusable skill that allows an operating agent to "fork" its current conversation into a new terminal window—either to execute a raw CLI command or to spin up a secondary agent (Claude, Gemini, or Codex) with a summarized context. Key architectural patterns introduced include the **"Pivot File"** (`skill.md`) for central logic, the **"Cookbook"** for progressive disclosure of instructions, and the use of **Astral UV** for Python tooling. The guide emphasizes the philosophy of "beginning with the end in mind" to prevent dependency on AI tools and ensure robust system design.

## Glossary of Key Terms

* **Agent Skill**: A modular capability that allows an AI agent to deploy prompts and code against a specific problem in a consistent, reusable way. [Definition derived from document context]
* **Pivot File (`skill.md`)**: The central Markdown file in a skill directory that defines the skill's purpose, triggers, and logic, acting as the entry point for the agent. [Definition derived from document context]
* **Progressive Disclosure**: An interaction design pattern where information (or prompt instructions) is revealed to the agent only when necessary, preventing context overload. [Source: *Nielsen Norman Group / Industry Standard*]
* **In-loop Agentic Coding**: A development methodology where the human engineer maintains high presence and effort, orchestrating the AI agent step-by-step rather than deferring entire tasks to the AI ("out-of-loop"). [Definition derived from document context]
* **Cookbook Pattern**: A directory structure containing specific Markdown files (recipes) that provide detailed instructions for specific use cases (e.g., specific CLI tools), referenced only when needed by the main skill. [Definition derived from document context]
* **Astral UV**: An extremely fast Python package installer and resolver, written in Rust, used here for managing Python dependencies and scripts. [Source: *Astral Documentation*]
* **Context Window**: The limit on the amount of text (tokens) an LLM can process at one time; forking terminals is a strategy to manage this limitation by offloading tasks. [Source: *Academic/Industry General*]

## Key Quotations

> "Skills let you deploy prompts and code against any problem in a consistent, reusable way."
>
> — **IndyDevDan** (context: Defining the core value proposition of building custom skills for LLMs.)

> "I think none of that matters if you don't begin with the end in mind. If you don't actually fully understand what you want to see... Engineers' brains are rotting due to this incredible technology... The point here is to always understand what you're asking your agents to accomplish for you."
>
> — **IndyDevDan** (context: Emphasizing the necessity of human planning and architectural thought before engaging AI tools.)

> "The only things you need to focus on are the primitives that make it all up. The context, model, prompt, and tools, the core four. If you understand these, if you master these, you'll master the agent."
>
> — **IndyDevDan** (context: summarizing the fundamental building blocks of AI engineering.)

> "We're trading off speed and context for better performance."
>
> — **IndyDevDan** (context: Explaining why the agent is instructed to read help documentation before executing commands, even if it takes longer.)

---

## 1. Engineering Philosophy and Planning

Before writing code, the process begins with offline planning ("pen and paper"). The goal is to define the concrete output structures and the "end state" of the session.

### The "Core Four" Primitives
To master agentic engineering, one must focus on four primitives:
1.  **Context**: The information available to the model.
2.  **Model**: The specific LLM being used (e.g., Claude 3.5 Sonnet, Gemini 2.5).
3.  **Prompt**: The instructions given to the model.
4.  **Tools**: The capabilities the model can call upon (scripts, CLIs).

### The Problem and Solution
* **Problem**: Long-running agent sessions clutter context windows. Engineers need to parallelize work or offload specific tasks without losing the main thread.
* **Solution**: A **Fork Terminal Skill**. This allows an agent to spawn a new terminal window, summarize the current work, and hand off that context to a new agent or execute a raw command in parallel.

## 2. System Architecture

The skill is structured to maximize modularity and utilize **Progressive Disclosure**.



### The File Structure
The project is initialized with a specific directory hierarchy:
* `claude/skills/`: The root directory for agent skills.
    * `skill.md`: The **Pivot File**. It progressively discloses how the skill works to the operating agent.
    * `tools/`: Contains single-file scripts and command-line tools (e.g., Python scripts using Astral UV).
    * `prompts/`: specific user prompts (e.g., `fork_summary_user_prompt.md`).
    * `cookbook/`: Additional documentation loaded conditionally.
        * `cli_command.md`: Instructions for raw CLI usage.
        * `claude_code.md`: Instructions for Claude agents.
        * `gemini_cli.md`: Instructions for Gemini agents.

## 3. Implementation Step-by-Step

### Step 1: The Pivot File (`skill.md`)
This file defines when the skill is used. It contains:
* **Description**: "Fork a new terminal session to a new window using raw CLI command."
* **Triggers**: When the user requests "fork terminal," "create new terminal," or "new terminal."
* **Variables**: Boolean flags to enable/disable specific features (e.g., `enable_gemini_cli`, `enable_raw_cli`).
* **Routing Logic**: Simple `if/then` statements that direct the agent to the `cookbook` files based on the user's request.

### Step 2: The Forking Mechanism (Python Script)
A Python script is created in the `tools/` directory to handle the actual window management.
* **Tooling**: Uses **Astral UV** for dependency management.
* **OS Integration**: Uses `osascript` (AppleScript) to spawn new Terminal windows on macOS (with provisions for PowerShell on Windows).
* **Logic**:
    1.  Accepts a command string.
    2.  Opens a new terminal window.
    3.  Navigates to the **Current Working Directory** (critical for context preservation).
    4.  Executes the command.

### Step 3: The Cookbook (Progressive Disclosure)
Instead of stuffing all instructions into one prompt, the system uses a "Cookbook" approach. The agent reads these files *only* when the specific tool is requested.

| Cookbook File | Purpose | Key Instructions |
| :--- | :--- | :--- |
| **`cli_command.md`** | Handling raw commands (curl, ffmpeg). | "Before executing, run `[command] --help` to understand options." |
| **`claude_code.md`** | Spawning Anthropic agents. | Definitions for "Fast" (Haiku) vs. "Base" (Sonnet) vs. "Heavy" (Opus) models. |
| **`gemini_cli.md`** | Spawning Google agents. | Logic for Gemini 2.5 Flash vs. Gemini 3 Pro. |

**Key Tactic**: The instructions force the agent to run `--help` on a tool before using it. This ensures the agent understands the specific version and capabilities of the CLI it is about to use, reducing hallucinations.

### Step 4: Context Forking and Summarization
To make the fork useful, the new agent needs context from the previous session.

1.  **The Prompt Template**: A file (`fork_summary_user_prompt.md`) is created in YAML format.
2.  **The Workflow**:
    * **Base Agent**: Reads the conversation history.
    * **Summarization**: Compresses the history into the YAML template (User Prompt -> Response Summary).
    * **Handoff**: The Base Agent constructs a command that initializes the **Fork Agent** with this summary as its starting prompt.
3.  **Result**: The new terminal window opens with a fresh agent that already "knows" what happened in the previous session, but with a cleared context window.



## 4. Testing and Iteration
The development process followed a rigorous "Proof of Concept" (PoC) to "MVP" cycle:

1.  **PoC**: Verify `osascript` can open a terminal and run `ffmpeg --help`.
2.  **Debugging**:
    * *Issue*: Forked terminals opening in the root directory.
    * *Fix*: Updated script to explicitly `cd` into the current working directory before execution.
    * *Issue*: Permission denied errors on scripts.
    * *Fix*: Added `chmod +x` steps.
    * *Issue*: Agent overwriting the summary file rather than reading it.
    * *Fix*: Clarified prompt instructions: "Don't update the file directly. Just read it and use it to craft a new prompt."
3.  **Scaling**: Once the pattern was established for Claude, it was replicated for Codex and Gemini using the `cookbook` structure.

## 5. Conclusion
The Fork Terminal Skill demonstrates how to structure complex AI behaviors using simple primitives. by treating code, prompts, and documentation as interchangeable parts of a "Skill," engineers can:
* **Scale Compute**: Run multiple agents in parallel.
* **Preserve Context**: Summarize and hand off work effectively.
* **Standardize Operations**: Ensure agents use tools consistently via the `cookbook` definitions.

The final system allows a user to simply type:
`Fork session codex cli. Summarize work done.`
And the system automatically summarizes the current state, spawns a new window, boots a Codex agent, and feeds it the context to continue working.

---

### Next Step for User
Would you like me to generate the actual **Python script code** using `subprocess` and `osascript` mentioned in the document, or draft the **YAML summary template** for the prompt strategy?