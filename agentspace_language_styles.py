"""
AgentSpace - Language Style System

Control the WRITING STYLE, TONE, and VOICE of your marketing kits.

This is separate from visual design - it controls HOW WORDS ARE WRITTEN:
- Sentence structure and length
- Active vs passive voice
- Power words and vocabulary
- Tone and pacing
- Distinctive voice patterns

Based on analysis of Swift Innovation's writing style.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import re


# ============================================================================
# SWIFT INNOVATION LANGUAGE ANALYSIS
# ============================================================================

SWIFT_LANGUAGE_PROFILE = {
    "sentence_length": {
        "average": 14.3,
        "short_percent": 31,      # <10 words
        "medium_percent": 56,     # 10-20 words
        "long_percent": 13        # >20 words
    },
    
    "voice": {
        "active_percent": 97,     # Highly active voice
        "passive_percent": 3,     # Minimal passive
        "declarative": "high"     # Lots of statements vs questions
    },
    
    "power_words": [
        "momentum", "clarity", "fragmentation", "embedded", "aligned",
        "execution", "outcomes", "strategic", "connected", "infrastructure"
    ],
    
    "signature_patterns": [
        "X sells 'Y'",                    # Competitor differentiation
        "without X",                      # Positioning (without fragmentation)
        "Not X. Y.",                      # Contrast (Not hours. Outcomes.)
        "Verb without modifier"           # Momentum without micromanagement
    ],
    
    "punctuation": {
        "colons": "frequent",             # 79 uses
        "em_dashes": "rare",              # 0 uses
        "quotes": "selective"             # 6 uses for emphasis
    },
    
    "distinctive_voice": [
        "We measure outcomes, not hours.",
        "Independence is strongest when it moves together.",
        "Momentum without micromanagement.",
        "Strategy is nothing without execution."
    ]
}


# ============================================================================
# LANGUAGE STYLE SYSTEM
# ============================================================================

@dataclass
class LanguageStyle:
    """
    Complete language/writing style specification.
    
    Controls HOW content is written, not just WHAT is written.
    """
    
    name: str
    description: str
    
    # SENTENCE STRUCTURE
    avg_sentence_length: int          # Target average words per sentence
    short_sentence_ratio: float       # % of sentences <10 words
    use_fragments: bool               # Allow sentence fragments for impact
    
    # VOICE & TONE
    active_voice_target: float        # % active voice (vs passive)
    declarative_ratio: float          # % statements vs questions
    tone_adjectives: List[str]        # Confident, Professional, Bold, etc.
    
    # VOCABULARY
    power_words: List[str]            # Key vocabulary to emphasize
    avoid_words: List[str]            # Words to avoid (jargon, clichés)
    vocabulary_level: str             # "accessible", "professional", "technical"
    
    # SIGNATURE PATTERNS
    signature_phrases: List[str]      # Distinctive patterns (e.g., "X sells Y")
    sentence_starters: List[str]      # Preferred opening words
    emphasis_pattern: str             # How to create emphasis
    
    # PACING & RHYTHM
    rhythm: str                       # "punchy", "flowing", "methodical"
    paragraph_length: str             # "short", "medium", "long"
    use_repetition: bool              # Strategic repetition for emphasis
    
    # PUNCTUATION STYLE
    colon_usage: str                  # "frequent", "moderate", "rare"
    dash_usage: str                   # "frequent", "moderate", "rare"
    quote_usage: str                  # "frequent", "selective", "rare"


# ============================================================================
# PRE-BUILT LANGUAGE STYLES
# ============================================================================

LANGUAGE_STYLES = {
    "swift_innovation": LanguageStyle(
        name="Swift Innovation Voice",
        description="Clear, declarative statements with strategic power words. Active voice. Punchy rhythm.",
        
        # Sentence structure (14.3 word average)
        avg_sentence_length=14,
        short_sentence_ratio=0.30,     # 30% short sentences
        use_fragments=True,             # "Momentum without micromanagement."
        
        # Voice (97% active)
        active_voice_target=0.95,
        declarative_ratio=0.90,         # Statements, not questions
        tone_adjectives=["Confident", "Precise", "Strategic", "Modern"],
        
        # Vocabulary
        power_words=["momentum", "clarity", "fragmentation", "embedded", "aligned",
                    "execution", "outcomes", "strategic", "connected", "infrastructure"],
        avoid_words=["utilize", "leverage", "synergy", "paradigm", "solution"],
        vocabulary_level="professional",
        
        # Patterns
        signature_phrases=[
            "X sells 'Y'",
            "without [noun]",
            "Not X. Y.",
            "[Noun] without [modifier]"
        ],
        sentence_starters=["Swift", "Most", "Businesses", "Strategy", "Execution"],
        emphasis_pattern="contrast",    # A not B. C.
        
        # Pacing
        rhythm="punchy",
        paragraph_length="short",       # 2-4 sentences
        use_repetition=True,            # "Growth without fragmentation"
        
        # Punctuation
        colon_usage="frequent",         # 79 uses
        dash_usage="rare",
        quote_usage="selective"
    ),
    
    "professional_corporate": LanguageStyle(
        name="Professional Corporate",
        description="Formal, authoritative tone. Longer sentences. Traditional business language.",
        
        avg_sentence_length=18,
        short_sentence_ratio=0.20,
        use_fragments=False,
        
        active_voice_target=0.80,
        declarative_ratio=0.85,
        tone_adjectives=["Professional", "Authoritative", "Thorough", "Trustworthy"],
        
        power_words=["excellence", "integrity", "commitment", "innovation", "expertise",
                    "performance", "quality", "value", "partnership", "solutions"],
        avoid_words=["gonna", "wanna", "cool", "awesome", "game-changer"],
        vocabulary_level="professional",
        
        signature_phrases=[
            "We are committed to",
            "Our expertise in",
            "Through our comprehensive"
        ],
        sentence_starters=["Our", "We", "The company", "Through", "With"],
        emphasis_pattern="elaboration",
        
        rhythm="flowing",
        paragraph_length="medium",
        use_repetition=False,
        
        colon_usage="moderate",
        dash_usage="moderate",
        quote_usage="rare"
    ),
    
    "tech_modern": LanguageStyle(
        name="Tech Modern",
        description="Direct, fast-paced. Short sentences. Modern tech vocabulary. Confident.",
        
        avg_sentence_length=12,
        short_sentence_ratio=0.40,      # 40% short
        use_fragments=True,
        
        active_voice_target=0.95,
        declarative_ratio=0.85,
        tone_adjectives=["Direct", "Modern", "Efficient", "Bold"],
        
        power_words=["transform", "innovate", "scale", "automate", "accelerate",
                    "optimize", "disrupt", "platform", "ecosystem", "intelligence"],
        avoid_words=["traditional", "legacy", "manual", "slow", "complex"],
        vocabulary_level="professional",
        
        signature_phrases=[
            "Built for",
            "Ship faster",
            "Zero [pain point]"
        ],
        sentence_starters=["Build", "Ship", "Scale", "Transform", "Automate"],
        emphasis_pattern="repetition",
        
        rhythm="punchy",
        paragraph_length="short",
        use_repetition=True,
        
        colon_usage="frequent",
        dash_usage="moderate",
        quote_usage="frequent"
    ),
    
    "creative_bold": LanguageStyle(
        name="Creative Bold",
        description="Vivid, energetic language. Varied sentence length. Creative wordplay. Personality.",
        
        avg_sentence_length=13,
        short_sentence_ratio=0.35,
        use_fragments=True,
        
        active_voice_target=0.90,
        declarative_ratio=0.75,         # More variety
        tone_adjectives=["Bold", "Creative", "Energetic", "Distinctive"],
        
        power_words=["unleash", "ignite", "breakthrough", "revolutionary", "vibrant",
                    "bold", "fearless", "transform", "elevate", "spectacular"],
        avoid_words=["boring", "standard", "typical", "average", "normal"],
        vocabulary_level="accessible",
        
        signature_phrases=[
            "Imagine [scenario]",
            "What if [question]",
            "Here's the thing:"
        ],
        sentence_starters=["Imagine", "Picture", "Think", "Here's", "What if"],
        emphasis_pattern="surprise",
        
        rhythm="varied",
        paragraph_length="varied",
        use_repetition=True,
        
        colon_usage="frequent",
        dash_usage="frequent",
        quote_usage="frequent"
    ),
    
    "consultative_expert": LanguageStyle(
        name="Consultative Expert",
        description="Insightful, analytical. Data-driven. Measured pace. Expert credibility.",
        
        avg_sentence_length=16,
        short_sentence_ratio=0.25,
        use_fragments=False,
        
        active_voice_target=0.85,
        declarative_ratio=0.80,
        tone_adjectives=["Insightful", "Analytical", "Credible", "Measured"],
        
        power_words=["insight", "analysis", "strategic", "framework", "methodology",
                    "optimize", "benchmark", "assessment", "roadmap", "metrics"],
        avoid_words=["maybe", "probably", "hope", "try", "wish"],
        vocabulary_level="professional",
        
        signature_phrases=[
            "Our analysis shows",
            "Based on research",
            "The data indicates"
        ],
        sentence_starters=["Research", "Analysis", "Data", "Studies", "Evidence"],
        emphasis_pattern="evidence",
        
        rhythm="methodical",
        paragraph_length="medium",
        use_repetition=False,
        
        colon_usage="frequent",
        dash_usage="rare",
        quote_usage="moderate"
    ),
    
    "accessible_friendly": LanguageStyle(
        name="Accessible Friendly",
        description="Conversational, warm. Simple language. Approachable. Clear explanations.",
        
        avg_sentence_length=13,
        short_sentence_ratio=0.35,
        use_fragments=True,
        
        active_voice_target=0.95,
        declarative_ratio=0.70,         # More questions for engagement
        tone_adjectives=["Friendly", "Clear", "Approachable", "Helpful"],
        
        power_words=["simple", "easy", "clear", "helpful", "quick",
                    "straightforward", "practical", "everyday", "real", "useful"],
        avoid_words=["utilize", "facilitate", "implement", "paradigm", "synergize"],
        vocabulary_level="accessible",
        
        signature_phrases=[
            "Here's how",
            "Think of it like",
            "In simple terms"
        ],
        sentence_starters=["Let's", "Here's", "Think", "Imagine", "Simply put"],
        emphasis_pattern="clarity",
        
        rhythm="conversational",
        paragraph_length="short",
        use_repetition=True,
        
        colon_usage="moderate",
        dash_usage="frequent",
        quote_usage="frequent"
    )
}


# ============================================================================
# LANGUAGE STYLE PROMPTS
# ============================================================================

def get_language_style_instructions(style: LanguageStyle) -> str:
    """
    Generate writing instructions based on language style.
    
    Returns prompt instructions for AI to follow.
    """
    
    instructions = f"""
