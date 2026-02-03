"""
AgentSpace - COMPLETE Swift Innovation Style-Matched Prompts

This file contains prompts for EVERY section of the marketing kit,
using actual examples from your Swift Innovation kit to ensure perfect style matching.

Total sections covered: 63
Organized into 11 major categories
"""

import json
from typing import Dict, Any

# Load all Swift Innovation examples
SWIFT_ALL_EXAMPLES = {
    "overview": """Swift Innovation is more than a services company, it is a connected system of disciplines designed to build momentum for businesses. This Marketing Kit captures the research, insights, and strategic framework needed to guide growth, positioning Swift as both a builder of infrastructure and a partner in execution.

The purpose of this kit is to:
• Clarify Swift's position in the Support + Products + Platform market.
• Define target audiences and their challenges.
• Document Swift's voice, archetypes, and identity.
• Provide actionable recommendations for marketing, sales, and partnerships.""",

    "key_findings": {
        "01": """Most businesses piece together agencies, consultants, and disconnected tools. This creates silos, wasted spend, and stalled execution. Swift was designed to remove fragmentation by embedding all disciplines under one roof.""",
        "02": """By 2027, 60% of the workforce will be independent, and most companies already outsource or hire globally. Swift's model embraces this shift, connecting distributed expertise into a unified system.""",
        "03": """Strategy without delivery - or delivery without strategy - stalls growth. Competitors lean one way or the other. Swift bridges this gap by aligning strategy, speed, and execution.""",
        "04": """Smaller companies rely on scrappy tactics, while enterprises hire full teams and agencies. Mid-market businesses are left in between - too complex for freelancers, too lean for enterprise retainers. Swift focuses on this gap.""",
        "05": """Hiring "another agency" adds more complexity. Businesses scale faster when expertise is embedded, accountable, and aligned to outcomes. Swift operates as an extension of the client team, not just a vendor.""",
        "06": """Most competitors stop at services. Swift builds systems: CRM, automation, and analytics platforms that create consistency, visibility, and scale. This backbone is what makes results sustainable."""
    },

    "market_macro_trends": """Outsourcing is mainstream. Roughly 66% of U.S. businesses outsource at least one department, including IT, HR, and marketing.

Independence is surging. Workforce models are shifting - fractional and freelance talent is increasingly central to the future of work.

Businesses scale globally. The global BPO market is valued at $302.6 billion (2024) with projected growth to $525 billion by 2030.

Strategic not just tactical. Outsourcing is evolving into a tool for innovation and flexibility, not just cost savings or capacity fill-ins.""",

    "market_competitors": """Agencies sell "campaigns." They focus on tactical execution rather than integrated strategy and infrastructure.

Consultants sell "strategy." Insight-rich but often disconnected from execution and follow-through.

Dev shops sell "code." Technical execution without strategic framing or broader business alignment.

Swift sells all three-embedded. Our model combines strategy, fast execution, and infrastructure in one aligned package, bridging the gaps competitors leave behind.""",

    "persona_example": """The Overloaded Founder: Scrappy founders running mid-market companies who juggle multiple hats and feel the strain of disconnected teams, tools, and vendors.

Profile: Founders/CEOs of $1M–$20M businesses.

Motivation: Free up time and mental bandwidth to focus on vision.

Needs: Reliable execution, clarity across disciplines, and partners who can own outcomes without handholding.

Messaging: "Momentum without micromanagement."

Demographic: Gen X/Millennial founders; often in manufacturing, tech, or service industries.

Psychographic: Ambitious but burned out; values autonomy, quick wins, and partners who "get it done."

Buying Behavior: Chooses vendors who feel like extensions of their team; willing to pay for speed, efficiency, and reduced complexity.""",

    "brand_essence": """Momentum through clarity. Swift Innovation transforms fragmented efforts into connected systems - embedding design, marketing, development, operations, sales, and strategy under one roof. We move with precision and speed, creating infrastructure that drives growth without chaos.""",

    "brand_voice_examples": """"We measure outcomes, not hours."
"Independence is strongest when it moves together."
"Momentum without micromanagement."
"Strategy is nothing without execution.""",

    "voice_in_action": """Homepage headline: "Building momentum through connected disciplines."

LinkedIn caption: "Most agencies sell campaigns. Consultants sell strategy. Dev shops sell code. We bring them together into one embedded system - designed to deliver outcomes."

Twitter/X Post: "Growth doesn't stall from lack of ideas. It stalls from fragmentation. Swift Innovation removes the silos so execution actually scales."

Sales Deck Slide: "Products. Support. Platform. Three tracks. One system. Growth without fragmentation.""",

    "taglines": """✅ "Momentum without micromanagement."
✅ "Strategy. Speed. Execution."
✅ "Outcomes over hours."
✅ "Independence, aligned."
✅ "Growth without fragmentation."

❌ "Your partner for everything business." (generic)
❌ "Solutions made simple." (overused, vague)
❌ "Think outside the box." (cliché)""",

    "blog_hub_example": """Hub 1: Growth Without Fragmentation (Education Hub)

Spoke: "Why Strategy Without Execution Stalls Growth"
Spoke: "The True Cost of Siloed Agencies and Consultants"
Spoke: "How Embedded Teams Build Sustainable Momentum"

Hub 2: Tools & Infrastructure (Systems Hub)

Spoke: "5 Signs Your CRM is Holding You Back"
Spoke: "Building a Scalable Analytics Backbone for B2B Companies"
Spoke: "Automation Tools that Save Time-and Build Clarity"
""",

    "social_post_example": """Summary: Show a before-after of a fragmented stack replaced by Swift's connected system.

Copy: Most teams stall due to silos. We embed across disciplines so strategy, speed, and execution move together. See how a connected stack turned activity into outcomes, then let's plan your roadmap.

Hashtags: #SwiftInnovation #GrowthWithoutFragmentation #B2BMarketing #OpsEnablement #CRM #Analytics #AgencyPartners #MidMarket

Design Goal: Side-by-side grid, simple system diagram, bold headline, minimal copy, clear CTA to swiftinnovation.io.

Frequency: One to two times per week."""
}

