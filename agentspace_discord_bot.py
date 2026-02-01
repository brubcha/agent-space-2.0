"""
AgentSpace Discord Bot

Allows users to interact with AgentSpace via Discord:
- Make requests
- Upload files
- Get DOCX downloads
- Check request status
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
import json
from datetime import datetime
from pathlib import Path
import sqlite3

# Import your agent
from agentspace_main import run_marketing_kit_generation
from agentspace_docx_generator import generate_marketing_kit_docx

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
UPLOAD_FOLDER = 'discord_uploads'
OUTPUT_FOLDER = 'discord_outputs'
DB_PATH = 'agentspace_discord.db'

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)


# ============================================================================
# DATABASE
# ============================================================================

def init_discord_db():
    """Initialize Discord bot database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Discord users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS discord_users (
            discord_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Discord requests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS discord_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT NOT NULL,
            guild_id TEXT,
            channel_id TEXT,
            request_type TEXT NOT NULL,
            client_name TEXT NOT NULL,
            website TEXT,
            offerings TEXT,
            competitors TEXT,
            additional_info TEXT,
            status TEXT DEFAULT 'pending',
            json_output_path TEXT,
            docx_output_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (discord_id) REFERENCES discord_users (discord_id)
        )
    ''')
    
    # Discord files table
    c.execute('''
        CREATE TABLE IF NOT EXISTS discord_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_type TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES discord_requests (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def register_discord_user(discord_id: str, username: str):
    """Register or update a Discord user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO discord_users (discord_id, username)
        VALUES (?, ?)
    ''', (discord_id, username))
    conn.commit()
    conn.close()


# ============================================================================
# BOT EVENTS
# ============================================================================

@bot.event
async def on_ready():
    """Bot startup."""
    print(f'✓ {bot.user} is now online!')
    print(f'  Connected to {len(bot.guilds)} server(s)')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'✓ Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    
    # Set status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for /help | Marketing Kits"
        )
    )


@bot.event
async def on_member_join(member):
    """Welcome new members."""
    # Send welcome DM
    try:
        embed = discord.Embed(
            title="👋 Welcome to AgentSpace!",
            description=(
                "I'm your AI-powered marketing kit generator.\n\n"
                "**Get Started:**\n"
                "• Use `/new-request` to create a marketing kit\n"
                "• Use `/my-requests` to see your history\n"
                "• Use `/help` for more commands\n\n"
                "Let's build something amazing!"
            ),
            color=discord.Color.blue()
        )
        await member.send(embed=embed)
    except:
        pass  # User has DMs disabled


# ============================================================================
# SLASH COMMANDS
# ============================================================================

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Help command."""
    embed = discord.Embed(
        title="🤖 AgentSpace Commands",
        description="Generate professional marketing kits using AI",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/new-request",
        value="Create a new marketing kit request",
        inline=False
    )
    
    embed.add_field(
        name="/my-requests",
        value="View your request history",
        inline=False
    )
    
    embed.add_field(
        name="/request-status <id>",
        value="Check status of a specific request",
        inline=False
    )
    
    embed.add_field(
        name="/download <id>",
        value="Download completed marketing kit",
        inline=False
    )
    
    embed.set_footer(text="Need help? Ask in #support")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="new-request", description="Create a new marketing kit request")