LANGUAGE STYLE: {style.name}
{style.description}

WRITING RULES:

**Sentence Structure:**
- Target average: {style.avg_sentence_length} words per sentence
- Use {int(style.short_sentence_ratio * 100)}% short sentences (<10 words) for impact
- Sentence fragments: {'Allowed for emphasis' if style.use_fragments else 'Avoid'}

**Voice & Tone:**
- Active voice: {int(style.active_voice_target * 100)}% of sentences
- Minimize passive voice
- Tone: {', '.join(style.tone_adjectives)}
- Use {int(style.declarative_ratio * 100)}% declarative statements

**Vocabulary:**
- Power words to use: {', '.join(style.power_words[:8])}
- Words to avoid: {', '.join(style.avoid_words[:5])}
- Level: {style.vocabulary_level.title()}

**Signature Patterns:**
Use these distinctive patterns when appropriate:
{chr(10).join(['• ' + p for p in style.signature_phrases[:3]])}

**Pacing:**
- Rhythm: {style.rhythm.title()}
- Paragraph length: {style.paragraph_length.title()} (2-4 sentences for short, 4-6 for medium)
- Repetition: {'Use strategically for emphasis' if style.use_repetition else 'Avoid'}

**Punctuation:**
- Colons: {style.colon_usage.title()} use
- Em dashes: {style.dash_usage.title()} use
- Quotes: {style.quote_usage.title()} use for emphasis