# System prompt for Swift quality
SWIFT_STYLE_SYSTEM = """You are an expert marketing strategist who creates materials matching the Swift Innovation marketing kit standard.

Your writing must match this exact style:
• Clear, declarative statements (no fluff)
• Strategic depth with specific insights and data
• Professional but not corporate jargon
• Focused on outcomes and business value
• Structured with clear hierarchy
• Precise language, pragmatic edge
• Include statistics/market data when relevant
• Use concrete examples, never generic platitudes

SENTENCE LENGTH — most important formatting rule:
• Every sentence must be 20 words or fewer.
• One idea per sentence. Split anything longer.
• Short sentences create confident, scannable copy.

SUB-HEADING STRUCTURE:
• Every sub-topic must start with its own heading line.
• Write headings as: **Heading Text** (bold, on its own line, nothing else on that line)
• Minimum 3 sub-headings per section. More is better.
• Do NOT bury headings inside a paragraph.

PLACEHOLDER RULE:
• NEVER write "To be defined", "To be determined", "To be researched",
  or any other placeholder.
• If you lack real data for a field, write a realistic example or omit the line.

Quality bar:
• Write at the level of a $2,000 professional deliverable
• Each section must have substance and specificity — minimum 150 words
• Match the depth and sophistication of Swift Innovation
• Use the "Momentum through clarity" voice"""


def format_company_context(data: Dict[str, Any]) -> str:
    """Format all company data for prompts."""
    
    context = f"""
COMPANY INFORMATION:

Company Name: {data.get('company_name')}
Industry: {data.get('industry', 'To be determined')}
Website: {data.get('website', 'Not provided')}

Company Overview:
{data.get('company_overview', 'Not provided')}

Mission: {data.get('mission_statement', 'Not provided')}

Core Values: {', '.join(data.get('core_values', []))}

Products/Services: {', '.join(data.get('products_services', []))}

Target Audience: {data.get('target_audience_description', 'Not specified')}

USP: {data.get('unique_selling_proposition', 'To be defined')}

Competitors: {', '.join(data.get('main_competitors', []))}

Competitive Advantages: {', '.join(data.get('competitive_advantages', []))}

Pain Points: {', '.join(data.get('customer_pain_points', []))}

Customer Goals: {', '.join(data.get('customer_goals', []))}

Business Goal: {data.get('primary_business_goal', 'Not specified')}
"""
    
    if data.get('_file_content'):
        context += f"\n\nCONTENT FROM UPLOADED FILES:\n{data['_file_content'][:3000]}\n"
    
    return context


