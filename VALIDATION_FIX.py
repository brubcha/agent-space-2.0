"""
FIXED Web App Integration

This fixes the validation error by using the new flexible input schema.
"""

# ============================================================================
# INSTRUCTIONS TO FIX YOUR WEBAPP
# ============================================================================

# 1. REPLACE agentspace-inputs.py with agentspace-inputs-FIXED.py
#    - Download agentspace-inputs-FIXED.py
#    - Rename it to: agentspace-inputs.py
#    - Replace your existing agentspace-inputs.py

# 2. UPDATE your agentspace-webapp.py process_marketing_kit_request function
#    - Find the function (around line 450)
#    - Replace with the version below

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
    
    # Step 4: Generate marketing kit with enriched data
    from agentspace_main import run_marketing_kit_generation
    
    result = run_marketing_kit_generation(validated_inputs, output_format="json")
    
    if result and result.success:
        # Save JSON output
        json_filename = f"marketing_kit_{client_name.replace(' ', '_')}_{request_id}.json"
        json_path = os.path.join(app.config['OUTPUT_FOLDER'], json_filename)
        
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
        from agentspace_docx_generator import generate_marketing_kit_docx
        
        docx_filename = f"Marketing_Kit_{client_name.replace(' ', '_')}_{request_id}.docx"
        docx_path = os.path.join(app.config['OUTPUT_FOLDER'], docx_filename)
        
        generate_marketing_kit_docx(
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
# ALTERNATIVE: Quick Patch (If you don't want to replace the whole file)
# ============================================================================

# Just add this to the TOP of your existing process_marketing_kit_request:

"""
def process_marketing_kit_request(request_id, client_name, website, offerings, competitors, additional_info, uploaded_files):
    
    # ADD THESE LINES AT THE VERY BEGINNING:
    from agentspace_inputs import prepare_inputs_with_defaults
    
    # ... rest of your existing code ...
    
    # Then BEFORE calling run_marketing_kit_generation, add:
    enriched_profile = prepare_inputs_with_defaults(enriched_profile)
    
    # THEN call:
    result = run_marketing_kit_generation(enriched_profile, output_format="json")
"""
