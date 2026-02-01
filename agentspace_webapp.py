# Final surrogate scrubber and logger
import sys
def remove_surrogates_and_log(obj, log_path=None, path_stack=None):
    if path_stack is None:
        path_stack = []
    if isinstance(obj, str):
        # If surrogates present, log and replace
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj):
            if log_path:
                with open(log_path, 'a', encoding='utf-8', errors='replace') as log:
                    log.write(f"Surrogate found at {'.'.join(map(str, path_stack))}: {repr(obj)}\n")
            # Replace surrogates with replacement char
            return ''.join(ch if not (0xD800 <= ord(ch) <= 0xDFFF) else '\uFFFD' for ch in obj)
        return obj
    elif isinstance(obj, dict):
        return {k: remove_surrogates_and_log(v, log_path, path_stack + [k]) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in enumerate(obj)]
    elif isinstance(obj, tuple):
        return tuple(remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in enumerate(obj))
    elif isinstance(obj, set):
        return {remove_surrogates_and_log(i, log_path, path_stack + [str(idx)]) for idx, i in enumerate(obj)}
    elif obj is None or isinstance(obj, (int, float, bool)):
        return obj
    else:
        # For any other type, convert to string and sanitize
        return remove_surrogates_and_log(str(obj), log_path, path_stack)

# Function to remove all surrogate code points from strings, recursively for any JSON-serializable structure
def sanitize_unicode(obj):
    if isinstance(obj, str):
        # Encode/decode with errors='replace' to remove/replace invalid surrogates
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
        # For any other type, convert to string and sanitize
        return sanitize_unicode(str(obj))