CRITICAL: Write in THIS style consistently throughout all sections.
"""
    
    return instructions


def get_language_style_examples(style_name: str = "swift_innovation") -> List[str]:
    """Get example sentences in a given language style."""
    
    examples = {
        "swift_innovation": [
            "Most businesses piece together agencies, consultants, and disconnected tools.",
            "Swift was designed to remove fragmentation.",
            "Strategy without delivery stalls growth.",
            "We measure outcomes, not hours.",
            "Momentum without micromanagement."
        ],
        
        "professional_corporate": [
            "Our organization is committed to delivering exceptional value to our clients.",
            "Through comprehensive analysis and strategic planning, we enable sustainable growth.",
            "We bring together deep industry expertise with innovative solutions.",
            "Our approach is grounded in proven methodologies and best practices."
        ],
        
        "tech_modern": [
            "Ship faster. Scale infinitely.",
            "Built for teams that move fast.",
            "Zero complexity. Maximum impact.",
            "Transform your workflow in minutes.",
            "Automate everything. Focus on what matters."
        ],
        
        "creative_bold": [
            "Imagine a world where creativity flows effortlessly.",
            "What if your brand could speak without saying a word?",
            "Here's the thing: Bold ideas need fearless execution.",
            "We don't just think outside the box. We reimagine it entirely."
        ],
        
        "consultative_expert": [
            "Our analysis of market trends indicates three key opportunities.",
            "Research shows that integrated approaches deliver 40% better outcomes.",
            "Based on benchmark data across 500 companies, we recommend a phased approach.",
            "The strategic framework combines proven methodologies with emerging best practices."
        ],
        
        "accessible_friendly": [
            "Here's how it works in simple terms.",
            "Think of it like building with blocks - one piece at a time.",
            "We make it easy so you can focus on growing your business.",
            "Let's break this down into simple steps you can start today."
        ]
    }
    
    return examples.get(style_name, examples["swift_innovation"])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_language_style(name: str) -> LanguageStyle:
    """Get a language style by name."""
    return LANGUAGE_STYLES.get(name, LANGUAGE_STYLES["swift_innovation"])


def list_language_styles() -> List[str]:
    """List all available language styles."""
    return list(LANGUAGE_STYLES.keys())


def analyze_text_style(text: str) -> Dict[str, any]:
    """
    Analyze a text sample to determine its language style.
    
    Args:
        text: Sample text to analyze
        
    Returns:
        Dictionary with style metrics
    """
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 2]
    
    # Calculate metrics
    word_counts = [len(s.split()) for s in sentences]
    avg_length = sum(word_counts) / len(word_counts) if word_counts else 0
    short_pct = len([w for w in word_counts if w < 10]) / len(word_counts) if word_counts else 0
    
    # Check for passive voice
    passive_count = len(re.findall(r'\b(is|are|was|were|been)\s+\w+ed\b', text))
    passive_pct = passive_count / len(sentences) if sentences else 0
    
    return {
        "avg_sentence_length": avg_length,
        "short_sentence_ratio": short_pct,
        "passive_ratio": passive_pct,
        "total_sentences": len(sentences),
        "total_words": sum(word_counts)
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("AGENTSPACE LANGUAGE STYLES")
    print("=" * 80)
    print()
    
    print("Available Language Styles:")
    for i, name in enumerate(list_language_styles(), 1):
        style = get_language_style(name)
        print(f"{i}. {style.name}")
        print(f"   {style.description}")
        print(f"   Tone: {', '.join(style.tone_adjectives[:3])}")
        print(f"   Avg sentence: {style.avg_sentence_length} words")
        print()
    
    print("=" * 80)
    print("\nEXAMPLE: Swift Innovation Language Style")
    print("=" * 80)
    
    swift = get_language_style("swift_innovation")
    instructions = get_language_style_instructions(swift)
    print(instructions)
    
    print("\nExample Sentences in Swift Style:")
    for example in get_language_style_examples("swift_innovation"):
        print(f"  • {example}")
