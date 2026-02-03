"""
AgentSpace - Design Agent

AI-powered agent that analyzes company branding and suggests
optimal visual design for marketing kits.

This agent:
- Analyzes company industry and brand personality
- Suggests color palettes
- Recommends typography
- Proposes layout styles
- Creates complete design specifications
"""

from typing import Dict, Any, Optional
from agentspace_design_styles import (
    ColorPalette, TypographyStyle, LayoutStyle, DesignSystem,
    extract_colors_from_brand
)


# ============================================================================
# DESIGN AGENT PROMPT
# ============================================================================

DESIGN_AGENT_SYSTEM_PROMPT = """You are an expert brand and visual designer who creates professional design systems for marketing materials.

Your role is to analyze a company's brand, industry, and positioning, then suggest optimal visual design choices including:
- Color palettes that reinforce brand personality
- Typography that matches industry standards
- Layout styles appropriate for the audience

Base your recommendations on:
1. Industry norms (healthcare = trust, tech = modern, finance = conservative)
2. Brand personality (bold vs subtle, creative vs professional)
3. Target audience (B2B corporate vs DTC consumer)
4. Competitive positioning (differentiation vs alignment)

Provide specific, actionable design recommendations."""


def get_design_recommendations_prompt(company_data: Dict[str, Any]) -> str:
    """Generate prompt for design recommendations."""
    
    prompt = f"""
Analyze this company and recommend visual design choices for their marketing kit.

COMPANY INFORMATION:
Company: {company_data.get('company_name')}
Industry: {company_data.get('industry')}
Target Audience: {company_data.get('target_audience_description')}
Brand Personality: {', '.join(company_data.get('brand_personality_adjectives', []))}
Tone: {company_data.get('tone_preferences')}
Competitors: {', '.join(company_data.get('main_competitors', []))}

Recommend:

1. **Color Strategy**
   - Primary color (describe tone: corporate blue, energetic orange, trustworthy navy, etc.)
   - Secondary/accent color
   - Overall color mood (conservative, bold, modern, classic)
   
2. **Typography Style**
   - Heading font family (serif, sans-serif, specific name if known)
   - Body font family
   - Overall typographic feel (modern, classic, tech, elegant)
   
3. **Layout Approach**
   - Spacing preference (compact, standard, spacious)
   - Visual elements (minimal, moderate decoration, bold graphics)
   - Professional level (conservative corporate, creative agency, startup casual)

4. **Overall Design Direction**
   - One sentence describing the complete visual identity
   - How it supports brand positioning

Be specific. If brand colors exist, use them. Match industry expectations while allowing differentiation.
"""
    
    return prompt


# ============================================================================
# DESIGN AGENT
# ============================================================================

