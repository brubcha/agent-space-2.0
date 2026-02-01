"""
Marketing Kit DOCX Generator

Generates professional Word documents matching the Swift Innovation
marketing kit structure.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime


class MarketingKitDocxGenerator:
    """
    Generates marketing kit DOCX files with proper formatting.
    """
    
    def __init__(self):
        self.doc = Document()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure document styles."""
        # Set up normal style
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(11)
    
    def _add_title(self, text: str):
        """Add title heading."""
        heading = self.doc.add_heading(text, level=0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = heading.runs[0]
        run.font.size = Pt(24)
        run.font.bold = True
    
    def _add_heading(self, text: str, level: int = 1):
        """Add section heading."""
        heading = self.doc.add_heading(text, level=level)
        run = heading.runs[0]
        if level == 1:
            run.font.size = Pt(18)
        elif level == 2:
            run.font.size = Pt(14)
        run.font.bold = True
    
    def _add_paragraph(self, text: str, bold: bool = False):
        """Add paragraph."""
        p = self.doc.add_paragraph(text)
        if bold:
            p.runs[0].bold = True
        return p
    
    def _add_bullet_list(self, items: list):
        """Add bulleted list."""
        for item in items:
            self.doc.add_paragraph(item, style='List Bullet')
    
    def _add_numbered_list(self, items: list):
        """Add numbered list."""
        for item in items:
            self.doc.add_paragraph(item, style='List Number')
    
    def generate(self, company_name: str, agent_results: dict, save_path: str):
        """
        Generate the complete marketing kit DOCX.
        
        Args:
            company_name: Client company name
            agent_results: Results from agent execution
            save_path: Where to save the DOCX file
        """
        
        # Title Page
        self._add_title(f"Marketing Kit")
        self.doc.add_paragraph()
        
        title_para = self.doc.add_paragraph(company_name)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_para.runs[0].font.size = Pt(16)
        
        self.doc.add_paragraph()
        
        date_para = self.doc.add_paragraph(datetime.now().strftime("%B %Y"))
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_para.runs[0].font.size = Pt(12)
        date_para.runs[0].italic = True
        
        self.doc.add_page_break()
        
        # Table of Contents placeholder
        self._add_heading("Table of Contents", level=1)
        self._add_paragraph("1. Overview")
        self._add_paragraph("2. The Goal")
        self._add_paragraph("3. Key Findings")
        self._add_paragraph("4. Market Landscape")
        self._add_paragraph("5. Audience & Personas")
        self._add_paragraph("6. Brand Voice")
        self._add_paragraph("7. Content Strategy")
        self._add_paragraph("8. Social Strategy")
        self._add_paragraph("9. Campaign Structure")
        self._add_paragraph("10. Engagement Framework")
        
        self.doc.add_page_break()
        
        # Generate each section from agent results
        sections = {
            "overview_writer": ("Overview", self._generate_overview_section),
            "key_findings_researcher": ("Key Findings", self._generate_key_findings_section),
            "market_landscape_analyzer": ("Market Landscape", self._generate_market_landscape_section),
            "persona_creator": ("Audience & Personas", self._generate_personas_section),
            "brand_voice_definer": ("Brand Voice", self._generate_brand_voice_section),
            "keyword_strategist": ("Keyword Strategy", self._generate_keyword_section),
            "blog_strategist": ("Blog Strategy", self._generate_blog_section),
            "social_strategist": ("Social Strategy", self._generate_social_section),
            "campaign_architect": ("Campaign Structure", self._generate_campaign_section),
            "engagement_framework_builder": ("Engagement Framework", self._generate_engagement_section),
        }
        
        for agent_name, (section_title, generator_func) in sections.items():
            if agent_name in agent_results:
                self._add_heading(section_title, level=1)
                agent_output = agent_results[agent_name].get('output', '')
                generator_func(agent_output)
                self.doc.add_page_break()
        
        # Save the document
        self.doc.save(save_path)
        print(f"✓ Marketing kit saved to: {save_path}")
    
    def _generate_overview_section(self, content):
        """Generate overview section."""
        self._add_paragraph(str(content))
        self.doc.add_paragraph()
    
    def _generate_key_findings_section(self, content):
        """Generate key findings section."""
        self._add_paragraph(
            "Based on market research and competitive analysis, "
            "here are the key insights driving this marketing strategy:"
        )
        self.doc.add_paragraph()
        
        # If content is a string, add it as is
        # In a real implementation, this would be structured data
        self._add_paragraph(str(content))
    
    def _generate_market_landscape_section(self, content):
        """Generate market landscape section."""
        self._add_heading("Macro Trends & Growth", level=2)
        self._add_paragraph(str(content)[:500])  # Truncate for demo
        self.doc.add_paragraph()
    
    def _generate_personas_section(self, content):
        """Generate personas section."""
        self._add_paragraph(
            "The following personas represent the primary target audiences "
            "for marketing and sales activities:"
        )
        self.doc.add_paragraph()
        self._add_paragraph(str(content))
    
    def _generate_brand_voice_section(self, content):
        """Generate brand voice section."""
        self._add_heading("Brand Essence", level=2)
        self._add_paragraph(str(content)[:300])
        self.doc.add_paragraph()
        
        self._add_heading("Voice Examples", level=2)
        self._add_bullet_list([
            "Example 1: [Generated by agent]",
            "Example 2: [Generated by agent]",
            "Example 3: [Generated by agent]"
        ])
    
    def _generate_keyword_section(self, content):
        """Generate keyword strategy section."""
        self._add_paragraph("Strategic keyword targeting across multiple categories:")
        self.doc.add_paragraph()
        self._add_paragraph(str(content))
    
    def _generate_blog_section(self, content):
        """Generate blog strategy section."""
        self._add_paragraph(str(content))
    
    def _generate_social_section(self, content):
        """Generate social strategy section."""
        self._add_paragraph(str(content))
    
    def _generate_campaign_section(self, content):
        """Generate campaign structure section."""
        self._add_paragraph(str(content))
    
    def _generate_engagement_section(self, content):
        """Generate engagement framework section."""
        self._add_paragraph(str(content))


def generate_marketing_kit_docx(company_name: str, agent_results: dict, output_dir: str = "."):
    """
    Convenience function to generate marketing kit DOCX.
    
    Args:
        company_name: Client company name
        agent_results: Dictionary of agent execution results
        output_dir: Directory to save the file
    
    Returns:
        Path to generated DOCX file
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Marketing_Kit_{company_name.replace(' ', '_')}_{timestamp}.docx"
    save_path = f"{output_dir}/{filename}"
    
    generator = MarketingKitDocxGenerator()
    generator.generate(company_name, agent_results, save_path)
    
    return save_path


# Example usage
if __name__ == "__main__":
    # Demo with placeholder data
    example_results = {
        "overview_writer": {
            "status": "success",
            "output": "This marketing kit provides strategic foundation for all marketing activities..."
        },
        "key_findings_researcher": {
            "status": "success",
            "output": "1. Fragmentation is the core problem\n2. Independence is reshaping work..."
        }
    }
    
    docx_path = generate_marketing_kit_docx(
        company_name="Example Company",
        agent_results=example_results
    )
    
    print(f"Demo DOCX generated: {docx_path}")
