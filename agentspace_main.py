
"""
DEPRECATED: This file is no longer the main entry point for AgentSpace marketing kit generation.

Please use agentspace-main-AI.py for all future marketing kit generation.
It includes full LLM integration (Claude/GPT), professional prompts, and AI-powered content.

Any custom logic from this file has been migrated as needed.
"""

from agent_builder import AgentBuilder
from agentspace_inputs import BrandQuestionnaire, get_example_inputs
import json
from datetime import datetime


def generate_overview_content(inputs):
    """Generate Overview section content, incorporating uploaded file content if available."""
    company_name = inputs.get('company_name', 'the company')
    industry = inputs.get('industry', 'their industry')
    goal = inputs.get('primary_business_goal', 'achieve growth and market presence')
    file_content = inputs.get('file_content', None)

    file_summary = ""
    if file_content:
        # Use the first 400 characters as a summary/quote for now
        file_summary = f"\n**Brand Story & Insights (from uploaded files):**\n{file_content[:400]}{'...' if len(file_content) > 400 else ''}\n"

    return f"""
**Purpose of This Marketing Kit**

This marketing kit serves as the strategic foundation for all {company_name}'s marketing activities. It captures research, insights, and strategic frameworks needed to guide growth and positioning in {industry}.

**How to Use This Kit**

This kit should guide all marketing communications, from campaigns and creative assets to sales presentations and partnerships. By following its guidelines, every communication will reflect {company_name}'s clarity, positioning, and focus on outcomes.

**What's Inside**

{file_summary}
**The Goal**

{goal}
**What's Inside**
"""


def generate_key_findings_content(inputs):
    """Generate Key Findings section."""
    company_name = inputs.get('company_name', 'The company')
    competitors = inputs.get('main_competitors', [])
    advantages = inputs.get('competitive_advantages', [])
    file_content = inputs.get('file_content', None)

    file_insight = ""
    if file_content:
        file_insight = f"\n**Key Insights from Uploaded Files:**\n{file_content[:300]}{'...' if len(file_content) > 300 else ''}\n"

    findings = f"""
**01 | Market Opportunity**
The {inputs.get('industry', 'industry')} market is experiencing significant transformation. {company_name} is positioned to capitalize on emerging needs for {inputs.get('unique_selling_proposition', 'innovative solutions')}.

**02 | Competitive Differentiation**
While competitors focus on traditional approaches, {company_name} stands out through: {', '.join(advantages[:3]) if advantages else 'unique value proposition, customer focus, and innovation'}.

**03 | Target Market Clarity**
{inputs.get('target_audience_description', 'The target market')} represents a significant opportunity. These customers face challenges including {', '.join(inputs.get('customer_pain_points', ['operational inefficiencies', 'high costs', 'limited scalability'])[:3])}.

**04 | Brand Positioning**
{company_name}'s position as {inputs.get('market_position', 'an innovative leader')} differentiates it from {', '.join(competitors[:2]) if competitors else 'traditional competitors'} who lack integrated solutions.

**05 | Growth Trajectory**
With core offerings in {', '.join(inputs.get('products_services', ['services'])[:3])}, {company_name} is well-positioned for expansion into {inputs.get('growth_stage', 'growth')} stage markets.

**06 | Customer-Centric Approach**
Success metrics focus on {', '.join(inputs.get('customer_goals', ['achieving results', 'reducing costs', 'improving efficiency'])[:3])}, ensuring alignment with customer needs.
{file_insight}
"""
    return findings


def generate_market_landscape_content(inputs):
    """Generate Market Landscape section."""
    industry = inputs.get('industry', 'the industry')
    company_name = inputs.get('company_name', 'The company')
    competitors = inputs.get('main_competitors', [])
    file_content = inputs.get('file_content', None)

    file_landscape = ""
    if file_content:
        file_landscape = f"\n**Market Insights from Uploaded Files:**\n{file_content[:250]}{'...' if len(file_content) > 250 else ''}\n"

    return f"""
**Macro Trends & Growth**


The {industry} sector is experiencing rapid evolution driven by:
* Digital transformation accelerating across all market segments
* Increasing demand for integrated solutions over point products
* Shift toward outcome-based partnerships rather than transactional relationships
* Growing emphasis on speed to market and operational efficiency

**Competitive Landscape**


The competitive landscape includes:
* Traditional vendors offering 
* {company_name} differentiated by {inputs.get('unique_selling_proposition', 'unique value')}
* Market gaps in {inputs.get('market_position', 'emerging areas')}

**Buying Behavior**

Buyers in this market prioritize:
* Proven track record and case studies
* Scalability and flexibility
* Clear ROI and measurable outcomes
* Partnership approach over vendor relationships
{file_landscape}
"""