class DesignAgent:
    """
    AI-powered design agent that creates visual specifications.
    """
    
    def __init__(self, llm=None):
        """
        Initialize design agent.
        
        Args:
            llm: LLM instance (ClaudeLLM or GPTLLM)
        """
        self.llm = llm
    
    def analyze_and_recommend(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze company and recommend design system.
        
        Args:
            company_data: Company information dictionary
            
        Returns:
            Design recommendations dictionary
        """
        
        print("🎨 Design Agent analyzing brand...")
        
        # Get design recommendations from AI
        prompt = get_design_recommendations_prompt(company_data)
        
        if self.llm:
            result = self.llm.generate(
                prompt=prompt,
                system=DESIGN_AGENT_SYSTEM_PROMPT,
                max_tokens=1500,
                temperature=0.7
            )
            
            if result["success"]:
                recommendations = result["content"]
                print(f"  ✓ Design recommendations generated")
                
                # Parse recommendations
                design_specs = self._parse_recommendations(recommendations, company_data)
                return design_specs
        
        # Fallback: Rule-based recommendations
        print("  ℹ Using rule-based design recommendations")
        return self._rule_based_recommendations(company_data)
    
    def _parse_recommendations(self, recommendations: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI recommendations into structured design specs."""
        
        # Extract key information from recommendations
        # This is a simplified parser - could be enhanced
        
        recs_lower = recommendations.lower()
        
        # Determine color mood
        if any(word in recs_lower for word in ['trust', 'corporate', 'professional', 'navy', 'blue']):
            color_palette = "healthcare_professional"
        elif any(word in recs_lower for word in ['bold', 'creative', 'orange', 'vibrant']):
            color_palette = "creative_bold"
        elif any(word in recs_lower for word in ['tech', 'modern', 'purple', 'innovation']):
            color_palette = "tech_modern"
        elif any(word in recs_lower for word in ['conservative', 'finance', 'traditional']):
            color_palette = "finance_trust"
        else:
            color_palette = "swift_innovation"
        
        # Determine typography
        if any(word in recs_lower for word in ['serif', 'classic', 'traditional', 'elegant']):
            typography = "professional_serif"
        elif any(word in recs_lower for word in ['sans', 'modern', 'clean', 'minimal']):
            typography = "tech_sans"
        elif any(word in recs_lower for word in ['mixed', 'sophisticated']):
            typography = "elegant_mixed"
        else:
            typography = "swift_modern"
        
        # Determine layout
        if any(word in recs_lower for word in ['spacious', 'airy', 'premium']):
            layout = "spacious"
        elif any(word in recs_lower for word in ['compact', 'efficient', 'dense']):
            layout = "compact"
        elif any(word in recs_lower for word in ['magazine', 'creative', 'editorial']):
            layout = "magazine"
        else:
            layout = "standard"
        
        return {
            "color_palette": color_palette,
            "typography": typography,
            "layout": layout,
            "ai_recommendations": recommendations,
            "recommended_system": self._map_to_design_system(color_palette, typography, layout, company_data)
        }
    
    def _rule_based_recommendations(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate design recommendations based on rules."""
        
        industry = company_data.get('industry', '').lower()
        personality = [p.lower() for p in company_data.get('brand_personality_adjectives', [])]
        
        # Industry-based defaults
        if any(word in industry for word in ['health', 'medical', 'hospital', 'care']):
            system_name = "healthcare_professional"
        elif any(word in industry for word in ['tech', 'software', 'saas', 'ai']):
            system_name = "tech_startup"
        elif any(word in industry for word in ['finance', 'bank', 'investment', 'insurance']):
            system_name = "finance_corporate"
        elif any(word in industry for word in ['creative', 'agency', 'design', 'marketing']):
            system_name = "creative_agency"
        elif any(word in personality for word in ['minimal', 'clean', 'simple']):
            system_name = "minimal_modern"
        else:
            system_name = "swift_innovation"
        
        from agentspace_design_styles import get_design_system
        system = get_design_system(system_name)
        
        return {
            "recommended_system": system_name,
            "design_system": system,
            "reasoning": f"Based on {industry} industry and {', '.join(personality[:2])} personality"
        }
    
    def _map_to_design_system(self, color_palette: str, typography: str, layout: str, company_data: Dict) -> str:
        """Map components to closest pre-built design system."""
        
        # Simple mapping logic
        if color_palette == "healthcare_professional" and typography == "professional_serif":
            return "healthcare_professional"
        elif color_palette == "tech_modern" and typography == "tech_sans":
            return "tech_startup"
        elif color_palette == "finance_trust":
            return "finance_corporate"
        elif color_palette == "creative_bold":
            return "creative_agency"
        else:
            return "swift_innovation"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_design_for_company(company_data: Dict[str, Any], llm=None) -> DesignSystem:
    """
    Get recommended design system for a company.
    
    Args:
        company_data: Company information
        llm: Optional LLM instance for AI recommendations
        
    Returns:
        Recommended DesignSystem
    """
    
    agent = DesignAgent(llm=llm)
    recommendations = agent.analyze_and_recommend(company_data)
    
    # Get the design system
    from agentspace_design_styles import get_design_system, create_custom_design_system
    
    if "recommended_system" in recommendations:
        system_name = recommendations["recommended_system"]
        design_system = get_design_system(system_name)
        
        # Print reasoning
        if "ai_recommendations" in recommendations:
            print("\n  Design Reasoning:")
            print(f"  {recommendations['ai_recommendations'][:200]}...")
        elif "reasoning" in recommendations:
            print(f"\n  Design Reasoning: {recommendations['reasoning']}")
        
        print(f"\n  ✓ Selected design system: {design_system.name}")
        
        return design_system
    
    # Fallback
    from agentspace_design_styles import DESIGN_SYSTEMS
    return DESIGN_SYSTEMS["swift_innovation"]


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DESIGN AGENT TEST")
    print("=" * 80)
    print()
    
    # Test data
    test_company = {
        "company_name": "HealthTech Solutions",
        "industry": "Healthcare Technology",
        "target_audience_description": "Hospital administrators and clinical directors",
        "brand_personality_adjectives": ["Professional", "Trustworthy", "Innovative"],
        "tone_preferences": "Professional and approachable",
        "main_competitors": ["Epic Systems", "Cerner"]
    }
    
    # Get design recommendation (without LLM - rule-based)
    agent = DesignAgent()
    recommendations = agent.analyze_and_recommend(test_company)
    
    print("Design Recommendations:")
    print(f"  System: {recommendations['recommended_system']}")
    print(f"  Reasoning: {recommendations['reasoning']}")
    print()
    
    # Get full design system
    from agentspace_design_styles import get_design_system, preview_design_system
    design = get_design_system(recommendations['recommended_system'])
    print(preview_design_system(design))
