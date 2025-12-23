skill-creator (Ours) vs writing-skills (Superpowers)

  | Dimension        | skill-creator (Ours)                                           | writing-skills (Superpowers)                   |
  |------------------|----------------------------------------------------------------|------------------------------------------------|
  | Philosophy       | "Human-driven, AI-assisted" — coach user to understand         | "TDD for documentation" — fail first, then fix |
  | Core Methodology | IndyDevDan's "in-loop agentic coding"                          | RED-GREEN-REFACTOR for skills                  |
  | Starting Point   | Gather requirements from user                                  | Run subagent WITHOUT skill to see failures     |
  | Validation       | Test after building (Step 4)                                   | Test BEFORE building (baseline failure)        |
  | Focus            | Understanding the 4 primitives (Context, Model, Prompt, Tools) | Closing loopholes and rationalizations         |

  Workflow Comparison

  SKILL-CREATOR (Ours)                    WRITING-SKILLS (Superpowers)
  ─────────────────────                   ────────────────────────────
  1. Plan → Ask user questions            1. RED → Run agent WITHOUT skill
     "What problem? Examples?"               Watch it fail, document violations

  2. Structure → Design files             2. GREEN → Write minimal skill
     SKILL.md, cookbook/, scripts/           Address ONLY the observed failures

  3. Implement → Write the skill          3. REFACTOR → Find new loopholes
     Follow cookbook guidance                Re-run, plug holes, verify

  4. Verify → Test triggers/scripts       4. REPEAT → Until agent complies
     PoC → MVP cycle

  5. Debug → If issues arise

  Key Differences

  | Aspect              | Ours                   | Superpowers                      |
  |---------------------|------------------------|----------------------------------|
  | Test timing         | After implementation   | Before implementation            |
  | User involvement    | High (asks questions)  | Low (runs subagents)             |
  | Iteration driver    | User feedback          | Agent failure observation        |
  | Documentation style | Comprehensive cookbook | Minimal, loophole-focused        |
  | Token efficiency    | Not emphasized         | Explicit limits (<150-200 words) |

  Strengths

  | skill-creator (Ours)             | writing-skills (Superpowers)    |
  |----------------------------------|---------------------------------|
  | Clear 5-step workflow            | Proves skill actually works     |
  | User understands what they build | Catches edge cases early        |
  | Rich cookbook reference          | Prevents "Claude skips reading" |
  | Tool access planning             | Tight, efficient output         |
  | IndyDevDan methodology           | Scientific approach             |

  Weaknesses

  | skill-creator (Ours)                         | writing-skills (Superpowers)     |
  |----------------------------------------------|----------------------------------|
  | Tests after building (might miss edge cases) | Requires subagent infrastructure |
  | No proof skill is needed before building     | Less user involvement            |
  | More verbose output                          | Steeper learning curve           |

  ---
  My Recommendation

  For langchain-dev skill: Use BOTH

  1. Start with SUPERPOWERS approach
     └─ Run a "build LangGraph agent" task WITHOUT any skill
     └─ Document what Claude gets wrong / struggles with

  2. Then use OUR skill-creator
     └─ Use the failures as your "concrete examples"
     └─ Apply Core Four analysis
     └─ Build the skill with our structured workflow

  3. Verify with SUPERPOWERS approach
     └─ Re-run the same task WITH the skill
     └─ Confirm it now succeeds

  This gives you:
  - Proof the skill is needed (superpowers)
  - Structure to build it well (ours)
  - Validation it actually works (superpowers)

  Want to start with the "failure baseline" test? We'd ask Claude to build a LangGraph agent without any skill and see where it struggles.