"""
AgentSpace Web Application

A web interface for generating marketing kits with:
- User authentication
- Request forms with file uploads
- DOCX downloads
- Request history
- Admin controls
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from pathlib import Path
import sqlite3

# Import your agent

from agentspace_main_AI import run_marketing_kit_generation_AI
from agentspace_docx_generator import generate_marketing_kit_docx
from agentspace_scrapers import analyze_all_sources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure folders exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Requests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
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
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Files table (for uploaded files)
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_type TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES requests (id)
        )
    ''')
    
    conn.commit()
    conn.close()


# ============================================================================
# USER MODEL
# ============================================================================

class User(UserMixin):
    def __init__(self, id, username, email, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email, is_admin FROM users WHERE id = ?', (user_id,))
    user_data = c.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None


# ============================================================================
# ROUTES - AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    """Homepage - redirect to dashboard if logged in, otherwise to login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('agentspace.db')
        c = conn.cursor()
        c.execute('SELECT id, username, email, password_hash, is_admin FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2], user_data[4])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('agentspace.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'error')
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============================================================================
# ROUTES - MAIN APPLICATION
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing request history."""
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, request_type, client_name, status, created_at, completed_at
        FROM requests
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 20
    ''', (current_user.id,))
    requests = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', requests=requests, user=current_user)


@app.route('/new-request', methods=['GET', 'POST'])
@login_required
def new_request():
    """Form for creating a new marketing kit request."""
    
    if request.method == 'POST':
        # Get form data
        request_type = request.form.get('request_type', 'Marketing Kit')
        client_name = request.form['client_name']
        website = request.form.get('website', '')
        offerings = request.form.get('offerings', '')
        competitors = request.form.get('competitors', '')
        additional_info = request.form.get('additional_info', '')
        
        # Create request in database
        conn = sqlite3.connect('agentspace.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO requests (user_id, request_type, client_name, website, offerings, competitors, additional_info, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'processing')
        ''', (current_user.id, request_type, client_name, website, offerings, competitors, additional_info))
        request_id = c.lastrowid
        conn.commit()
        
        # Handle file uploads
        uploaded_files = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    # Create user-specific upload folder
                    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id), str(request_id))
                    Path(user_upload_folder).mkdir(parents=True, exist_ok=True)
                    
                    filepath = os.path.join(user_upload_folder, filename)
                    file.save(filepath)
                    
                    # Save file info to database
                    c.execute('''
                        INSERT INTO uploaded_files (request_id, filename, filepath, file_type)
                        VALUES (?, ?, ?, ?)
                    ''', (request_id, filename, filepath, file.content_type))
                    
                    uploaded_files.append(filepath)
        
        conn.commit()
        conn.close()
        
        # Generate marketing kit asynchronously (in a real app, use Celery or similar)
        # For now, we'll do it synchronously
        try:
            result = process_marketing_kit_request(
                request_id=request_id,
                client_name=client_name,
                website=website,
                offerings=offerings,
                competitors=competitors,
                additional_info=additional_info,
                uploaded_files=uploaded_files
            )
            
            flash('Marketing kit generated successfully!', 'success')
            return redirect(url_for('view_request', request_id=request_id))
        
        except Exception as e:
            flash(f'Error generating marketing kit: {str(e)}', 'error')
            # Update status to failed
            conn = sqlite3.connect('agentspace.db')
            c = conn.cursor()
            c.execute('UPDATE requests SET status = ? WHERE id = ?', ('failed', request_id))
            conn.commit()
            conn.close()
    
    return render_template('new_request.html')


@app.route('/request/<int:request_id>')
@login_required
def view_request(request_id):
    """View a specific request and download files."""
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    
    # Get request details
    c.execute('''
        SELECT id, request_type, client_name, website, offerings, competitors, 
               additional_info, status, json_output_path, docx_output_path, 
               created_at, completed_at
        FROM requests
        WHERE id = ? AND user_id = ?
    ''', (request_id, current_user.id))
    
    request_data = c.fetchone()
    
    if not request_data:
        flash('Request not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Get uploaded files
    c.execute('''
        SELECT filename, file_type, uploaded_at
        FROM uploaded_files
        WHERE request_id = ?
    ''', (request_id,))
    
    uploaded_files = c.fetchall()
    conn.close()
    
    return render_template('view_request.html', request=request_data, files=uploaded_files)


@app.route('/download/<int:request_id>/<file_type>')
@login_required
def download_file(request_id, file_type):
    """Download generated files (JSON or DOCX)."""
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    c.execute('''
        SELECT json_output_path, docx_output_path
        FROM requests
        WHERE id = ? AND user_id = ?
    ''', (request_id, current_user.id))
    
    result = c.fetchone()
    conn.close()
    
    if not result:
        flash('Request not found', 'error')
        return redirect(url_for('dashboard'))
    
    if file_type == 'json' and result[0]:
        return send_file(result[0], as_attachment=True)
    elif file_type == 'docx' and result[1]:
        return send_file(result[1], as_attachment=True)
    else:
        flash('File not found', 'error')
        return redirect(url_for('view_request', request_id=request_id))


# ============================================================================
# ROUTES - ADMIN
# ============================================================================

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard - only accessible to admin users."""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    
    # Get all requests
    c.execute('''
        SELECT r.id, u.username, r.client_name, r.status, r.created_at
        FROM requests r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
        LIMIT 50
    ''')
    all_requests = c.fetchall()
    
    # Get all users
    c.execute('SELECT id, username, email, is_admin, created_at FROM users')
    all_users = c.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', requests=all_requests, users=all_users)


# ============================================================================
# PROCESSING LOGIC
# ============================================================================



