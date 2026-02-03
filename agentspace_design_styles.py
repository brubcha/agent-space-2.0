
"""
AgentSpace - Visual Design Styles System

Control the visual appearance of your marketing kits with:
- Pre-built design templates
- Brand color schemes
- Typography systems
- Layout styles
- Visual hierarchies

Use this to match client brand guidelines or create new visual identities.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from docx.shared import RGBColor, Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ============================================================================
# COLOR SYSTEM
# ============================================================================

@dataclass
class ColorPalette:
	"""Brand color palette."""
	name: str
	primary: Tuple[int, int, int]      # Main brand color
	secondary: Tuple[int, int, int]    # Accent color
	dark: Tuple[int, int, int]         # Headings, emphasis
	light: Tuple[int, int, int]        # Backgrounds, subtle elements
	text: Tuple[int, int, int]         # Body text
	muted: Tuple[int, int, int]        # Secondary text, captions


# Pre-built color palettes
DESIGN_PALETTES = {
	"swift_innovation": ColorPalette(
		name="Swift Innovation",
		primary=(41, 128, 185),      # Blue
		secondary=(231, 76, 60),     # Red accent
		dark=(44, 62, 80),           # Dark blue-gray
		light=(236, 240, 241),       # Light gray
		text=(52, 73, 94),           # Dark gray text
		muted=(149, 165, 166)        # Muted gray
	),
	"healthcare_professional": ColorPalette(
		name="Healthcare Professional",
		primary=(46, 134, 193),      # Medical blue
		secondary=(26, 188, 156),    # Teal accent
		dark=(23, 32, 42),           # Nearly black
		light=(250, 250, 250),       # Off-white
		text=(44, 62, 80),           # Dark blue-gray
		muted=(127, 140, 141)        # Gray
	),
	"tech_modern": ColorPalette(
		name="Tech Modern",
		primary=(142, 68, 173),      # Purple
		secondary=(52, 152, 219),    # Blue
		dark=(33, 47, 61),           # Dark slate
		light=(245, 246, 250),       # Light blue-gray
		text=(44, 62, 80),           # Dark gray
		muted=(149, 165, 166)        # Gray
	),
	"finance_trust": ColorPalette(
		name="Finance & Trust",
		primary=(21, 67, 96),        # Navy blue
		dark=(11, 37, 56),           # Darker navy
		secondary=(192, 57, 43),     # Deep red accent
		light=(247, 249, 250),       # Very light gray
		text=(33, 47, 61),           # Dark slate
		muted=(115, 133, 145)        # Blue-gray
	),
	"creative_bold": ColorPalette(
		name="Creative Bold",
		primary=(230, 126, 34),      # Orange
		secondary=(155, 89, 182),    # Purple
		dark=(41, 49, 51),           # Charcoal
		light=(254, 249, 231),       # Warm off-white
		text=(52, 73, 94),           # Dark gray
		muted=(189, 195, 199)        # Light gray
	),
	"minimal_elegant": ColorPalette(
		name="Minimal Elegant",
		primary=(52, 73, 94),        # Dark slate
		secondary=(189, 195, 199),   # Light gray accent
		dark=(33, 47, 61),           # Darker slate
		light=(255, 255, 255),       # Pure white
		text=(44, 62, 80),           # Dark blue-gray
		muted=(149, 165, 166)        # Medium gray
	)
}

# ============================================================================
# TYPOGRAPHY SYSTEM
# ============================================================================

@dataclass
class TypographyStyle:
	"""Typography system for the marketing kit."""
	name: str
	heading_font: str          # Font for headings
	body_font: str             # Font for body text
	h1_size: int               # Main title
	h2_size: int               # Section headers
	h3_size: int               # Sub-sections
	body_size: int             # Normal text
	caption_size: int          # Small text, captions
	line_spacing: float        # Line height multiplier
	paragraph_spacing: int     # Points between paragraphs

TYPOGRAPHY_STYLES = {
	"swift_modern": TypographyStyle(
		name="Swift Modern",
		heading_font="Calibri",
		body_font="Calibri",
		h1_size=28,
		h2_size=18,
		h3_size=14,
		body_size=11,
		caption_size=9,
		line_spacing=1.15,
		paragraph_spacing=6
	),
	"professional_serif": TypographyStyle(
		name="Professional Serif",
		heading_font="Georgia",
		body_font="Georgia",
		h1_size=26,
		h2_size=16,
		h3_size=13,
		body_size=11,
		caption_size=9,
		line_spacing=1.3,
		paragraph_spacing=8
	),
	"tech_sans": TypographyStyle(
		name="Tech Sans-Serif",
		heading_font="Arial",
		body_font="Arial",
		h1_size=30,
		h2_size=20,
		h3_size=15,
		body_size=11,
		caption_size=9,
		line_spacing=1.2,
		paragraph_spacing=6
	),
	"elegant_mixed": TypographyStyle(
		name="Elegant Mixed",
		heading_font="Georgia",
		body_font="Calibri",
		h1_size=28,
		h2_size=18,
		h3_size=14,
		body_size=11,
		caption_size=9,
		line_spacing=1.25,
		paragraph_spacing=8
	)
}

# ============================================================================
# LAYOUT SYSTEM
# ============================================================================

@dataclass
class LayoutStyle:
	"""Page layout and spacing system."""
	name: str
	top_margin: float
	bottom_margin: float
	left_margin: float
	right_margin: float
	section_spacing_before: int
	section_spacing_after: int
	use_section_dividers: bool
	use_page_borders: bool
	use_header_footer: bool

LAYOUT_STYLES = {
	"standard": LayoutStyle(
		name="Standard Professional",
		top_margin=1.0,
		bottom_margin=1.0,
		left_margin=1.0,
		right_margin=1.0,
		section_spacing_before=12,
		section_spacing_after=6,
		use_section_dividers=False,
		use_page_borders=False,
		use_header_footer=True
	),
	"compact": LayoutStyle(
		name="Compact",
		top_margin=0.75,
		bottom_margin=0.75,
		left_margin=0.75,
		right_margin=0.75,
		section_spacing_before=8,
		section_spacing_after=4,
		use_section_dividers=True,
		use_page_borders=False,
		use_header_footer=False
	),
	"spacious": LayoutStyle(
		name="Spacious & Airy",
		top_margin=1.5,
		bottom_margin=1.5,
		left_margin=1.25,
		right_margin=1.25,
		section_spacing_before=18,
		section_spacing_after=12,
		use_section_dividers=False,
		use_page_borders=False,
		use_header_footer=True
	),
	"magazine": LayoutStyle(
		name="Magazine Style",
		top_margin=1.0,
		bottom_margin=1.0,
		left_margin=1.5,
		right_margin=1.0,
		section_spacing_before=14,
		section_spacing_after=8,
		use_section_dividers=True,
		use_page_borders=True,
		use_header_footer=True
	)
}

# ============================================================================
# COMPLETE DESIGN SYSTEM
# ============================================================================

@dataclass
class DesignSystem:
	"""Complete visual design system for a marketing kit."""
	name: str
	colors: ColorPalette
	typography: TypographyStyle
	layout: LayoutStyle
	description: str

DESIGN_SYSTEMS = {
	"swift_innovation": DesignSystem(
		name="Swift Innovation Style",
		colors=DESIGN_PALETTES["swift_innovation"],
		typography=TYPOGRAPHY_STYLES["swift_modern"],
		layout=LAYOUT_STYLES["standard"],
		description="Modern, professional style matching Swift Innovation's brand"
	),
	"healthcare_professional": DesignSystem(
		name="Healthcare Professional",
		colors=DESIGN_PALETTES["healthcare_professional"],
		typography=TYPOGRAPHY_STYLES["professional_serif"],
		layout=LAYOUT_STYLES["spacious"],
		description="Trust-building design for healthcare and medical companies"
	),
	"tech_startup": DesignSystem(
		name="Tech Startup",
		colors=DESIGN_PALETTES["tech_modern"],
		typography=TYPOGRAPHY_STYLES["tech_sans"],
		layout=LAYOUT_STYLES["compact"],
		description="Modern, energetic design for technology companies"
	),
	"finance_corporate": DesignSystem(
		name="Finance & Corporate",
		colors=DESIGN_PALETTES["finance_trust"],
		typography=TYPOGRAPHY_STYLES["professional_serif"],
		layout=LAYOUT_STYLES["standard"],
		description="Conservative, trustworthy design for financial services"
	),
	"creative_agency": DesignSystem(
		name="Creative Agency",
		colors=DESIGN_PALETTES["creative_bold"],
		typography=TYPOGRAPHY_STYLES["elegant_mixed"],
		layout=LAYOUT_STYLES["magazine"],
		description="Bold, creative design for agencies and creative firms"
	),
	"minimal_modern": DesignSystem(
		name="Minimal Modern",
		colors=DESIGN_PALETTES["minimal_elegant"],
		typography=TYPOGRAPHY_STYLES["tech_sans"],
		layout=LAYOUT_STYLES["spacious"],
		description="Clean, minimal design for modern B2B companies"
	)
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_design_system(name: str) -> DesignSystem:
	"""Get a design system by name."""
	return DESIGN_SYSTEMS.get(name, DESIGN_SYSTEMS["swift_innovation"])

def list_design_systems() -> list:
	"""List all available design systems."""
	return list(DESIGN_SYSTEMS.keys())

def create_custom_design_system(
	name: str,
	color_palette: str = "swift_innovation",
	typography: str = "swift_modern",
	layout: str = "standard",
	description: str = "Custom design system"
) -> DesignSystem:
	"""
	Create a custom design system by mixing components.
	"""
	return DesignSystem(
		name=name,
		colors=DESIGN_PALETTES.get(color_palette, DESIGN_PALETTES["swift_innovation"]),
		typography=TYPOGRAPHY_STYLES.get(typography, TYPOGRAPHY_STYLES["swift_modern"]),
		layout=LAYOUT_STYLES.get(layout, LAYOUT_STYLES["standard"]),
		description=description
	)

def extract_colors_from_brand(hex_colors: list) -> ColorPalette:
	"""
	Create a color palette from brand colors (hex codes).
	"""
	def hex_to_rgb(hex_color: str) -> tuple:
		hex_color = hex_color.lstrip('#')
		return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
	rgb_colors = [hex_to_rgb(c) for c in hex_colors]
	primary = rgb_colors[0] if len(rgb_colors) > 0 else (41, 128, 185)
	secondary = rgb_colors[1] if len(rgb_colors) > 1 else (231, 76, 60)
	return ColorPalette(
		name="Custom Brand Colors",
		primary=primary,
		secondary=secondary,
		dark=(44, 62, 80),
		light=(236, 240, 241),
		text=(52, 73, 94),
		muted=(149, 165, 166)
	)

def preview_design_system(design_system: DesignSystem) -> str:
	"""
	Generate a text preview of a design system.
	"""
	preview = f"""
DESIGN SYSTEM: {design_system.name}
{design_system.description}

COLORS:
  Primary:   RGB{design_system.colors.primary}
  Secondary: RGB{design_system.colors.secondary}
  Dark:      RGB{design_system.colors.dark}
  Light:     RGB{design_system.colors.light}
  Text:      RGB{design_system.colors.text}

TYPOGRAPHY:
  Headings: {design_system.typography.heading_font}
  Body:     {design_system.typography.body_font}
  H1 Size:  {design_system.typography.h1_size}pt
  H2 Size:  {design_system.typography.h2_size}pt
  Body Size: {design_system.typography.body_size}pt

LAYOUT:
  Margins: {design_system.layout.top_margin}" top/bottom, {design_system.layout.left_margin}" left/right
  Section Spacing: {design_system.layout.section_spacing_before}pt before
  Dividers: {'Yes' if design_system.layout.use_section_dividers else 'No'}
  Header/Footer: {'Yes' if design_system.layout.use_header_footer else 'No'}
"""
	return preview
