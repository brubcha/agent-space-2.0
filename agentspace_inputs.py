"""
Marketing Kit Input Schema - FIXED for Intelligent System

This version makes most fields optional so scraped data can fill them.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class BrandQuestionnaire(BaseModel):
    """
    Input schema compatible with web scraping and file analysis.
    
    Most fields are optional - they'll be filled by:
    1. Web form (if user provides)
    2. Website scraping (automatic)
    3. File analysis (automatic)
    4. Default values (fallback)
    """
    
    # === REQUIRED FIELDS (Absolute minimum) ===
    company_name: str = Field(..., description="Company name")
    
    # === OPTIONAL FIELDS (Can be enriched automatically) ===
    
    # Basic Info
    industry: Optional[str] = Field(None, description="Primary industry")
    company_size: Optional[str] = Field(None, description="Company size range")
    website: Optional[str] = Field(None, description="Company website URL")
    
    # Brand Story
    company_overview: Optional[str] = Field(None, description="Brief company overview")
    mission_statement: Optional[str] = Field(None, description="Mission statement")
    core_values: Optional[List[str]] = Field(default_factory=list, description="Core company values")
    unique_selling_proposition: Optional[str] = Field(None, description="What makes you different?")
    
    # Target Audience
    target_audience_description: Optional[str] = Field(None, description="Who are your ideal customers?")
    customer_pain_points: Optional[List[str]] = Field(default_factory=list, description="Problems you solve")
    customer_goals: Optional[List[str]] = Field(default_factory=list, description="What customers want to achieve")
    
    # Competitive Landscape
    main_competitors: Optional[List[str]] = Field(default_factory=list, description="Main competitors")
    competitive_advantages: Optional[List[str]] = Field(default_factory=list, description="Your key advantages")
    market_position: Optional[str] = Field(None, description="How you position yourself")
    
    # Brand Personality
    brand_personality_adjectives: Optional[List[str]] = Field(
        default_factory=lambda: ["Professional", "Reliable", "Innovative"],
        description="Adjectives describing your brand"
    )
    tone_preferences: Optional[str] = Field("Professional and approachable", description="Desired tone")
    voice_guidelines: Optional[str] = Field(None, description="Voice guidelines or examples")
    
    # Visual Identity
    primary_colors: Optional[List[str]] = Field(default_factory=list, description="Brand colors (hex codes)")
    logo_description: Optional[str] = Field(None, description="Logo description")
    
    # Business Model
    products_services: Optional[List[str]] = Field(default_factory=list, description="Main products/services")
    business_model: Optional[str] = Field("B2B", description="Business model")
    key_features: Optional[List[str]] = Field(default_factory=list, description="Top features/capabilities")
    
    # Goals & Strategy
    primary_business_goal: Optional[str] = Field("Growth and market leadership", description="Primary goal")
    target_markets: Optional[List[str]] = Field(default_factory=list, description="Target markets")
    growth_stage: Optional[str] = Field("Growth", description="Business stage")
    
    # Content & Proof
    existing_tagline: Optional[str] = Field(None, description="Current tagline")
    key_messages: Optional[List[str]] = Field(default_factory=list, description="Key messages")
    proof_points: Optional[List[str]] = Field(default_factory=list, description="Stats, case studies, wins")
    
    # Channels
    primary_channels: Optional[List[str]] = Field(
        default_factory=lambda: ["Website", "Social Media"],
        description="Marketing channels"
    )
    content_preferences: Optional[str] = Field(None, description="Content preferences")
    
    # Additional
    brand_inspirations: Optional[List[str]] = Field(default_factory=list, description="Brands you admire")
    avoid_list: Optional[List[str]] = Field(default_factory=list, description="Things to avoid")
    special_requirements: Optional[str] = Field(None, description="Other requirements")
    
    # Internal (from file analysis)
    file_content: Optional[str] = Field(None, description="Raw file content for reference")


class MarketingKitInputs(BaseModel):
    """
    Complete inputs for marketing kit generation.
    """
    questionnaire: BrandQuestionnaire
    logo_file: Optional[str] = Field(None, description="Path to logo file")
    brand_assets: Optional[List[str]] = Field(None, description="Paths to brand assets")
    additional_documents: Optional[List[str]] = Field(None, description="Supporting documents")


def get_example_inputs() -> dict:
    """
    Example inputs - now with more optional fields.
    """
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
    example = {
        "company_name": "Example Corp",
        "industry": "Technology Services",
        "company_size": "$5M-$15M",
        "website": "https://example.com",
        "company_overview": "We provide embedded technology teams for mid-market businesses.",
        "mission_statement": "To help businesses grow through integrated execution.",
        "core_values": ["Quality", "Innovation", "Customer Focus"],
        "unique_selling_proposition": "All disciplines under one roof instead of multiple vendors",
        "target_audience_description": "Mid-market B2B companies ($5M-$50M)",
        "customer_pain_points": ["Managing multiple vendors", "Slow execution"],
        "customer_goals": ["Scale efficiently", "Faster time to market"],
        "main_competitors": ["Traditional agencies", "Consulting firms"],
        "competitive_advantages": ["Integrated model", "All disciplines unified"],
        "market_position": "The integrated alternative to fragmented vendors",
        "products_services": ["Marketing Teams", "Product Development", "CRM Platform"],
        "primary_business_goal": "Become the go-to partner for mid-market B2B companies",
    }
    return sanitize_unicode(example)


# Helper function to ensure all required fields have defaults
def prepare_inputs_with_defaults(inputs: dict) -> dict:
    """
    Take any dict of inputs and fill in missing required fields with defaults.
    This ensures validation always passes.
    """
    defaults = {
        # Provide sensible defaults for everything
        "industry": "To be determined",
        "company_size": "To be determined",
        "company_overview": "",
        "mission_statement": "To be defined",
        "core_values": ["Quality", "Innovation", "Customer Focus"],
        "unique_selling_proposition": "To be defined",
        "target_audience_description": "To be defined",
        "customer_pain_points": ["To be researched"],
        "customer_goals": ["To be researched"],
        "main_competitors": [],
        "competitive_advantages": ["To be defined"],
        "market_position": "To be defined",
        "brand_personality_adjectives": ["Professional", "Reliable", "Innovative"],
        "tone_preferences": "Professional and approachable",
        "products_services": ["To be defined"],
        "business_model": "B2B",
        "key_features": [],
        "primary_business_goal": "Growth and market leadership",
        "target_markets": ["To be researched"],
        "growth_stage": "Growth",
        "proof_points": [],
        "primary_channels": ["Website", "Social Media"],
    }
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
    result = {**defaults, **inputs}
    return sanitize_unicode(result)


if __name__ == "__main__":
    # Test validation with minimal data
    minimal = {
        "company_name": "Test Company"
    }
    
    # This should now work!
    prepared = prepare_inputs_with_defaults(minimal)
    questionnaire = BrandQuestionnaire(**prepared)
    
    print("✓ Validation passed with minimal data!")
    print(f"  Company: {questionnaire.company_name}")
    print(f"  USP: {questionnaire.unique_selling_proposition}")
