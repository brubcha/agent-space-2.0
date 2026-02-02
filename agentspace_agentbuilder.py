from agent_builder import AgentBuilder
from agentspace_inputs import BrandQuestionnaire, get_example_inputs
from datetime import datetime
import json

# Section logic functions (copied from your current implementation)
def overview_writer(inputs):
    return generate_overview_content(inputs)

def key_findings_researcher(inputs):
    return generate_key_findings_content(inputs)

def market_landscape_analyzer(inputs):
    return generate_market_landscape_content(inputs)

def persona_creator(inputs):
    return generate_personas_content(inputs)

def brand_voice_definer(inputs):
    return generate_brand_voice_content(inputs)

def keyword_strategist(inputs):
    return generate_content_strategy(inputs)

def campaign_architect(inputs):
    return generate_campaign_structure(inputs)

def engagement_framework_builder(inputs):
    return generate_engagement_framework(inputs)

# Main AgentBuilder workflow
def main():
    inputs = get_example_inputs()  # Replace with your actual input source
    try:
        questionnaire = BrandQuestionnaire(**inputs)
    except Exception as e:
        print(f"Input validation failed: {e}")
        return

    builder = AgentBuilder(name="MarketingKitAgent")
    builder.set_objective("Generate a complete marketing kit for a brand.")

    builder.add_subagent(name="overview_writer", task="Generate overview content")
    builder.add_subagent(name="key_findings_researcher", task="Generate key findings content")
    builder.add_subagent(name="market_landscape_analyzer", task="Generate market landscape content")
    builder.add_subagent(name="persona_creator", task="Generate personas content")
    builder.add_subagent(name="brand_voice_definer", task="Generate brand voice content")
    builder.add_subagent(name="keyword_strategist", task="Generate content strategy")
    builder.add_subagent(name="campaign_architect", task="Generate campaign structure")
    builder.add_subagent(name="engagement_framework_builder", task="Generate engagement framework")

    builder.set_coordinator(workflow="sequential")
    agent = builder.build()
    result = agent.run(inputs=inputs)

    output_filename = f"marketing_kit_{questionnaire.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(result.output, f, ensure_ascii=False, indent=2)
    print(f"Marketing kit saved to {output_filename}")

if __name__ == "__main__":
    main()
