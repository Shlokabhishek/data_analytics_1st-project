"""
Netflix Content Strategy Dashboard - Web Application
Flask-based interactive dashboard
Deployable on Vercel, Heroku, or any WSGI server
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)

# Load data
df = pd.read_csv('netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/summary')
def get_summary():
    """API endpoint for summary statistics"""
    stats = {
        'total_titles': len(df),
        'movies': len(df[df['type'] == 'Movie']),
        'tv_shows': len(df[df['type'] == 'TV Show']),
        'countries': df['country'].nunique(),
        'genres': df['listed_in'].nunique(),
        'ratings': df['rating'].nunique(),
        'directors': df['director'].nunique(),
        'date_range': f"{df['release_year'].min()} to {df['release_year'].max()}"
    }
    return jsonify(stats)

@app.route('/api/content-distribution')
def get_content_distribution():
    """API endpoint for content distribution data"""
    # Type distribution
    type_dist = df['type'].value_counts()
    
    # Genre distribution
    all_genres = [genre for genres in df['listed_in'].dropna() 
                  for genre in genres.split(', ')]
    genre_counts = pd.Series(all_genres).value_counts().head(15)
    
    # Country distribution
    all_countries = [country.strip() for countries in df['country'].dropna() 
                     for country in countries.split(', ')]
    country_counts = pd.Series(all_countries).value_counts().head(15)
    
    return jsonify({
        'type_distribution': type_dist.to_dict(),
        'genre_distribution': genre_counts.to_dict(),
        'country_distribution': country_counts.to_dict()
    })

@app.route('/api/lifecycle-trends')
def get_lifecycle_trends():
    """API endpoint for lifecycle trends"""
    # Yearly releases
    yearly_data = df.groupby(['release_year', 'type']).size().unstack(fill_value=0).tail(20)
    
    # Rating distribution
    rating_dist = df['rating'].value_counts().head(10)
    
    # Movie duration stats
    df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype(float)
    movie_durations = df[df['type'] == 'Movie']['duration_value'].describe()
    
    return jsonify({
        'yearly_releases': {
            'years': yearly_data.index.tolist(),
            'movies': yearly_data['Movie'].tolist() if 'Movie' in yearly_data.columns else [],
            'tv_shows': yearly_data['TV Show'].tolist() if 'TV Show' in yearly_data.columns else []
        },
        'rating_distribution': rating_dist.to_dict(),
        'movie_duration_stats': {
            'mean': float(movie_durations['mean']),
            'median': float(movie_durations['50%']),
            'min': float(movie_durations['min']),
            'max': float(movie_durations['max'])
        }
    })

@app.route('/api/saturation-analysis')
def get_saturation_analysis():
    """API endpoint for saturation and opportunity analysis"""
    # Genre saturation
    all_genres = [genre for genres in df['listed_in'].dropna() 
                  for genre in genres.split(', ')]
    genre_counts = pd.Series(all_genres).value_counts()
    
    oversaturated = genre_counts.head(5)
    underserved = genre_counts.tail(10)
    
    # Country markets
    all_countries = [country.strip() for countries in df['country'].dropna() 
                     for country in countries.split(', ')]
    country_counts = pd.Series(all_countries).value_counts()
    emerging_markets = country_counts[country_counts < 100].tail(10)
    
    # Content age
    current_year = 2026
    df['content_age'] = current_year - df['release_year']
    age_groups = pd.cut(df['content_age'], 
                       bins=[0, 2, 5, 10, 20, 100],
                       labels=['Very Recent (0-2yr)', 'Recent (2-5yr)',
                              'Medium (5-10yr)', 'Old (10-20yr)', 'Classic (20yr+)'])
    
    return jsonify({
        'oversaturated_genres': oversaturated.to_dict(),
        'underserved_genres': underserved.to_dict(),
        'emerging_markets': emerging_markets.to_dict(),
        'content_age_distribution': age_groups.value_counts().to_dict()
    })

@app.route('/api/investment-plan')
def get_investment_plan():
    """API endpoint for investment plan"""
    # Recent data (2021+)
    recent_data = df[df['release_year'] >= 2021]
    
    # Genre mix
    all_genres = [genre for genres in recent_data['listed_in'].dropna() 
                  for genre in genres.split(', ')]
    recent_genres = pd.Series(all_genres).value_counts().head(5)
    
    # Content type mix
    type_ratio = recent_data['type'].value_counts(normalize=True)
    
    # Geographic focus
    all_countries = [country.strip() for countries in recent_data['country'].dropna() 
                     for country in countries.split(', ')]
    recent_countries = pd.Series(all_countries).value_counts().head(5)
    
    # Rating mix
    rating_mix = recent_data['rating'].value_counts(normalize=True).head(3)
    
    return jsonify({
        'proposed_genres': recent_genres.to_dict(),
        'content_type_mix': type_ratio.to_dict(),
        'geographic_focus': recent_countries.to_dict(),
        'rating_mix': rating_mix.to_dict()
    })

@app.route('/api/insights')
def get_insights():
    """API endpoint for key insights"""
    movie_pct = (df['type'] == 'Movie').sum() / len(df) * 100
    
    all_genres = [genre for genres in df['listed_in'].dropna() 
                  for genre in genres.split(', ')]
    top_genre = pd.Series(all_genres).value_counts().index[0]
    
    insights = [
        f"1. Movies dominate Netflix catalog at {movie_pct:.1f}%, indicating strong focus on film content",
        f"2. '{top_genre}' is the most prevalent genre, suggesting high audience demand",
        f"3. Dataset spans {df['release_year'].max() - df['release_year'].min()} years of content history",
        f"4. Content from {df['country'].nunique()} countries shows global diversity",
        f"5. Recent years (2015-2021) show rapid content addition growth"
    ]
    
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
