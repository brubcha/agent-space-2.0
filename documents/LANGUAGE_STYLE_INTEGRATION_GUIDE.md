# ✍️ LANGUAGE STYLE CONTROL - Complete Guide

## What This Is

**Language styling controls HOW words are written, separate from visual design.**

This is about:

- ✅ Sentence structure and length
- ✅ Active vs passive voice
- ✅ Tone and pacing
- ✅ Power words and vocabulary
- ✅ Distinctive voice patterns
- ✅ Punctuation style

**NOT about fonts, colors, or layout** (that's visual design)

---

## 🎯 SWIFT INNOVATION LANGUAGE ANALYSIS

### What We Discovered:

**Sentence Structure:**

- Average: **14.3 words** per sentence
- **31% short** sentences (<10 words)
- **56% medium** sentences (10-20 words)
- **13% long** sentences (>20 words)
- Result: **Punchy, varied rhythm**

**Voice:**

- **97% active voice** (minimal passive)
- **Declarative statements** (not questions)
- **Confident, direct** tone

**Power Words (Swift's vocabulary):**

- momentum (16x)
- execution (33x)
- outcomes (20x)
- embedded (21x)
- infrastructure (16x)
- clarity (13x)
- fragmentation (11x)
- connected (11x)

**Signature Patterns:**

```
"X sells 'Y'" - Competitor differentiation
"without [noun]" - Positioning (6x fragmentation, 3x micromanagement)
"Not X. Y." - Contrast for emphasis
```

**Distinctive Voice Examples:**

```
"We measure outcomes, not hours."
"Independence is strongest when it moves together."
"Momentum without micromanagement."
"Strategy is nothing without execution."
```

**Punctuation:**

- Colons: **Frequent** (79 uses) - for lists, elaboration
- Em dashes: **Rare** (0 uses)
- Quotes: **Selective** (6 uses) - for emphasis only

---

## 📦 PRE-BUILT LANGUAGE STYLES

### 1. Swift Innovation Voice

```
Tone: Confident, Precise, Strategic, Modern
Sentence: 14 words avg, 30% short for impact
Voice: 95% active, declarative statements
Power Words: momentum, clarity, execution, outcomes
Pattern: "X sells 'Y'", "without [noun]"
Rhythm: Punchy, short paragraphs
```

**When to use:** B2B services, consulting, agencies

---

### 2. Professional Corporate

```
Tone: Professional, Authoritative, Trustworthy
Sentence: 18 words avg, flowing
Voice: 80% active, formal
Power Words: excellence, integrity, commitment, expertise
Pattern: "We are committed to", "Through our comprehensive"
Rhythm: Flowing, medium paragraphs
```

**When to use:** Finance, legal, enterprise

---

### 3. Tech Modern

```
Tone: Direct, Modern, Efficient, Bold
Sentence: 12 words avg, 40% short
Voice: 95% active, ultra-direct
Power Words: transform, scale, automate, accelerate
Pattern: "Built for", "Ship faster", "Zero [pain]"
Rhythm: Fast-paced, punchy
```

**When to use:** SaaS, tech startups, software

---

### 4. Creative Bold

```
Tone: Bold, Creative, Energetic, Distinctive
Sentence: 13 words avg, varied length
Voice: 90% active, personality-driven
Power Words: unleash, ignite, breakthrough, vibrant
Pattern: "Imagine [scenario]", "What if [question]"
Rhythm: Varied, creative
```

**When to use:** Creative agencies, DTC brands

---

### 5. Consultative Expert

```
Tone: Insightful, Analytical, Credible
Sentence: 16 words avg, measured
Voice: 85% active, data-driven
Power Words: insight, analysis, framework, metrics
Pattern: "Our analysis shows", "Based on research"
Rhythm: Methodical, medium paragraphs
```

**When to use:** Consulting, research, advisory

---

### 6. Accessible Friendly

```
Tone: Friendly, Clear, Approachable
Sentence: 13 words avg, conversational
Voice: 95% active, engaging
Power Words: simple, easy, clear, practical
Pattern: "Here's how", "Think of it like"
Rhythm: Conversational, short paragraphs
```

**When to use:** Consumer brands, education, SMB

---

## 🔧 HOW TO USE

### In Your Prompts:

```python
from agentspace_language_styles import get_language_style, get_language_style_instructions

# Get style
style = get_language_style("swift_innovation")

# Get writing instructions
instructions = get_language_style_instructions(style)

# Add to your prompt:
prompt = f"""
{company_context}

{instructions}

Now write the Overview section following this language style.
"""
```

---

## 📊 BEFORE vs AFTER

### Generic AI Writing:

```
Our company provides comprehensive solutions that enable
organizations to achieve their strategic objectives through
innovative approaches and best-in-class methodologies.
```

- Passive voice
- Vague ("comprehensive solutions")
- Wordy (25 words, meandering)
- Corporate jargon
- No punch

### Swift Innovation Style:

```
Most businesses piece together agencies, consultants, and
disconnected tools. This creates silos, wasted spend, and
stalled execution. Swift was designed to remove fragmentation
by embedding all disciplines under one roof.
```

- Active voice
- Specific (names the problem)
- Punchy (3 sentences, 14/9/15 words)
- Clear language
- Rhythmic

---

## ✍️ LANGUAGE PATTERNS TO FOLLOW

### Swift's Signature Patterns:

**1. Competitor Differentiation:**

```
Pattern: "X sells 'Y'"

Examples:
"Agencies sell 'campaigns.' They focus on tactical execution."
"Consultants sell 'strategy.' Insight-rich but disconnected."
"Dev shops sell 'code.' Technical without strategic framing."
"Swift sells all three-embedded."
```

**2. Without [Noun] Positioning:**

```
Pattern: "[Benefit] without [pain point]"

Examples:
"Growth without fragmentation"
"Momentum without micromanagement"
"Execution without delay"
"Scale without overhead"
```

**3. Not X. Y. Contrast:**

```
Pattern: "Not [old way]. [New way]."

Examples:
"Not another vendor. A connected partner."
"Not hours. Outcomes."
"Not services. Systems."
```

**4. Declarative + Short:**

```
Pattern: One-sentence punch

Examples:
"Swift was designed to remove fragmentation."
"Strategy without delivery stalls growth."
"Infrastructure is the differentiator."
```

---

## 🎨 COMBINING VISUAL + LANGUAGE

### Complete Style Control:

```python
# Visual Design
from agentspace_design_styles import get_design_system
visual = get_design_system("swift_innovation")

# Language Style
from agentspace_language_styles import get_language_style
language = get_language_style("swift_innovation")

# Generate with BOTH
generate_marketing_kit(
    company_data=data,
    visual_design=visual,     # Colors, fonts, layout
    language_style=language   # Writing voice, tone, patterns
)
```

**Result:** Content that LOOKS like Swift AND READS like Swift! ✨

---

## 📈 INTEGRATION EXAMPLES

### Example 1: Healthcare Tech with Swift Voice

```python
visual = get_design_system("healthcare_professional")  # Medical blue
language = get_language_style("swift_innovation")      # Punchy, strategic

# Result: Healthcare colors + Swift confidence
```

### Example 2: Tech Startup - All Modern

```python
visual = get_design_system("tech_startup")    # Purple, compact
language = get_language_style("tech_modern")  # Fast, direct

# Result: Cohesive modern tech vibe
```

### Example 3: Finance - Conservative + Expert

```python
visual = get_design_system("finance_corporate")      # Navy, serif
language = get_language_style("consultative_expert") # Data-driven

# Result: Trustworthy, authoritative
```

---

## 🚀 QUICK START

### Step 1: Choose Language Style

```python
from agentspace_language_styles import get_language_style

style = get_language_style("swift_innovation")
```

### Step 2: Add to Prompts

```python
instructions = get_language_style_instructions(style)

# Include in each section prompt:
prompt = f"""
{company_info}

WRITING STYLE:
{instructions}

Write the [section] following this style exactly.
"""
```

### Step 3: Generate

AI will now write in Swift Innovation voice!

---

## ✅ CHECKLIST FOR SWIFT STYLE

When reviewing AI output, check:

- [ ] Average sentence: ~14 words
- [ ] 30% sentences are short (<10 words)
- [ ] Active voice dominates
- [ ] Uses power words (momentum, execution, outcomes)
- [ ] Includes "without [noun]" pattern
- [ ] Declarative statements, minimal questions
- [ ] Frequent colons for lists
- [ ] Quotes only for emphasis
- [ ] Short paragraphs (2-4 sentences)
- [ ] Punchy rhythm

---

## 🎊 SUMMARY

### What You Control:

✅ Sentence length and structure
✅ Active vs passive voice ratio
✅ Power vocabulary
✅ Signature language patterns  
✅ Tone and pacing
✅ Punctuation style
✅ Paragraph rhythm

### What You Get:

**Generic AI:**
"Our organization provides comprehensive solutions..."

**Swift Style:**
"Most businesses piece together agencies, consultants, and disconnected tools..."

**The difference is VOICE!** ✨

---

## 📚 NEXT STEPS

### Today:

1. Add language style to your prompts
2. Generate same content in 2-3 styles
3. Compare the difference

### This Week:

1. Perfect Swift Innovation style matching
2. Test with real client content
3. Get feedback on voice

### This Month:

1. Build library of language styles
2. Match each client's voice
3. Deliver content that SOUNDS like them

---

**You now control HOW words are written, not just WHAT is written!** ✍️🎯
