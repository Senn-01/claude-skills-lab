# feedback on docs/plans/2025-12-23-eugene-design.md

**Contemplative Review**
The Vision (As I Understand It)
Eugene exists to create strategic clarity from the chaos of thoughts, ideas, and commitments. It's a meta-layer — not another task manager, but the nervous system that helps you see what matters.
Core promise: "Signal from noise."
You capture everything without friction. Eugene helps you see what deserves your finite attention. The matrix shows strategic reality. The journal holds reflection. External tools handle execution details.

What the Docs Get Right
AspectAssessmentMeta-layer positioningClear. No sub-tasks. Linear/Notion handle granularity.PrimitivesSolid. inbox_item → project → journal_note. Clean lifecycle.Agent architectureSound. Supervisor + workers. Scalable.GTD fundamentalsPresent. Capture everything, process to zero, 2-minute rule.Cost/benefit matrixStrong differentiator. Strategic, not temporal.Event sourcingForward-thinking. Enables future ANALYZE.PersonaDefined. Silent executor. Not chatty.Voice pipelineTechnically sound. Streaming, interruptible.



## Helicopter view of what we want to build - At the end, we create an AGENTIC time management tool.  
Agentic SaaS, minimalistic, retro-futuristic, voice-first, using best-in-class inspirations from other project management tools.

Website is divided for front end in two parts:
- a braindump (GTD like) multimodal for frictionless CAPTURE.
- then a second part with : 
    - PLAN: Strategic Center (matrix, kanban notion style with things3 principles, Inbox of CAPTURE processing)
    - EXECUTE: time-boxing possibility on projects on the map (later : deep focus principles added)
    - ANALYZE: Insightfull data, BI for personal reflection and improvement.
    - JOURNAL : personal journal for personal reflection and improvement. (obsidian like)

This means that our voice agent should first understand those choices and route accordingly. (first MVP)
(Later we want REMINDERS, ROUTING TO EXTERNAL TOOLS (mcp connectors), etc.)
This means we need to carefully plan our backend architecture to be able to support this.

## Core Philosophy

We are committed to an voice Agent First design philosophy. This Agent is the solid(**todo** define persona) **PARTNER** like Hal-9000 in 2001: A Space Odyssey. 

Our motto is: **"Those who plan the future tend to create it"**

**IMPORTANT** 
    - Any Questions, design choices, should be oriented with this lens. 
    - For example: connector? use mcp. Agent is our brain, nervous system of our app. we need to create a DB ? build with Ai retrieval and efficiency in mind?
    - Any Design choice should ask before if we are inspiring from the best in their domain tool.

---
### Inspired by

#### from indydevdan - Agentic SaaS
- Agentic Coding 2.0 (The Conductor)
    Agents that conduct other agents.
    * **Structure**: You prompt a "Lead Agent" (Executive/Conductor). The Lead Agent spawns specialized "Command Level Agents" (Worker/Sub-agents) with specific system prompts and playbooks.
    * **Shift**: The engineer moves from being a lead developer to an executive managing a digital workforce.

- UI vs. Agents (Agents Eat SaaS)
    Agents are becoming the interface. Software-as-a-Service (SaaS) platforms that force users to click through slow UIs will be disrupted by agents that interact with the database/API directly.
    * **Prediction**: The best UIs will become prompt interfaces where the user states an intent, and a swarm of agents executes the CRUD operations in the background.

- Multi-Agent Orchestration
    One agent is no longer enough. The trend is moving from single-stream prompting to running 3, 5, or 10 agents in parallel or sequence.
    * **Benefit**: Redundancy and verification. What one reviewer misses, three will find.
    * **Technique**: Using cross-validation between agents to increase the reliability of the final output.

- Tool Calling is the Opportunity
    According to OpenRouter data, only **15% of output tokens are tool calls**, despite reasoning models taking up 50% of usage.
    * **The Gap**: Most usage is still text generation. The biggest opportunity lies in increasing the density of tool calls (actions taken by the agent).
    * **The Metric**: Long chains of correct tool calls are the direct proxy for "impact" and "trust."

---
## UI/UX Design Principles
 
 **High-Signal, Low-Noise:**
 **Frictionless Input:** 
 **Minimalism & Focus:** 
 **Thematic Cohesion:**
 **Reflective and professional Feedback:** 

 - **The tagline should reflect:**
  - Professional sophistication
  - Strategic thinking
  - time-boxing (could be extended to Deep focus)
  - Awareness/mindfulness
  - Genuine Time focus and management gains.

  It integrates proven methodologies (GTD capture, Deep Work principles, visual project management) with elegant execution and thoughtful design.



## Our Core Principles
SOLID building blocks, clear RULES, then design by Emergence. 

This means we build on really simple bases first, and build complexity from there whil having the long-term vision in mind.