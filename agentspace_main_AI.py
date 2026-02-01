"""
AgentSpace - AI-Powered Marketing Kit Generator

This is the COMPLETE, PRODUCTION-READY version that combines:
- Intelligence Layer (website scraping + file reading)
- LLM Integration (Claude/GPT)
- Professional prompts
- Real AI-generated content

This replaces agentspace-main.py
"""

from agentspace_inputs import BrandQuestionnaire, prepare_inputs_with_defaults
from agentspace_llm import LLMFactory
from agentspace_prompts import get_prompt_for_section_swift_complete as get_prompt_for_section
import json
from datetime import datetime
import os


def run_marketing_kit_generation_AI(inputs: dict, output_format: str = "json", provider: str = "claude"):
    # Import sanitizer from webapp (or redefine here if needed)
    try:
        from agentspace_webapp import sanitize_unicode
    except ImportError:
        def sanitize_unicode(obj):
            if isinstance(obj, str):
                return obj.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            elif isinstance(obj, dict):
                return {sanitize_unicode(k): sanitize_unicode(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_unicode(i) for i in obj]
            elif isinstance(obj, tuple):
                return tuple(sanitize_unicode(i) for i in obj)
            elif isinstance(obj, set):
                return {sanitize_unicode(i) for i in obj}
            elif obj is None or isinstance(obj, (int, float, bool)):
                return obj
            else:
                return sanitize_unicode(str(obj))
    """
    Generate marketing kit using AI.
    
    Args:
        inputs: Company data (enriched from scraping/files)
        output_format: "json" or "docx"
        provider: "claude" or "gpt"
    Returns:
        Result object with AI-generated content
    """
    
    print("=" * 80)
    print("AGENTSPACE - AI-POWERED MARKETING KIT GENERATOR")
    print("=" * 80)
    print()
    
    # Step 1: Validate inputs
    print("[1mValidating inputs...[0m")
    try:
        # Ensure all required fields have defaults
        validated_inputs = prepare_inputs_with_defaults(inputs)
        questionnaire = BrandQuestionnaire(**validated_inputs)
        print(f"\u2713 Inputs validated for: {questionnaire.company_name}")
    except Exception as e:
        print(f"\u2717 Validation failed: {e}")
        return None
    
    print()
    print(f"\u001b[1mCompany: {questionnaire.company_name}\u001b[0m")
    print(f"\u001b[1mIndustry: {questionnaire.industry}\u001b[0m")
    print(f"\u001b[1mGoal: {questionnaire.primary_business_goal}\u001b[0m")
    print()
    
    # Step 2: Initialize LLM
    print(f"\u001b[1mInitializing {provider.upper()} AI...\u001b[0m")
    try:
        llm = LLMFactory.create(provider=provider)
        print(f"\u2713 {provider.upper()} ready")
    except Exception as e:
        print(f"\u2717 Failed to initialize LLM: {e}")
        print("   Check your API key in .env file")
        return None
    
    print()
    
    # Step 3: Generate each section with AI
    print("\u2728 Generating marketing kit sections with AI...")
    print()
    
    sections = {}
    section_names = [
        "overview_writer",
        "key_findings_researcher",
        "market_landscape_analyzer",
        "persona_creator",
        "brand_voice_definer",
        "keyword_strategist",
        "social_strategist",
        "campaign_architect",
        "engagement_framework_builder",
    ]
    
    total_cost = 0.0
    total_tokens = 0
    
    for i, section_name in enumerate(section_names, 1):
        print(f"  [{i}/9] Generating {section_name.replace('_', ' ').title()}...")
        
        try:
            # Get prompt for this section
            system_prompt, user_prompt = get_prompt_for_section(
                section_name,
                validated_inputs
            )
            
            # Generate with AI
            result = llm.generate(
                prompt=user_prompt,
                system=system_prompt,
                max_tokens=4000,
                temperature=0.7
            )
            
            if result["success"]:
                sections[section_name] = {
                    "status": "success",
                    "output": result["content"],
                    "tokens": result["tokens"]["total"],
                    "cost": result["cost"]
                }
                
                total_tokens += result["tokens"]["total"]
                total_cost += result["cost"]
                
                print(f"        \u2713 Generated ({result['tokens']['output']} tokens, ${result['cost']:.4f})")
            else:
                sections[section_name] = {
                    "status": "failed",
                    "output": f"[Error: {result.get('error', 'Unknown error')}]",
                    "error": result.get("error")
                }
                print(f"        \u2717 Failed: {result.get('error')}")
        
        except Exception as e:
            sections[section_name] = {
                "status": "failed",
                "output": f"[Exception: {str(e)}]",
                "error": str(e)
            }
            print(f"        \u2717 Exception: {str(e)}")
    
    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print()
    print(f"\u001b[1mTotal Tokens: {total_tokens:,}\u001b[0m")
    print(f"\u001b[1mTotal Cost: ${total_cost:.4f}\u001b[0m")
    print(f"\u001b[1mProvider: {provider.upper()}\u001b[0m")
    print()
    
    # Step 4: Create result object
    class Result:
        def __init__(self, sections, metadata):
            self.success = True
            self.output = sections
            self.metadata = metadata
            self.errors = []
        
        def to_dict(self):
            return {
                "success": self.success,
                "output": self.output,
                "metadata": self.metadata,
                "errors": self.errors
            }
    
    result = Result(
        sections=sections,
        metadata={
            "company_name": questionnaire.company_name,
            "generated_at": datetime.now().isoformat(),
            "provider": provider,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "sections_generated": len(sections),
            "sections_successful": sum(1 for s in sections.values() if s["status"] == "success")
        }
    )
    
    # Step 5: Save JSON
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"marketing_kit_{questionnaire.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
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
    print(f"\U0001F4BE Marketing kit saved to: {output_filename}")
    print()
    return result
    print()
    
    # Example inputs
    from agentspace_inputs import get_example_inputs
    inputs = get_example_inputs()
    
    # Generate
    result = run_marketing_kit_generation_AI(inputs, provider=provider)
    
    if result and result.success:
        print()
        print("\uD83C\uDF89 SUCCESS!")
        print()
        print("Your AI-generated marketing kit is ready!")
        print()
        print("Next steps:")
        print("1. Review the JSON file")
        print("2. Generate DOCX with agentspace-docx-generator.py")
        print("3. Deliver to your client!")
        print()


if __name__ == "__main__":
    main()