@app_commands.describe(
    client_name="Name of the client company",
    request_type="Type of request (default: Marketing Kit)",
    website="Client's website URL",
    offerings="Products/services offered (comma-separated)",
    competitors="Main competitors (comma-separated)",
    additional_info="Any other relevant information"
)
async def new_request(
    interaction: discord.Interaction,
    client_name: str,
    request_type: str = "Marketing Kit",
    website: str = None,
    offerings: str = None,
    competitors: str = None,
    additional_info: str = None
):
    """Create a new marketing kit request."""
    
    # Register user
    register_discord_user(str(interaction.user.id), interaction.user.name)
    
    # Defer response (this can take time)
    await interaction.response.defer(thinking=True)
    
    try:
        # Create request in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO discord_requests 
            (discord_id, guild_id, channel_id, request_type, client_name, website, offerings, competitors, additional_info, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'processing')
        ''', (
            str(interaction.user.id),
            str(interaction.guild_id) if interaction.guild else None,
            str(interaction.channel_id),
            request_type,
            client_name,
            website,
            offerings,
            competitors,
            additional_info
        ))
        request_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Send initial response
        embed = discord.Embed(
            title="🚀 Processing Your Request",
            description=f"Request ID: #{request_id}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Client", value=client_name, inline=True)
        embed.add_field(name="Type", value=request_type, inline=True)
        embed.add_field(name="Status", value="⏳ Processing...", inline=False)
        
        await interaction.followup.send(embed=embed)
        
        # Process the request
        result = await process_discord_request(
            request_id=request_id,
            client_name=client_name,
            website=website,
            offerings=offerings,
            competitors=competitors,
            additional_info=additional_info
        )
        
        if result:
            # Send success message
            success_embed = discord.Embed(
                title="✅ Marketing Kit Generated!",
                description=f"Request ID: #{request_id}",
                color=discord.Color.green()
            )
            success_embed.add_field(name="Client", value=client_name, inline=True)
            success_embed.add_field(name="Status", value="✓ Completed", inline=True)
            success_embed.add_field(
                name="Download",
                value=f"Use `/download {request_id}` to get your files!",
                inline=False
            )
            
            await interaction.followup.send(embed=success_embed)
        
        else:
            raise Exception("Generation failed")
    
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"Failed to generate marketing kit: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)


@bot.tree.command(name="my-requests", description="View your request history")
async def my_requests(interaction: discord.Interaction):
    """View user's request history."""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, client_name, request_type, status, created_at
        FROM discord_requests
        WHERE discord_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    ''', (str(interaction.user.id),))
    
    requests = c.fetchall()
    conn.close()
    
    if not requests:
        await interaction.response.send_message(
            "You haven't made any requests yet. Use `/new-request` to get started!",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title=f"📋 Your Requests ({len(requests)})",
        color=discord.Color.blue()
    )
    
    for req in requests:
        status_emoji = {
            'pending': '⏳',
            'processing': '⚙️',
            'completed': '✅',
            'failed': '❌'
        }.get(req[3], '❓')
        
        embed.add_field(
            name=f"#{req[0]} - {req[1]}",
            value=f"{status_emoji} {req[3].title()} | {req[2]} | {req[4]}",
            inline=False
        )
    
    embed.set_footer(text="Use /download <id> to download completed kits")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="download", description="Download a completed marketing kit")