def process_marketing_kit_request(request_id, client_name, website, offerings, competitors, additional_info, uploaded_files):
    """
    FIXED version that handles validation properly.
    """
    print("=" * 80)
    print("INTELLIGENT MARKETING KIT GENERATION")
    print("=" * 80)
    print()

    # Import the helper function
    from agentspace_inputs import prepare_inputs_with_defaults

    # Step 1: Prepare minimal form data
    form_data = {
        "company_name": client_name,
    }
    # Add optional fields only if provided
    if website:
        form_data["website"] = website
    if offerings:
        form_data["products_services"] = [s.strip() for s in offerings.split(',') if s.strip()]
    if competitors:
        form_data["main_competitors"] = [c.strip() for c in competitors.split(',') if c.strip()]
    if additional_info:
        form_data["company_overview"] = additional_info

    # Step 2: Analyze all sources (website + files + form)
    from agentspace_scrapers import analyze_all_sources
    enriched_profile = analyze_all_sources(
        website_url=website,
        uploaded_files=uploaded_files,
        form_data=form_data
    )

    # Step 3: Prepare with defaults to ensure validation passes
    validated_inputs = prepare_inputs_with_defaults(enriched_profile)

    # Only fail if both structured and fallback content are missing
    if 'error' in enriched_profile and not enriched_profile.get('company_overview'):
        error_json = {
            "success": False,
            "error": enriched_profile['error'],
            "output": {},
            "metadata": {},
            "errors": [enriched_profile['error']]
        }
        json_filename = f"marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(app.config['OUTPUT_FOLDER'], json_filename)
        # Sanitize before saving
        safe_error_json = sanitize_unicode(error_json)
        log_id = request_id if request_id is not None else 'unknown'
        error_log_path = os.path.join(app.config['OUTPUT_FOLDER'], f"error_log_{log_id}.txt")
        # Final surrogate scrub before saving
        scrubbed_error_json = remove_surrogates_and_log(safe_error_json, log_path=error_log_path)
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(scrubbed_error_json, indent=2, ensure_ascii=True))
        except Exception as e:
            # Log error and problematic data, always create a log file
            try:
                with open(error_log_path, 'a', encoding='utf-8', errors='replace') as log:
                    log.write(f"Serialization error: {str(e)}\n\nData:\n{scrubbed_error_json}\n")
                print(f"Serialization error logged to {error_log_path}")
            except Exception as log_e:
                print(f"Failed to write error log: {log_e}")
            raise
        # Optionally update DB status to failed
        conn = sqlite3.connect('agentspace.db')
        c = conn.cursor()
        c.execute('''
            UPDATE requests
            SET status = 'failed',
                json_output_path = ?,
                docx_output_path = NULL,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (json_path, request_id))
        conn.commit()
        conn.close()
        return error_json
    # If company_overview is present, clear error for downstream kit generation
    if 'error' in enriched_profile and enriched_profile.get('company_overview'):
        enriched_profile.pop('error', None)

    # Also ensure error is not present in validated_inputs
    if 'error' in validated_inputs:
        validated_inputs.pop('error', None)

    # Step 4: Generate marketing kit with enriched data
    from agentspace_main_AI import run_marketing_kit_generation_AI
    result = run_marketing_kit_generation_AI(validated_inputs, output_format="json", provider="claude")

    if result and result.success:
        # Save JSON output
        json_filename = f"marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(app.config['OUTPUT_FOLDER'], json_filename)

        # Sanitize before saving
        safe_result = sanitize_unicode(result.to_dict())
        log_id = request_id if request_id is not None else 'unknown'
        error_log_path = os.path.join(app.config['OUTPUT_FOLDER'], f"error_log_{log_id}.txt")
        # Final surrogate scrub before saving
        scrubbed_result = remove_surrogates_and_log(safe_result, log_path=error_log_path)
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(scrubbed_result, indent=2, ensure_ascii=True))
        except Exception as e:
            # Log error and problematic data, always create a log file
            try:
                with open(error_log_path, 'a', encoding='utf-8', errors='replace') as log:
                    log.write(f"Serialization error: {str(e)}\n\nData:\n{scrubbed_result}\n")
                print(f"Serialization error logged to {error_log_path}")
            except Exception as log_e:
                print(f"Failed to write error log: {log_e}")
            raise

        # Generate DOCX and get the actual file path
        from agentspace_docx_generator import generate_marketing_kit_docx
        docx_path = generate_marketing_kit_docx(
            company_name=client_name,
            agent_results=result.output,
            output_dir=app.config['OUTPUT_FOLDER']
        )

        # Update database
        conn = sqlite3.connect('agentspace.db')
        c = conn.cursor()
        c.execute('''
            UPDATE requests
            SET status = 'completed',
                json_output_path = ?,
                docx_output_path = ?,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (json_path, docx_path, request_id))
        conn.commit()
        conn.close()

        return result
    else:
        raise Exception("Agent failed to generate marketing kit")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Create default admin user if doesn't exist
    conn = sqlite3.connect('agentspace.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if c.fetchone()[0] == 0:
        admin_password = generate_password_hash('admin123')  # CHANGE THIS!
        c.execute(
            'INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)',
            ('admin', 'admin@agentspace.com', admin_password, 1)
        )
        conn.commit()
        print("✓ Default admin user created:")
        print("  Username: admin")
        print("  Password: admin123")
        print("  ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
    conn.close()
    
    print("\n" + "="*60)
    print("AgentSpace Web Application")
    print("="*60)
    print("\nStarting server...")
    print("Visit: http://localhost:5000")
    print("\nDefault login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