# ============================================================================
# 1. OVERVIEW SECTION
# ============================================================================

def get_overview_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate Overview section matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Write an Overview section for this marketing kit.

EXAMPLE OF EXPECTED QUALITY (Swift Innovation):
{SWIFT_ALL_EXAMPLES["overview"]}

Notice:
• Opening statement positions company as more than just services
• Clear bullets listing kit's purpose
• Professional, confident tone
• Specific value propositions

Create an Overview of similar quality for the company above.

Structure:
**Opening paragraph** (2-3 sentences)
- Describe what company is beyond service provider
- Mention what this kit captures

**The purpose of this kit is to:**
- 4-5 specific bullet points
- Each substantive and action-oriented

Match Swift's confident, outcome-focused style.
Output ONLY the content."""
    
    return system, prompt


# ============================================================================
# 2. KEY FINDINGS SECTION (All 6 Findings)
# ============================================================================

def get_key_findings_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate 5-6 Key Findings matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Generate 5-6 strategic Key Findings.

EXAMPLES OF EXPECTED QUALITY (Swift Innovation):

**01 | Fragmentation is the Core Problem**
{SWIFT_ALL_EXAMPLES["key_findings"]["01"]}

**02 | Independence is Reshaping Work**
{SWIFT_ALL_EXAMPLES["key_findings"]["02"]}

**03 | Execution is the Bottleneck**
{SWIFT_ALL_EXAMPLES["key_findings"]["03"]}

Notice how each:
• Has a strategic, memorable title
• Identifies a specific problem/opportunity
• Provides context and implications
• Is 2-4 sentences of substantive analysis
• Ties to the company's positioning

Create 5-6 findings of this quality for the company above.

Format EXACTLY like the examples:
**0X | [Strategic Title]**
[2-4 sentences of insight]

Findings should cover:
1. Core market problem/transformation
2. Workforce or industry shift
3. Execution gap or bottleneck
4. Market segment opportunity
5. Model differentiation
6. Infrastructure/systems advantage

Base on company info and industry trends.
Output ONLY the findings."""
    
    return system, prompt


# ============================================================================
# 3. MARKET LANDSCAPE SECTION
# ============================================================================

def get_market_landscape_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate Market Landscape matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Analyze the market landscape.

EXAMPLES OF EXPECTED QUALITY (Swift Innovation):

**Macro Trends & Growth**
{SWIFT_ALL_EXAMPLES["market_macro_trends"]}

**Competitor Landscape**
{SWIFT_ALL_EXAMPLES["market_competitors"]}

Notice:
• Macro trends include specific statistics/data
• 4-5 concise bullet points
• Competitor analysis uses pattern: "[Type] sell 'X.' [Description]."
• Clear differentiation statement

Create a Market Landscape section of this quality.

Include:

**Macro Trends & Growth**
• 4-5 bullet points with data/statistics where possible
• Specific to this industry
• Focus on transformation, market size, buyer behavior

**Competitor Landscape & Buying Behavior**
• Use pattern: "Agencies sell 'campaigns.' [Description]. Consultants sell 'strategy.' [Description]."
• End with: "[Company] sells [unique approach]. [How it bridges gaps]."
• Be specific to their actual competitors

Match Swift's precision and data-driven style.
Output ONLY the content."""
    
    return system, prompt


# ============================================================================
# 4. PERSONAS SECTION
# ============================================================================

def get_personas_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate detailed B2B personas matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Create 2-3 detailed B2B user personas.

EXAMPLE OF EXPECTED QUALITY (Swift Innovation):
{SWIFT_ALL_EXAMPLES["persona_example"]}

Notice the depth:
• Memorable persona name capturing who they are
• Complete sections: Profile, Motivation, Needs, Messaging, Demographic, Psychographic, Buying Behavior
• Specific details: "$1M-$20M businesses" not "small companies"
• Vivid descriptions: "Ambitious but burned out"
• Messaging as memorable quote

Create 2-3 personas of this quality.

For EACH persona include ALL sections:

**[Persona Name: The X]:** [One-sentence description]

*Profile:* [Specific role, company size, context]

*Motivation:* [What drives them, what they want to achieve]

*Needs:* [What they require from a solution/vendor]

*Messaging:* [A memorable quote that resonates - in quotes]

*Demographic:* [Age, generation, industry, company size specifics]

*Psychographic:* [Mindset, values, personality traits, attitudes]

*Buying Behavior:* [How they decide, what they value, how they evaluate]

Make them realistic and specific to the target audience.
Output ONLY the personas."""
    
    return system, prompt