@app_commands.describe(request_id="The ID of your request")
async def download(interaction: discord.Interaction, request_id: int):
    """Download a completed marketing kit."""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT status, docx_output_path, client_name
        FROM discord_requests
        WHERE id = ? AND discord_id = ?
    ''', (request_id, str(interaction.user.id)))
    
    result = c.fetchone()
    conn.close()
    
    if not result:
        await interaction.response.send_message(
            "❌ Request not found or you don't have permission to access it.",
            ephemeral=True
        )
        return
    
    status, docx_path, client_name = result
    
    if status != 'completed':
        await interaction.response.send_message(
            f"⏳ Request #{request_id} is still {status}. Please wait for it to complete.",
            ephemeral=True
        )
        return
    
    if not docx_path or not os.path.exists(docx_path):
        await interaction.response.send_message(
            "❌ File not found. Please contact support.",
            ephemeral=True
        )
        return
    
    # Send the file
    await interaction.response.defer(thinking=True)
    
    try:
        file = discord.File(docx_path, filename=f"Marketing_Kit_{client_name.replace(' ', '_')}.docx")
        
        embed = discord.Embed(
            title="📄 Your Marketing Kit",
            description=f"Request ID: #{request_id}\nClient: {client_name}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Generated by AgentSpace")
        
        await interaction.followup.send(embed=embed, file=file)
    
    except Exception as e:
        await interaction.followup.send(f"❌ Error sending file: {str(e)}")


# ============================================================================
# FILE UPLOAD HANDLER
# ============================================================================

@bot.event
async def on_message(message):
    """Handle file uploads and regular messages."""
    
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Check for file attachments
    if message.attachments:
        # Check if user has a pending request
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT id FROM discord_requests
            WHERE discord_id = ? AND status = 'pending'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (str(message.author.id),))
        
        pending = c.fetchone()
        
        if pending:
            request_id = pending[0]
            
            # Save attachments
            for attachment in message.attachments:
                filename = attachment.filename
                filepath = os.path.join(UPLOAD_FOLDER, f"{request_id}_{filename}")
                
                await attachment.save(filepath)
                
                c.execute('''
                    INSERT INTO discord_files (request_id, filename, filepath, file_type)
                    VALUES (?, ?, ?, ?)
                ''', (request_id, filename, filepath, attachment.content_type))
            
            conn.commit()
            conn.close()
            
            await message.add_reaction('✅')
            await message.reply(
                f"✅ Files added to request #{request_id}!\n"
                f"Continue with the request or use `/submit-request {request_id}` when ready."
            )
        else:
            await message.reply(
                "💡 Create a request first using `/new-request`, then upload files!"
            )
        
        return
    
    # Process commands
    await bot.process_commands(message)


# ============================================================================
# PROCESSING LOGIC
# ============================================================================

async def process_discord_request(request_id, client_name, website, offerings, competitors, additional_info):
    """Process a marketing kit request from Discord."""
    
    # Convert Discord inputs to agent format
    agent_inputs = {
        "company_name": client_name,
        "industry": "To be determined",
        "company_size": "To be determined",
        "website": website or "",
        
        "company_overview": additional_info if additional_info else f"{client_name} offers {offerings if offerings else 'various services'}",
        "mission_statement": "To be defined",
        "core_values": ["Quality", "Innovation", "Customer Focus"],
        "unique_selling_proposition": offerings if offerings else "To be defined",
        
        "target_audience_description": "To be defined",
        "customer_pain_points": ["To be researched"],
        "customer_goals": ["To be researched"],
        
        "main_competitors": competitors.split(',') if competitors else [],
        "competitive_advantages": ["To be defined"],
        "market_position": "To be defined",
        
        "brand_personality_adjectives": ["Professional", "Reliable", "Innovative"],
        "tone_preferences": "Professional and approachable",
        
        "products_services": offerings.split(',') if offerings else ["To be defined"],
        "business_model": "B2B",
        "key_features": ["To be defined"],
        
        "primary_business_goal": "To be defined",
        "target_markets": ["To be researched"],
        "growth_stage": "Growth",
        
        "proof_points": [],
        "primary_channels": ["Website", "Social Media"],
    }
    
    # Run the agent
    result = run_marketing_kit_generation(agent_inputs, output_format="json")
    
    if result and result.success:
        # Save JSON
        json_filename = f"discord_marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(OUTPUT_FOLDER, json_filename)
        
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
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(safe_result, f, indent=2, ensure_ascii=True)
        
        # Generate DOCX
        docx_filename = f"Marketing_Kit_{client_name.replace(' ', '_')}_{request_id}.docx"
        docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)
        
        generate_marketing_kit_docx(
            company_name=client_name,
            agent_results=result.output,
            output_dir=OUTPUT_FOLDER
        )
        
        # Update database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE discord_requests
            SET status = 'completed',
                json_output_path = ?,
                docx_output_path = ?,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (json_path, docx_path, request_id))
        conn.commit()
        conn.close()
        
        return True
    
    return False


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    init_discord_db()
    
    # Get bot token from environment variable
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not DISCORD_BOT_TOKEN:
        print("❌ ERROR: DISCORD_BOT_TOKEN not found in environment variables")
        print("\nTo set up:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a New Application")
        print("3. Go to Bot section, create a bot")
        print("4. Copy the token")
        print("5. Set environment variable: DISCORD_BOT_TOKEN=your_token_here")
        print("\nOr run: export DISCORD_BOT_TOKEN='your_token_here'")
        exit(1)
    
    print("\n" + "="*60)
    print("AgentSpace Discord Bot")
    print("="*60)
    print("\nStarting bot...")
    print("Commands:")
    print("  /help - Show all commands")
    print("  /new-request - Create marketing kit")
    print("  /my-requests - View history")
    print("  /download - Get your files")
    print("\n" + "="*60 + "\n")
    
    bot.run(DISCORD_BOT_TOKEN)
