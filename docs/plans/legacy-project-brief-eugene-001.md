
# Eugene Strat — Project Specification

## 1. Project Overview

## Core Philosophy
A productivity meta-layer tool that transforms how users capture, organize, and execute on ideas. It integrates GTD (Getting Things Done) principles with strategic visualization, data-driven insights.

---

Eugene Strat is a tool for people who refuse to work reactively.

In a world designed to fragment your attention, it creates space to step back: see all your projects at once, decide what actually matters, and understand where your time goes.

Not another task manager. A place to think.

The product captures two data streams—**projects** (what you're working on, scored by cost/benefit) and **sessions** (time-boxed focus blocks)—then synthesizes them into Strava-style performance intelligence: capacity patterns, focus quality trends, strategic alignment over time.

**Core loop:** Plan → Execute → Analyze → Improve.

---

## 1.5 Core Concepts

Foundational vocabulary. These definitions are design decisions, not just labels.

### Project

**User-facing definition:**
> Anything you want to invest focus time in and track strategically. Big or small. One session or fifty. If it deserves a place on your map, it's a project.

**System definition:**
A project is an entity that:
- Belongs to one user
- Has a name
- Has cost (1-10) and benefit (1-10) scores — its map coordinates
- Has a status lifecycle: `active` → `completed` | `archived`
- Can receive focus sessions
- Optionally belongs to a category and has tags

**What a project is NOT:**
- A task list (no subtasks, no checklists)
- A container for documents or files
- Scoped by duration or complexity — a 30-minute task and a 300-hour initiative are both valid projects

**Design rationale:**
The cost/benefit scoring normalizes projects of any scale. A quick win (cost:2, benefit:8) and a major endeavor (cost:9, benefit:9) sit in the same strategic space. The map reveals what matters, regardless of size.

---

### Session

**User-facing definition:**
> A time-boxed block of focused work on a specific project. You commit before starting, then reflect after finishing.

**System definition:**
A session is an entity that:
- Belongs to one user and one project
- Has a planned duration (pre-commitment)
- Has an actual duration (reality)
- Has a status lifecycle: `planned` → `active` → `completed` | `abandoned`
- Captures self-assessed quality (1-5) on completion
- Optionally includes a goal (intent) and notes (reflection)

**Design rationale:**
Sessions are the raw data for performance intelligence. Every session logged is a data point: time spent, on what, with what quality, achieving what goal. Patterns emerge from aggregation.

---

### Category

**User-facing definition:**
> A broad bucket for organizing projects by life domain. Default: Work, Learn, Build, Manage.

**System definition:**
- User-defined, mutable (can rename, delete, create)
- Projects optionally belong to one category
- Tags are scoped within categories

**Design rationale:**
Categories answer "what domain of life is this?" They're the top level of the organizational hierarchy: Category → Tag → Project.

---

### Tag

**User-facing definition:**
> A label within a category for grouping related projects. Example: under "Work," you might have tags for "Nexus," "Client-X," "Internal."

**System definition:**
- User-defined, scoped to a category
- Projects can have multiple tags (many-to-many)
- Tags enable cross-project analytics ("time spent on Nexus")

**Design rationale:**
Tags replace sub-projects. Instead of nesting projects, you tag them. This keeps the structure flat (strategic altitude) while allowing flexible grouping for filtering and analytics.

## **TODO**
- inspirition from apps that works well like : 
  - Things3 for project categorization
  - Notion For ProjecT DB 
  - Name it ... 