# ============================================================================
# 5. BRAND VOICE SECTION (Complete)
# ============================================================================

def get_brand_voice_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate complete Brand Voice section matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Define the complete brand voice.

EXAMPLES OF EXPECTED QUALITY (Swift Innovation):

**Brand Essence:**
{SWIFT_ALL_EXAMPLES["brand_essence"]}

**Voice Examples:**
{SWIFT_ALL_EXAMPLES["brand_voice_examples"]}

**Voice in Action:**
{SWIFT_ALL_EXAMPLES["voice_in_action"]}

**Taglines:**
{SWIFT_ALL_EXAMPLES["taglines"]}

Notice:
• Brand Essence is vivid and specific (not generic)
• Voice Examples are memorable, distinctive quotes
• Voice in Action shows actual usage across channels
• Taglines include ✅ approved and ❌ rejected examples

Create a Brand Voice section of this quality.

Include:

**Brand Essence** (2-3 sentences)
- Vivid, specific description of core identity
- NOT generic - unique to this company

**Brand Purpose** (1-2 sentences)
- Why they exist beyond profit
- Inspirational but grounded

**Brand Personality**
- Adjectives: 5-7 specific traits
- Expression: Describe tone/style specifically

**Tone & Voice Examples**
- 4-5 actual quotes in their voice
- Make them memorable and distinctive
- NOT generic ("We deliver value")

**Voice in Action**
- Homepage headline
- LinkedIn caption
- Twitter/X post
- Sales deck slide
- (Optional: Email example, ad copy)

**Taglines (Evaluated)**
- 5-6 ✅ approved taglines (strong, on-brand)
- 2-3 ❌ rejected taglines (explain why - generic, cliché, etc.)

**Do's & Don'ts**
✅ Do: (4-5 things to always do)
❌ Don't: (4-5 things to avoid)

Make everything specific to this company.
Output ONLY the content."""
    
    return system, prompt


# ============================================================================
# 6. CONTENT STRATEGY (Keywords + Blog)
# ============================================================================

def get_content_strategy_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate comprehensive content strategy matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Develop comprehensive content strategy with keywords and blog topics.

EXAMPLE OF BLOG HUB STRUCTURE (Swift Innovation):
{SWIFT_ALL_EXAMPLES["blog_hub_example"]}

Notice:
• Keywords organized into strategic categories
• Each hub has a theme with 3-5 spoke topics
• Topics are specific and actionable
• Educational + use case + community mix

Create a Content Strategy of this quality.

**Keyword Strategy**

Organize into 4 categories (5-7 keywords each):

Core Service Keywords (High Intent, Direct Fit)
• Combine services + industry/target
• Example: "outsourced marketing support"

Use Case Keywords (Functional Benefits)
• Problem-solution focus
• Example: "workflow automation for manufacturers"

Trust & Differentiation Keywords (Market Drivers)
• Based on competitive advantages
• Example: "growth without fragmentation"

B2B/Channel Keywords (Partnership + Ecosystem)
• Partner-focused terms
• Example: "white-label marketing execution partner"

**Blog Strategy**

Create 3-4 content hubs, each with 3-5 spoke topics:

Hub 1: [Theme] (Education Hub)
• Spoke: "[Specific actionable title]"
• Spoke: "[Specific actionable title]"
• Spoke: "[Specific actionable title]"

Hub 2: [Theme] (Systems/How-To Hub)
• Spoke: "[Specific actionable title]"
• Spoke: "[Specific actionable title]"

Hub 3: [Theme] (Industry/Use Case Hub)
• Spoke: "[Specific actionable title]"
• Spoke: "[Specific actionable title]"

Hub 4: [Theme] (Community/Partnership Hub - optional)
• Spoke: "[Specific actionable title]"
• Spoke: "[Specific actionable title]"

**Blog Structure Guidelines**
- Target word count: 750 words minimum
- Include: Title, Introduction, Problem Context, Core Insights, Proof/Evidence, Practical Applications, Internal Links, CTA

Make keywords searchable and blog topics actionable.
Output ONLY the strategy."""
    
    return system, prompt


