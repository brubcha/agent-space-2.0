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

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Use the new function for AgentBuilder workflow
from agentspace_agentbuilder import generate_marketing_kit
# Remove legacy import and use AgentBuilder workflow
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
        guild = discord.Object(id=1097296150014464163)
        synced = await bot.tree.sync(guild=guild)
        print(f'✓ Synced {len(synced)} command(s) to guild {guild.id}')
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
    


@bot.tree.command(name="new-request", description="Create a new marketing kit request")
@app_commands.describe(
    request_type="Type of request (default: Marketing Kit)",
    client_name="Name of the client company",
    website="Client's website URL",
    offerings="Products/services offered (comma-separated)",
    competitors="Main competitors (comma-separated)",
    additional_info="Any other relevant information"
)
async def new_request(
    interaction: discord.Interaction,
    request_type: str = "Marketing Kit",
    client_name: str = None,
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
        # Register user
        register_discord_user(str(interaction.user.id), interaction.user.name)

        # Create request in database with status 'pending'
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO discord_requests 
                (discord_id, guild_id, channel_id, request_type, client_name, website, offerings, competitors, additional_info, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
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
    except Exception as e:
        await interaction.followup.send(f"❌ Error creating request: {e}")
        return

    # Prompt for attachments
    embed = discord.Embed(
        title="📎 Attach Files (Optional)",
        description=(
            f"Request ID: #{request_id}\n\n"
            "If you have any files to attach (brand story, logo, etc.), please upload them now in this channel.\n"
            f"When finished, type `/submit-request {request_id}` to continue."
        ),
        color=discord.Color.orange()
    )
    embed.add_field(name="Client", value=client_name, inline=True)
    embed.add_field(name="Type", value=request_type, inline=True)
    embed.add_field(name="Status", value="Awaiting attachments...", inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="submit-request", description="Submit your request after uploading attachments")
@app_commands.describe(request_id="The ID of your pending request")
async def submit_request(interaction: discord.Interaction, request_id: int):
    """Submit a pending request and generate the marketing kit."""
    # Update status to 'processing'
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE discord_requests SET status = 'processing' WHERE id = ? AND discord_id = ?
    ''', (request_id, str(interaction.user.id)))
    conn.commit()
    # Fetch request details
    c.execute('''
        SELECT client_name, request_type, website, offerings, competitors, additional_info FROM discord_requests WHERE id = ? AND discord_id = ?
    ''', (request_id, str(interaction.user.id)))
    req = c.fetchone()
    conn.close()
    if not req:
        await interaction.response.send_message("❌ Request not found or you don't have permission to submit it.", ephemeral=True)
        return

    client_name, request_type, website, offerings, competitors, additional_info = req
    # Defer response
    await interaction.response.defer(thinking=True)
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
        error_embed = discord.Embed(
            title="❌ Error",
            description="Failed to generate marketing kit.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)
    
    # If you need to show request history, open a new connection here
    # Example:
    # conn = sqlite3.connect(DB_PATH)
    # c = conn.cursor()
    # c.execute('''SELECT * FROM discord_requests WHERE discord_id = ? ORDER BY created_at DESC LIMIT 10''', (str(interaction.user.id),))
    # requests = c.fetchall()
    # conn.close()
    # if not requests:
    #     await interaction.response.send_message(
    #         "You haven't made any requests yet. Use `/new-request` to get started!",
    #         ephemeral=True
    #     )
    #     return
    # embed = discord.Embed(
    #     title=f"📋 Your Requests ({len(requests)})",
    #     color=discord.Color.blue()
    # )
    # for req in requests:
    #     ...


@bot.tree.command(name="download", description="Download a completed marketing kit")
@app_commands.describe(request_id="The ID of your request")
async def download(interaction: discord.Interaction, request_id: int):
    """Download a completed marketing kit."""
    import os
    import traceback
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT status, docx_output_path, client_name
            FROM discord_requests
            WHERE id = ? AND discord_id = ?
        ''', (request_id, str(interaction.user.id)))
        result = c.fetchone()
    if not result:
        print(f"[ERROR] Download: No result for request_id={request_id}, user={interaction.user.id}")
        await interaction.response.send_message(
            "❌ Request not found or you don't have permission to access it.",
            ephemeral=True
        )
        return
    status, docx_path, client_name = result
    print(f"[DOWNLOAD DEBUG] status={status}, docx_path={docx_path}, client_name={client_name}")
    # Make path absolute if not already
    if docx_path and not os.path.isabs(docx_path):
        docx_path = os.path.abspath(docx_path)
    print(f"[DOWNLOAD DEBUG] Absolute docx_path: {docx_path}")
    if status != 'completed':
        await interaction.response.send_message(
            f"⏳ Request #{request_id} is still {status}. Please wait for it to complete.",
            ephemeral=True
        )
        return
    if not docx_path or not os.path.exists(docx_path):
        print(f"[ERROR] Download: File not found at {docx_path}")
        await interaction.response.send_message(
            f"❌ File not found. Path: {docx_path}",
            ephemeral=True
        )
        return
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
        print(f"[ERROR] Exception sending file: {e}\n{traceback.format_exc()}")
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
        with sqlite3.connect(DB_PATH) as conn:
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
                    sql = (
                        """
                        INSERT INTO discord_files (request_id, filename, filepath, file_type)
                        VALUES (?, ?, ?, ?)
                        """
                    )
                    c.execute(sql, (request_id, filename, filepath, attachment.content_type))
                conn.commit()
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
    
    # --- NEW LOGIC: Use same enrichment/validation as webapp ---
    import sqlite3
    from agentspace_scrapers import analyze_all_sources
    from agentspace_inputs import prepare_inputs_with_defaults
    from agentspace_main_AI import run_marketing_kit_generation_AI
    try:
        from agentspace_webapp import sanitize_unicode, remove_surrogates_and_log
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

    # 1. Gather uploaded files for this request
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT filepath FROM discord_files WHERE request_id = ?', (request_id,))
        uploaded_files = [row[0] for row in c.fetchall()]

    # 2. Build form_data dict (like webapp)
    form_data = {"company_name": client_name}
    if website:
        form_data["website"] = website
    if offerings:
        form_data["products_services"] = [s.strip() for s in offerings.split(',') if s.strip()]
    if competitors:
        form_data["main_competitors"] = [c.strip() for c in competitors.split(',') if c.strip()]
    if additional_info:
        form_data["company_overview"] = additional_info

    # 3. Enrich and validate inputs
    enriched_profile = analyze_all_sources(
        website_url=website,
        uploaded_files=uploaded_files,
        form_data=form_data
    )
    validated_inputs = prepare_inputs_with_defaults(enriched_profile)
    if 'error' in enriched_profile and not enriched_profile.get('company_overview'):
        # Save error JSON as in webapp
        error_json = {
            "success": False,
            "error": enriched_profile['error'],
            "output": {},
            "metadata": {},
            "errors": [enriched_profile['error']]
        }
        json_filename = f"discord_marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(OUTPUT_FOLDER, json_filename)
        safe_error_json = sanitize_unicode(error_json)
        log_id = request_id if request_id is not None else 'unknown'
        error_log_path = os.path.join(OUTPUT_FOLDER, f"error_log_{log_id}.txt")
        scrubbed_error_json = remove_surrogates_and_log(safe_error_json, log_path=error_log_path)
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(scrubbed_error_json, indent=2, ensure_ascii=True))
        # Update DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE discord_requests
            SET status = 'failed',
                json_output_path = ?,
                docx_output_path = NULL,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (json_path, request_id))
        conn.commit()
        conn.close()
        return False
    if 'error' in enriched_profile and enriched_profile.get('company_overview'):
        enriched_profile.pop('error', None)
    if 'error' in validated_inputs:
        validated_inputs.pop('error', None)

    # 4. Run agent (same as webapp)
    result = run_marketing_kit_generation_AI(validated_inputs, output_format="json", provider="claude")
    if result and result.success:
        json_filename = f"discord_marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(OUTPUT_FOLDER, json_filename)
        safe_result = sanitize_unicode(result.to_dict())
        log_id = request_id if request_id is not None else 'unknown'
        error_log_path = os.path.join(OUTPUT_FOLDER, f"error_log_{log_id}.txt")
        scrubbed_result = remove_surrogates_and_log(safe_result, log_path=error_log_path)
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(scrubbed_result, indent=2, ensure_ascii=True))
        # Generate DOCX
        from agentspace_docx_generator import generate_marketing_kit_docx
        docx_path = generate_marketing_kit_docx(
            company_name=client_name,
            agent_results=result.output,
            output_dir=OUTPUT_FOLDER
        )
        # Update DB
        with sqlite3.connect(DB_PATH) as conn:
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