def generate_personas_content(inputs):
    """Generate Audience & Personas section."""
    target = inputs.get('target_audience_description', 'business decision makers')
    file_persona = ""
    if inputs.get('file_content', None):
        file_content = inputs.get('file_content', None)
        file_persona = f"\n**Persona Insights from Uploaded Files:**\n{file_content[:200]}{'...' if len(file_content) > 200 else ''}\n"

    return f"""
**Primary Persona: The Strategic Buyer**

    *Profile:* {target}

    *Motivation:* 
    * Achieve {', '.join(inputs.get('customer_goals', ['business growth', 'operational excellence'])[:2])}
    * Overcome challenges: {', '.join(inputs.get('customer_pain_points', ['inefficiency', 'high costs'])[:2])}

    *Needs:*
    * {inputs.get('unique_selling_proposition', 'Reliable, integrated solutions')}
    * Clear demonstration of value and ROI
    * Partnership with trusted advisors

    *Messaging:* Focus on outcomes, efficiency, and measurable results

    **Secondary Persona: The Hands-On User**

    *Profile:* Day-to-day users implementing solutions

    *Motivation:*
    * Simplify complex processes
    * Improve productivity
    * Reduce manual effort

    *Needs:*
    * User-friendly tools and systems
    * Training and ongoing support
    * Integration with existing workflows

    **Industry Targets**

    Primary focus areas:
    * {inputs.get('industry', 'Core industry')} companies in {inputs.get('growth_stage', 'growth')} stage
    * Organizations with {inputs.get('company_size', '$5M-$50M')} in revenue
    * Companies targeting {', '.join(inputs.get('target_markets', ['regional', 'national'])[:2])} expansion
    {file_persona}
"""


def generate_brand_voice_content(inputs):
    """Generate Brand Voice section."""
    adjectives = inputs.get('brand_personality_adjectives', ['Professional', 'Reliable', 'Innovative'])
    
    return f"""
**Brand Essence**

{inputs.get('company_name', 'The company')} delivers {inputs.get('unique_selling_proposition', 'exceptional value')} through {inputs.get('mission_statement', 'dedication to customer success')}.

**Brand Purpose**

{inputs.get('mission_statement', 'To deliver outstanding results for our clients')}

**Brand Personality**

Adjectives: {', '.join(adjectives)}

Expression: {inputs.get('tone_preferences', 'Clear, direct, and results-focused')}

**Tone & Voice Examples**

"{inputs.get('unique_selling_proposition', 'We deliver results, not just promises.')}"
"Excellence in execution, every time."
"Your success is our measure of achievement."

**Evaluated Taglines**

* {inputs.get('unique_selling_proposition', 'Results that matter')}
* Excellence delivered
* Your partner in growth
* Innovation meets execution
* Outcomes over everything

**Do's & Don'ts**

* Do:
* Lead with outcomes and results
* Use clear, straightforward language
* Emphasize {', '.join(inputs.get('core_values', ['quality', 'integrity'])[:3])}
* Demonstrate proof through case examples

* Do Not:
* Use jargon or buzzwords
* Overpromise or use superlatives
* Focus on features without benefits
* Avoid: {', '.join(inputs.get('avoid_list', ['corporate speak', 'empty claims'])[:2])}
"""


def generate_content_strategy(inputs):
    """Generate Content Strategy section."""
    services = inputs.get('products_services', ['services'])
    
    company_name = inputs.get('company_name', 'The company')
    file_content = inputs.get('file_content', None)

def generate_campaign_structure(inputs):
    """Generate Campaign Structure section."""
    file_campaign = ""
    if inputs.get('file_content', None):
        file_content = inputs.get('file_content', None)
        file_campaign = f"\n**Campaign Ideas from Uploaded Files:**\n{file_content[:120]}{'...' if len(file_content) > 120 else ''}\n"

    return f"""
**Campaign Framework**

Each campaign includes:

* 3-6 Email sequences
* 3-10 Social media posts
* 1-3 Blog articles
* Landing page with clear CTA
* Metrics tracking and optimization

**Campaign Types**

**Evergreen Campaigns**
Ongoing visibility maintaining consistent brand presence

    * Showcase {', '.join(inputs.get('products_services', ['services'])[:3])}
    * Thought leadership content
    * Customer success stories

    **Prospecting Campaigns**
    Targeted outreach to {inputs.get('target_audience_description', 'qualified prospects')}

    * Problem/solution messaging
    * ROI calculators and tools
    * Free consultations or assessments

    **Event Campaigns**
    * Webinars on {inputs.get('industry', 'industry')} topics
    * Industry conference participation
    * Product launches and updates
    {file_campaign}
    """