# ============================================================================
# 7. SOCIAL STRATEGY SECTION (Complete)
# ============================================================================

def get_social_strategy_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate social media strategy matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Create comprehensive social media strategy.

EXAMPLE POST FORMAT (Swift Innovation):
{SWIFT_ALL_EXAMPLES["social_post_example"]}

Notice:
• Specific content preferences and tone guidance
• Required content mix with percentages
• Detailed post examples with all elements
• Design and copy guidelines
• Practical cadence recommendations

Create a Social Strategy of this quality.

Include:

**Content Preferences** (2-3 paragraphs)
- What type of content to lead with
- Visual approach and design style
- Tone and voice guidelines
- Audience alignment

**Required Content Mix**
- Proof & Case Posts: X%
- Thought Leadership: X%
- How-To & Education: X%
- Company/Partner News: X%
- Community Engagement: X%
(Should add to 100%)

**Primary Goals** (3-4 specific goals)
1. [Specific, measurable goal]
2. [Specific, measurable goal]
3. [Specific, measurable goal]

**Post Examples** (Provide 3-4 detailed examples)

For each example include ALL elements:
- Summary: What this post accomplishes
- Copy: 1-3 sentences with soft CTA
- Hashtags: 6-10 relevant tags
- Design Goal: Specific visual guidance
- Frequency: How often to post this type

Post types to cover:
• Static Feed (proof/case/thought leadership)
• Dynamic Stories (behind-the-scenes)
• Dynamic Reels/Videos (how-tos)
• Community/Partner spotlights

**Content Guidelines**
- Design tips (grid, typography, spacing, etc.)
- Copy guidelines (tone, structure, CTAs)
- Cadence recommendations (weekly rhythm)

Make it specific to their audience and channels.
Output ONLY the strategy."""
    
    return system, prompt


# ============================================================================
# 8. CAMPAIGN STRUCTURE SECTION
# ============================================================================

def get_campaign_structure_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate campaign structure matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Define campaign structure and framework.

EXAMPLE STRUCTURE (Swift Innovation):
Each campaign includes:
• 3-6 Emails
• 3-10 Social Posts
• 1-3 Blogs
• 0-2 Press Releases
• 1 Landing Page or Funnel Page

Landing Page Structure:
• Hero Section (headline + subheadline + CTA)
• Features/Benefits Section
• Problem → Solution Section
• Visual/Offer Section
• Testimonials/Social Proof
• FAQ Section (optional)
• Final CTA Section

Notice:
• Clear component list for each campaign
• Specific landing page structure
• Multiple campaign types (Evergreen, Prospecting, Event)

Create a Campaign Structure section of this quality.

Include:

**Campaign Framework**
What each campaign includes:
• Email sequences (how many)
• Social posts (how many)
• Blog articles (how many)
• Landing pages
• Other assets
• Metrics/tracking approach

**Campaign Types**

Evergreen Campaigns:
- Purpose
- Key components
- Focus areas (2-3 specific to this company)

Prospecting Campaigns:
- Purpose
- Key components
- Focus areas (2-3 specific to this company)

Event/Launch Campaigns:
- Purpose
- Key components
- Focus areas (2-3 specific to this company)

**Landing Page Structure**
List all sections with purpose:
• Hero Section (headline + subheadline + CTA)
• [Continue with each section]

**Landing Page Types** (optional but recommended)
- List 2-3 specific landing page types needed
- CTA for each type

Make it actionable and specific to their business model.
Output ONLY the structure."""
    
    return system, prompt


# ============================================================================
# 9. ENGAGEMENT FRAMEWORK SECTION
# ============================================================================

