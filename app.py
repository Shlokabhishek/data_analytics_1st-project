"""
Netflix Content Strategy Dashboard - Web Application
Flask-based interactive dashboard
Deployable on Vercel, Heroku, or any WSGI server
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
from netflix_analysis import NetflixAnalyzer

app = Flask(__name__)

# Initialize analyzer
analyzer = NetflixAnalyzer('netflix_titles.csv')

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/summary')
def get_summary():
    """API endpoint for summary statistics"""
    stats = analyzer.get_summary_stats()
    return jsonify(stats)

@app.route('/api/content-distribution')
def get_content_distribution():
    """API endpoint for content distribution data"""
    data = analyzer.analyze_content_distribution()
    
    return jsonify({
        'type_distribution': data['type_distribution'].to_dict(),
        'genre_distribution': data['genre_distribution'].head(15).to_dict(),
        'country_distribution': data['country_distribution'].head(15).to_dict()
    })

@app.route('/api/lifecycle-trends')
def get_lifecycle_trends():
    """API endpoint for lifecycle trends"""
    data = analyzer.analyze_content_lifecycle()
    
    # Get last 20 years of data
    yearly_data = data['yearly_releases'].tail(20)
    
    return jsonify({
        'yearly_releases': {
            'years': yearly_data.index.tolist(),
            'movies': yearly_data['Movie'].tolist() if 'Movie' in yearly_data.columns else [],
            'tv_shows': yearly_data['TV Show'].tolist() if 'TV Show' in yearly_data.columns else []
        },
        'rating_distribution': data['rating_distribution'].head(10).to_dict(),
        'movie_duration_stats': {
            'mean': float(data['movie_durations']['mean']),
            'median': float(data['movie_durations']['50%']),
            'min': float(data['movie_durations']['min']),
            'max': float(data['movie_durations']['max'])
        }
    })

@app.route('/api/saturation-analysis')
def get_saturation_analysis():
    """API endpoint for saturation and opportunity analysis"""
    data = analyzer.analyze_saturation_opportunity()
    
    return jsonify({
        'oversaturated_genres': data['oversaturated_genres'].to_dict(),
        'underserved_genres': data['underserved_genres'].to_dict(),
        'emerging_markets': data['emerging_markets'].to_dict(),
        'content_age_distribution': data['content_age_distribution'].to_dict()
    })

@app.route('/api/investment-plan')
def get_investment_plan():
    """API endpoint for investment plan"""
    data = analyzer.generate_investment_plan()
    
    return jsonify({
        'proposed_genres': data['proposed_genres'].to_dict(),
        'content_type_mix': data['content_type_mix'].to_dict(),
        'geographic_focus': data['geographic_focus'].to_dict(),
        'rating_mix': data['rating_mix'].to_dict()
    })

@app.route('/api/insights')
def get_insights():
    """API endpoint for key insights"""
    insights = analyzer.generate_key_insights()
    return jsonify({'insights': insights})

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" "*15 + "NETFLIX DASHBOARD WEB APPLICATION")
    print("="*70)
    print("\n🌐 Starting Flask server...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
