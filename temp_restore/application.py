"""
Resume Analyzer Flask Application for AWS Elastic Beanstalk
Fully connected to SQLite Database. No hardcoded history.
"""
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- 1. IMPORT CUSTOM MODULES ---
try:
    from analyzer_simple import ResumeAnalyzer
    from resume_parser import ResumeParser
    from database import ResumeDatabase  # This is required for real history
except ImportError as e:
    print(f"CRITICAL ERROR: Module import failed: {e}")
    ResumeAnalyzer = None
    ResumeParser = None
    ResumeDatabase = None

# --- 2. INITIALIZE FLASK APP ---
application = Flask(__name__)
CORS(application)

# --- 3. INITIALIZE HELPERS ---
ANALYZER = ResumeAnalyzer() if ResumeAnalyzer else None
PARSER = ResumeParser() if ResumeParser else None
DB = ResumeDatabase() if ResumeDatabase else None

# --- 4. ROUTES ---

@application.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database_connected': DB is not None,
        'version': '1.8.0 - Real Data'
    })

@application.route('/history', methods=['GET'])
@application.route('/api/history', methods=['GET'])
def history():
    """Return analysis history from database"""
    if DB:
        try:
            history_data = DB.get_history()
            print(f"History retrieved: {len(history_data)} items")
            # Return in format expected by frontend: { analyses: [...] }
            return jsonify({'analyses': history_data})
        except Exception as e:
            print(f"Database Error: {e}")
            traceback.print_exc()
            return jsonify({'error': f'Failed to load history: {str(e)}'}), 500
    else:
        print("Database not initialized")
        return jsonify({'error': 'Database not available'}), 500

@application.route('/api/history/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete an analysis record"""
    if DB:
        try:
            success = DB.delete_analysis(analysis_id)
            if success:
                return jsonify({'success': True, 'message': 'Analysis deleted successfully'})
            else:
                return jsonify({'success': False, 'message': 'Analysis not found'}), 404
        except Exception as e:
            print(f"Delete Error: {e}")
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        return jsonify({'success': False, 'error': 'Database not available'}), 500

@application.route('/stats', methods=['GET'])
@application.route('/api/stats', methods=['GET'])
def stats():
    """Return statistics about analyses"""
    if DB:
        try:
            history_data = DB.get_history()
            if not history_data:
                return jsonify({'stats': {
                    'total_analyses': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0
                }})
            
            scores = [item.get('overall_score', 0) for item in history_data]
            stats_data = {
                'total_analyses': len(history_data),
                'average_score': round(sum(scores) / len(scores), 2),
                'highest_score': max(scores),
                'lowest_score': min(scores)
            }
            return jsonify({'stats': stats_data})
        except Exception as e:
            print(f"Stats Error: {e}")
            return jsonify({'error': 'Failed to load stats'}), 500
    else:
        return jsonify({'error': 'Database not available'}), 500

@application.route('/analyze', methods=['POST'])
def analyze():
    try:
        resume_text = ""
        job_description = ""
        filename = "Text Input"

        # Handle JSON
        if request.is_json:
            data = request.get_json()
            resume_text = data.get('resume', '') or data.get('resume_text', '')
            job_description = data.get('job_description', '')

        # Handle Files
        else:
            job_description = request.form.get('job_description', '')
            if 'resume' in request.files:
                file = request.files['resume']
                if file.filename:
                    filename = secure_filename(file.filename)
                    temp_path = os.path.join('/tmp', filename)
                    file.save(temp_path)
                    try:
                        if PARSER:
                            parsed_data = PARSER.parse_resume(temp_path)
                            resume_text = parsed_data.get('raw_text', '')
                        else:
                            with open(temp_path, 'r', errors='ignore') as f:
                                resume_text = f.read()
                    except Exception:
                        pass
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

        if not resume_text or not job_description:
            return jsonify({'error': 'Missing data'}), 400

        if ANALYZER:
            result = ANALYZER.analyze(resume_text, job_description)
            
            # SAVE TO DATABASE
            if DB:
                result['resume_name'] = filename
                result['job_description'] = job_description
                try:
                    DB.save_analysis(result)
                except Exception as e:
                    print(f"DB Save Error: {e}")

            return jsonify(result)
        else:
            return jsonify({'error': 'Analyzer module not initialized'}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)