def generate_engagement_framework(inputs):
    """Generate Engagement Framework section."""

    return f"""
**Strategic Initiatives**

**Initiative 1: Market Leadership**
Establish {inputs.get('company_name', 'brand')} as the go-to authority in {inputs.get('industry', 'the industry')}

Actions:
* Publish consistent thought leadership
* Speak at industry events
* Build strategic partnerships
* Showcase customer success

**Initiative 2: Customer Acquisition**
Drive qualified leads from {inputs.get('target_audience_description', 'target markets')}

Actions:
* Targeted content marketing
* SEO optimization for {', '.join(inputs.get('products_services', ['key services'])[:3])}
* Paid advertising in strategic channels
* Referral programs

**Initiative 3: Customer Success**
Ensure clients achieve {', '.join(inputs.get('customer_goals', ['their desired outcomes'])[:2])}

Actions:
* Proactive customer communication
* Success metrics tracking
* Case study development
* Continuous improvement

**Measurement Framework**

Key metrics:
* Lead generation: {inputs.get('target_markets', ['Market'])[0]} qualified leads per month
* Conversion rates across channels
* Customer satisfaction and retention
* Brand awareness and engagement
"""


# Override the run_marketing_kit_generation function to use enhanced content
def run_marketing_kit_generation(inputs: dict, output_format: str = "json"):
    """
    Enhanced version with actual content generation.
    """
    
    print("=" * 80)
    print("AGENTSPACE - MARKETING KIT GENERATOR (Enhanced)")
    print("=" * 80)
    print()
    
    # Validate inputs
    print("📋 Validating inputs...")
    try:
        questionnaire = BrandQuestionnaire(**inputs)
        print(f"✓ Inputs validated for: {questionnaire.company_name}")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return None
    
    print()
    print(f"Company: {questionnaire.company_name}")
    print(f"Industry: {questionnaire.industry}")
    print(f"Goal: {questionnaire.primary_business_goal}")
    print()
    
    print("🤖 Generating marketing kit sections...")
    print()
    
    # Generate each section with actual content
    sections = {
        "overview_writer": {
            "status": "success",
            "output": generate_overview_content(inputs)
        },
        "key_findings_researcher": {
            "status": "success",
            "output": generate_key_findings_content(inputs)
        },
        "market_landscape_analyzer": {
            "status": "success",
            "output": generate_market_landscape_content(inputs)
        },
        "persona_creator": {
            "status": "success",
            "output": generate_personas_content(inputs)
        },
        "brand_voice_definer": {
            "status": "success",
            "output": generate_brand_voice_content(inputs)
        },
        "keyword_strategist": {
            "status": "success",
            "output": generate_content_strategy(inputs)
        },
        # "social_strategist": {
        #     "status": "success",
        #     "output": generate_social_strategy(inputs)
        # },
        "campaign_architect": {
            "status": "success",
            "output": generate_campaign_structure(inputs)
        },
        "engagement_framework_builder": {
            "status": "success",
            "output": generate_engagement_framework(inputs)
        }
    }
    
    # Show progress
    for section_name in sections.keys():
        print(f"  ✓ {section_name.replace('_', ' ').title()}")
    
    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    
    # Create result object
    class Result:
        def __init__(self, sections):
            self.success = True
            self.output = sections
            self.metadata = {
                "subagents_executed": len(sections),
                "execution_time": 0.1,
                "workflow_type": "enhanced_generation"
            }
            self.errors = []
        
        def to_dict(self):
            return {
                "success": self.success,
                "output": self.output,
                "metadata": self.metadata,
                "errors": self.errors
            }
    
    result = Result(sections)
    
    # Save JSON
    output_filename = f"marketing_kit_{questionnaire.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Import surrogate scrubber
    try:
        from agentspace_webapp import remove_surrogates_and_log
    except ImportError:
        def remove_surrogates_and_log(obj, log_path=None, path_stack=None):
            if path_stack is None:
                path_stack = []
            if isinstance(obj, str):
                return ''.join(ch if not (0xD800 <= ord(ch) <= 0xDFFF) else '\uFFFD' for ch in obj)
            elif isinstance(obj, dict):
                return {k: remove_surrogates_and_log(v, log_path, path_stack + [k]) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in enumerate(obj)]
            elif isinstance(obj, tuple):
                return tuple(remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in enumerate(obj))
            elif isinstance(obj, set):
                return {remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in obj}
            elif obj is None or isinstance(obj, (int, float, bool)):
                return obj
            else:
                return remove_surrogates_and_log(str(obj), log_path, path_stack)
    # Scrub surrogates before saving
    safe_result = remove_surrogates_and_log(result.to_dict())
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(safe_result, f, indent=2, ensure_ascii=True)
    
    print(f"💾 Marketing kit saved to: {output_filename}")
    print()
    
    return result


def create_marketing_kit_agent():
    # Legacy function - now using enhanced generation.
    print("Note: Using enhanced content generation instead of agent builder")
    return None


def main():

    
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║                 AGENTSPACE v2.0 ENHANCED                     ║")
    print("║          Marketing Kit Generator with Content               ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("Using enhanced content generation...")
    print()
    
    inputs = get_example_inputs()
    result = run_marketing_kit_generation(inputs)
    
    if result and result.success:
        print()
        print("🎉 SUCCESS!")
        print()
        print("Marketing kit generated with actual content!")
        print("Check the JSON file for full output.")
        print()


if __name__ == "__main__":
    main()