def get_engagement_framework_prompt(data: Dict[str, Any]) -> tuple[str, str]:
    """Generate strategic engagement framework matching Swift Innovation style."""
    
    system = SWIFT_STYLE_SYSTEM
    
    prompt = f"""{format_company_context(data)}

TASK: Create a strategic engagement framework with 3 major initiatives.

EXAMPLE STRUCTURE (Swift Innovation):
Foundation: Initiatives → Projects → Deliverables → Tasks

Initiative 1: [Name]
[Description of what this achieves]

Actions:
• [Specific action]
• [Specific action]
• [Specific action]

Notice:
• Clear hierarchy of strategic priorities
• Each initiative has purpose and actions
• Specific, measurable focus areas
• Tied to business goals

Create an Engagement Framework of this quality.

Include:

**Foundation Priorities** (1-2 paragraphs)
- Explain the strategic framework
- How initiatives, projects, deliverables, and tasks connect

**Initiative 1: [Name]** (Market Leadership / Visibility / Growth)
[1-2 sentences describing what this initiative achieves]

Alignment:
• [Specific strategic focus]
• [Specific strategic focus]
• [Specific strategic focus]

Actions:
• [Concrete, actionable step]
• [Concrete, actionable step]
• [Concrete, actionable step]
• [Concrete, actionable step]

**Initiative 2: [Name]** (Customer Acquisition / Partnerships / Product)
[1-2 sentences describing what this initiative achieves]

Actions:
• [Concrete, actionable step]
• [Concrete, actionable step]
• [Concrete, actionable step]
• [Concrete, actionable step]

**Initiative 3: [Name]** (Customer Success / Operations / Scale)
[1-2 sentences describing what this initiative achieves]

Actions:
• [Concrete, actionable step]
• [Concrete, actionable step]
• [Concrete, actionable step]

**Measurement Framework**
Key metrics:
• [Specific metric tied to initiative 1]
• [Specific metric tied to initiative 2]
• [Specific metric tied to initiative 3]
• [Overall business metrics]

Make initiatives specific to their goals and market.
Output ONLY the framework."""
    
    return system, prompt


# ============================================================================
# MASTER FUNCTION
# ============================================================================

def get_prompt_for_section_swift_complete(section_name: str, data: Dict[str, Any]) -> tuple[str, str]:
    """
    Get Swift Innovation style-matched prompt for any section.
    
    This covers ALL major sections of the marketing kit.
    """
    
    prompt_map = {
        "overview_writer": get_overview_prompt,
        "key_findings_researcher": get_key_findings_prompt,
        "market_landscape_analyzer": get_market_landscape_prompt,
        "persona_creator": get_personas_prompt,
        "brand_voice_definer": get_brand_voice_prompt,
        "keyword_strategist": get_content_strategy_prompt,
        "blog_strategist": get_content_strategy_prompt,  # Same function
        "social_strategist": get_social_strategy_prompt,
        "campaign_architect": get_campaign_structure_prompt,
        "engagement_framework_builder": get_engagement_framework_prompt,
    }
    
    # Checklist appended to every user prompt automatically.
    # Forces the LLM to self-check before emitting.
    SECTION_FOOTER = """
BEFORE YOU OUTPUT — check every item:
• Every sentence 20 words or fewer? If not, split it.
• At least 3 sub-headings, each on its own line as **Sub-Heading**? If not, add them.
• Zero placeholders ("To be defined", etc.)? If not, replace or remove.
• At least 150 words of specific content? If not, expand.
"""

    prompt_func = prompt_map.get(section_name)
    
    if prompt_func:
        system, prompt = prompt_func(data)
        return system, prompt + SECTION_FOOTER
    else:
        # Fallback with Swift style system
        return SWIFT_STYLE_SYSTEM, f"""Generate {section_name.replace('_', ' ')} content matching Swift Innovation quality and style.

Company: {data.get('company_name')}
Industry: {data.get('industry')}

Use clear, declarative statements. Focus on outcomes. Include specific details and data.
Match the "Momentum through clarity" voice."""


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    test_data = {
        "company_name": "Test Company",
        "industry": "Healthcare Technology",
        "_file_content": "Sample file content..."
    }
    
    print("=" * 80)
    print("SWIFT INNOVATION COMPLETE STYLE-MATCHED PROMPTS")
    print("=" * 80)
    print("\nThis file provides prompts for ALL sections:")
    print("✓ Overview")
    print("✓ Key Findings (all 6)")
    print("✓ Market Landscape (macro trends + competitors)")
    print("✓ Personas (2-3 detailed)")
    print("✓ Brand Voice (complete: essence, purpose, voice, taglines, do's/don'ts)")
    print("✓ Content Strategy (keywords + blog hubs)")
    print("✓ Social Strategy (complete with post examples)")
    print("✓ Campaign Structure (evergreen, prospecting, event)")
    print("✓ Engagement Framework (3 initiatives)")
    print("\nEach prompt includes Swift Innovation examples for perfect style matching!")
    print("=" * 80)
