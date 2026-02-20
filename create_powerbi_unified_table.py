"""
Netflix Power BI Dashboard - Unified Table Generator
Creates a single denormalized table with all calculated fields for Power BI dashboards
Author: Data Analytics Project
Date: February 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# LOAD ALL DATA SOURCES
# ============================================================

print("=" * 60)
print("NETFLIX POWER BI DASHBOARD - UNIFIED TABLE GENERATOR")
print("=" * 60)

# Load fact table
fact_df = pd.read_csv('powerbi_data/fact_netflix_titles.csv')
print(f"✓ Loaded fact_netflix_titles: {len(fact_df)} rows")

# Load dimension tables
dim_country = pd.read_csv('powerbi_data/dim_country.csv')
dim_genre = pd.read_csv('powerbi_data/dim_genre.csv')
dim_rating = pd.read_csv('powerbi_data/dim_rating.csv')
dim_type = pd.read_csv('powerbi_data/dim_type.csv')
dim_date = pd.read_csv('powerbi_data/dim_date.csv')

# Load bridge tables
bridge_country = pd.read_csv('powerbi_data/bridge_title_country.csv')
bridge_genre = pd.read_csv('powerbi_data/bridge_title_genre.csv')

print(f"✓ Loaded all dimension and bridge tables")

# ============================================================
# CREATE UNIFIED TABLE
# ============================================================

print("\n" + "-" * 60)
print("CREATING UNIFIED TABLE FOR POWER BI")
print("-" * 60)

# Start with fact table as base
df = fact_df.copy()

# Convert date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# ============================================================
# PAGE 1: CONTENT DISTRIBUTION INTELLIGENCE COLUMNS
# ============================================================

print("\n📊 Adding Page 1 columns: Content Distribution Intelligence...")

# Content Type Category (for Movies vs TV Shows analysis)
df['content_type'] = df['type']
df['content_type_category'] = df['type'].map({
    'Movie': 'Film Content',
    'TV Show': 'Series Content'
})

# Primary Genre (first listed genre)
df['primary_genre'] = df['listed_in'].apply(
    lambda x: x.split(', ')[0] if pd.notna(x) else 'Unknown'
)

# Genre Count (number of genres per title)
df['genre_count'] = df['listed_in'].apply(
    lambda x: len(x.split(', ')) if pd.notna(x) else 0
)

# Primary Country (first listed country)
df['primary_country'] = df['country'].apply(
    lambda x: x.split(', ')[0] if pd.notna(x) else 'Unknown'
)

# Country Count (number of countries per title)
df['country_count'] = df['country'].apply(
    lambda x: len(x.split(', ')) if pd.notna(x) else 0
)

# Production Region Classification
def classify_region(country):
    if pd.isna(country):
        return 'Unknown'
    country = str(country).split(', ')[0]
    
    north_america = ['United States', 'Canada', 'Mexico']
    europe = ['United Kingdom', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands', 
              'Belgium', 'Sweden', 'Norway', 'Denmark', 'Poland', 'Ireland', 'Switzerland']
    asia = ['India', 'Japan', 'South Korea', 'China', 'Hong Kong', 'Taiwan', 'Thailand',
            'Philippines', 'Indonesia', 'Singapore', 'Malaysia', 'Vietnam', 'Pakistan']
    latam = ['Brazil', 'Argentina', 'Colombia', 'Chile', 'Peru', 'Uruguay']
    oceania = ['Australia', 'New Zealand']
    africa = ['South Africa', 'Nigeria', 'Egypt', 'Morocco', 'Kenya']
    mena = ['Turkey', 'Israel', 'United Arab Emirates', 'Saudi Arabia', 'Egypt', 'Lebanon']
    
    if country in north_america:
        return 'North America'
    elif country in europe:
        return 'Europe'
    elif country in asia:
        return 'Asia'
    elif country in latam:
        return 'Latin America'
    elif country in oceania:
        return 'Oceania'
    elif country in africa:
        return 'Africa'
    elif country in mena:
        return 'Middle East'
    else:
        return 'Other'

df['production_region'] = df['country'].apply(classify_region)

# ============================================================
# PAGE 2: CONTENT LIFECYCLE TRENDS COLUMNS
# ============================================================

print("📅 Adding Page 2 columns: Content Lifecycle Trends...")

# Release Year Decade
df['release_decade'] = (df['release_year'] // 10) * 10
df['release_decade_label'] = df['release_decade'].apply(lambda x: f"{x}s")

# Release Era Classification
def classify_era(year):
    if pd.isna(year):
        return 'Unknown'
    elif year < 1990:
        return 'Classic (Pre-1990)'
    elif year < 2000:
        return '1990s Golden Era'
    elif year < 2010:
        return '2000s Digital Transition'
    elif year < 2015:
        return 'Early Streaming (2010-14)'
    elif year < 2020:
        return 'Peak Streaming (2015-19)'
    else:
        return 'Modern Era (2020+)'

df['release_era'] = df['release_year'].apply(classify_era)

# Content Age (in years from 2026)
current_year = 2026
df['content_age_years'] = current_year - df['release_year']

# Content Age Category
def categorize_age(age):
    if pd.isna(age):
        return 'Unknown'
    elif age <= 1:
        return 'Brand New (0-1 yr)'
    elif age <= 3:
        return 'Recent (1-3 yrs)'
    elif age <= 5:
        return 'Fairly Recent (3-5 yrs)'
    elif age <= 10:
        return 'Established (5-10 yrs)'
    elif age <= 20:
        return 'Mature (10-20 yrs)'
    else:
        return 'Classic (20+ yrs)'

df['content_age_category'] = df['content_age_years'].apply(categorize_age)

# Duration Classification (for movies)
def classify_duration(row):
    if row['type'] != 'Movie':
        return 'N/A - TV Show'
    duration = row['duration_value']
    if pd.isna(duration):
        return 'Unknown'
    elif duration < 60:
        return 'Short (<60 min)'
    elif duration < 90:
        return 'Standard (60-90 min)'
    elif duration < 120:
        return 'Feature (90-120 min)'
    elif duration < 150:
        return 'Long (120-150 min)'
    else:
        return 'Epic (150+ min)'

df['movie_duration_category'] = df.apply(classify_duration, axis=1)

# Season Count Classification (for TV shows)
def classify_seasons(row):
    if row['type'] != 'TV Show':
        return 'N/A - Movie'
    seasons = row['duration_value']
    if pd.isna(seasons):
        return 'Unknown'
    elif seasons == 1:
        return 'Limited Series (1 season)'
    elif seasons <= 3:
        return 'Short Run (2-3 seasons)'
    elif seasons <= 6:
        return 'Medium Run (4-6 seasons)'
    else:
        return 'Long Running (7+ seasons)'

df['tv_season_category'] = df.apply(classify_seasons, axis=1)

# Rating Category (from dim_rating)
rating_map = dict(zip(dim_rating['rating_code'], dim_rating['rating_category']))
df['rating_category'] = df['rating'].map(rating_map).fillna('Other')

# Target Audience based on Rating
def classify_audience(rating):
    if pd.isna(rating):
        return 'General'
    elif rating in ['TV-Y', 'TV-Y7', 'TV-Y7-FV', 'G', 'TV-G']:
        return 'Kids & Family'
    elif rating in ['PG', 'TV-PG']:
        return 'Family'
    elif rating in ['PG-13', 'TV-14']:
        return 'Teens & Adults'
    elif rating in ['R', 'TV-MA', 'NC-17']:
        return 'Adults Only'
    else:
        return 'General'

df['target_audience'] = df['rating'].apply(classify_audience)

# ============================================================
# PAGE 3: SATURATION & OPPORTUNITY ANALYSIS COLUMNS
# ============================================================

print("📈 Adding Page 3 columns: Saturation & Opportunity Analysis...")

# Calculate genre saturation metrics
genre_counts = bridge_genre['genre_name'].value_counts()
total_titles = len(df)

def get_genre_saturation(genre):
    if pd.isna(genre):
        return 'Unknown'
    primary_genre = genre.split(', ')[0]
    count = genre_counts.get(primary_genre, 0)
    pct = count / total_titles * 100
    if pct >= 10:
        return 'Highly Saturated (10%+)'
    elif pct >= 5:
        return 'Saturated (5-10%)'
    elif pct >= 2:
        return 'Moderate (2-5%)'
    elif pct >= 1:
        return 'Emerging (1-2%)'
    else:
        return 'Niche (<1%)'

df['genre_saturation_level'] = df['listed_in'].apply(get_genre_saturation)

# Market opportunity score (inverse of saturation)
def get_opportunity_score(saturation):
    if saturation == 'Highly Saturated (10%+)':
        return 1
    elif saturation == 'Saturated (5-10%)':
        return 2
    elif saturation == 'Moderate (2-5%)':
        return 3
    elif saturation == 'Emerging (1-2%)':
        return 4
    elif saturation == 'Niche (<1%)':
        return 5
    else:
        return 0

df['genre_opportunity_score'] = df['genre_saturation_level'].apply(get_opportunity_score)

# Country market classification
country_counts = bridge_country['country_name'].value_counts()

def classify_market(country):
    if pd.isna(country):
        return 'Unknown'
    primary_country = country.split(', ')[0]
    count = country_counts.get(primary_country, 0)
    if count >= 500:
        return 'Dominant Market (500+)'
    elif count >= 100:
        return 'Major Market (100-500)'
    elif count >= 50:
        return 'Growing Market (50-100)'
    elif count >= 20:
        return 'Emerging Market (20-50)'
    else:
        return 'Untapped Market (<20)'

df['market_classification'] = df['country'].apply(classify_market)

# Investment risk score
def calculate_risk_score(row):
    """Higher score = lower risk"""
    risk = 5  # Start with base score
    
    # Saturation risk
    if row['genre_saturation_level'] == 'Highly Saturated (10%+)':
        risk -= 1
    elif row['genre_saturation_level'] == 'Niche (<1%)':
        risk -= 0.5  # Very niche can be risky too
    
    # Content age risk
    if row['content_age_years'] > 10:
        risk -= 0.5
    
    # Market size risk
    if row['market_classification'] == 'Untapped Market (<20)':
        risk -= 1
    elif row['market_classification'] == 'Dominant Market (500+)':
        risk -= 0.5  # High competition
    
    return max(1, min(5, risk))

df['investment_risk_score'] = df.apply(calculate_risk_score, axis=1)

# Risk Level Classification
def classify_risk(score):
    if score >= 4.5:
        return 'Very Low Risk'
    elif score >= 4:
        return 'Low Risk'
    elif score >= 3:
        return 'Moderate Risk'
    elif score >= 2:
        return 'High Risk'
    else:
        return 'Very High Risk'

df['investment_risk_level'] = df['investment_risk_score'].apply(classify_risk)

# Competition Index
def calculate_competition(row):
    """1 = Low competition, 5 = High competition"""
    saturation = row['genre_saturation_level']
    market = row['market_classification']
    
    sat_score = {
        'Highly Saturated (10%+)': 5,
        'Saturated (5-10%)': 4,
        'Moderate (2-5%)': 3,
        'Emerging (1-2%)': 2,
        'Niche (<1%)': 1,
        'Unknown': 3
    }.get(saturation, 3)
    
    mkt_score = {
        'Dominant Market (500+)': 5,
        'Major Market (100-500)': 4,
        'Growing Market (50-100)': 3,
        'Emerging Market (20-50)': 2,
        'Untapped Market (<20)': 1,
        'Unknown': 3
    }.get(market, 3)
    
    return (sat_score + mkt_score) / 2

df['competition_index'] = df.apply(calculate_competition, axis=1)

# ============================================================
# PAGE 4: 3-YEAR INVESTMENT PLAN COLUMNS
# ============================================================

print("💰 Adding Page 4 columns: 3-Year Investment Plan...")

# Content Performance Indicator (simulated based on various factors)
def calculate_performance_indicator(row):
    """Simulated performance score 1-100"""
    base_score = 50
    
    # Recent content bonus
    if row['content_age_years'] <= 3:
        base_score += 20
    elif row['content_age_years'] <= 5:
        base_score += 10
    
    # Popular genre bonus
    if row['genre_saturation_level'] in ['Highly Saturated (10%+)', 'Saturated (5-10%)']:
        base_score += 10
    
    # Major market bonus
    if row['market_classification'] in ['Dominant Market (500+)', 'Major Market (100-500)']:
        base_score += 10
    
    # Appropriate rating bonus
    if row['rating'] in ['TV-MA', 'TV-14', 'PG-13']:
        base_score += 5
    
    return min(100, max(0, base_score + np.random.randint(-10, 10)))

np.random.seed(42)
df['performance_indicator'] = df.apply(calculate_performance_indicator, axis=1)

# Investment Priority
def calculate_investment_priority(row):
    """Combine opportunity and risk for investment priority"""
    opportunity = row['genre_opportunity_score']
    risk_score = row['investment_risk_score']
    performance = row['performance_indicator']
    
    # Weighted priority
    priority = (opportunity * 2 + risk_score + performance / 20) / 4
    return round(priority, 2)

df['investment_priority_score'] = df.apply(calculate_investment_priority, axis=1)

# Investment Recommendation
def get_investment_recommendation(row):
    priority = row['investment_priority_score']
    if priority >= 4:
        return 'Strong Investment'
    elif priority >= 3:
        return 'Moderate Investment'
    elif priority >= 2:
        return 'Cautious Investment'
    else:
        return 'Low Priority'

df['investment_recommendation'] = df.apply(get_investment_recommendation, axis=1)

# Content Strategy Bucket
def classify_strategy(row):
    genre_sat = row['genre_saturation_level']
    market = row['market_classification']
    
    if genre_sat in ['Niche (<1%)', 'Emerging (1-2%)'] and market in ['Growing Market (50-100)', 'Emerging Market (20-50)']:
        return 'Blue Ocean (Expand)'
    elif genre_sat in ['Highly Saturated (10%+)'] and market in ['Dominant Market (500+)']:
        return 'Red Ocean (Compete)'
    elif genre_sat in ['Moderate (2-5%)'] and market in ['Growing Market (50-100)', 'Emerging Market (20-50)']:
        return 'Growth Opportunity'
    elif market in ['Untapped Market (<20)']:
        return 'Market Entry'
    else:
        return 'Maintain Position'

df['content_strategy'] = df.apply(classify_strategy, axis=1)

# Year-wise Investment Allocation (for 3-year plan)
def allocate_year(row):
    strategy = row['content_strategy']
    priority = row['investment_priority_score']
    
    if strategy == 'Blue Ocean (Expand)' or priority >= 4:
        return 'Year 1 - Immediate'
    elif strategy == 'Growth Opportunity' or priority >= 3:
        return 'Year 2 - Scale'
    else:
        return 'Year 3 - Optimize'

df['investment_year'] = df.apply(allocate_year, axis=1)

# ============================================================
# ADDITIONAL ANALYSIS COLUMNS
# ============================================================

print("🔧 Adding additional analysis columns...")

# Has Director flag
df['has_director'] = df['director'].notna().astype(int)

# Has Cast flag
df['has_cast'] = df['cast'].notna().astype(int)

# Description length
df['description_length'] = df['description'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)

# Title length
df['title_length'] = df['title'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)

# Is International Production (multi-country)
df['is_international_production'] = (df['country_count'] > 1).astype(int)

# Is Multi-Genre
df['is_multi_genre'] = (df['genre_count'] > 1).astype(int)

# Content Freshness Score (for sorting)
df['freshness_score'] = 100 - df['content_age_years'].clip(0, 100)

# ============================================================
# EXPORT UNIFIED TABLE
# ============================================================

print("\n" + "=" * 60)
print("EXPORTING UNIFIED POWER BI TABLE")
print("=" * 60)

# Select and reorder columns for Power BI
powerbi_columns = [
    # Identifiers
    'show_id', 'title', 'type', 'content_type_category',
    
    # Page 1: Content Distribution
    'primary_genre', 'genre_count', 'is_multi_genre',
    'primary_country', 'country_count', 'production_region', 'is_international_production',
    
    # Page 2: Content Lifecycle
    'release_year', 'release_decade', 'release_decade_label', 'release_era',
    'date_added', 'year_added', 'month_added', 'quarter_added',
    'content_age_years', 'content_age_category', 'freshness_score',
    'duration', 'duration_value', 'duration_type',
    'movie_duration_category', 'tv_season_category',
    'rating', 'rating_category', 'target_audience',
    
    # Page 3: Saturation & Opportunity
    'genre_saturation_level', 'genre_opportunity_score',
    'market_classification', 'competition_index',
    'investment_risk_score', 'investment_risk_level',
    
    # Page 4: Investment Plan
    'performance_indicator', 'investment_priority_score',
    'investment_recommendation', 'content_strategy', 'investment_year',
    
    # Additional metadata
    'director', 'has_director', 'cast', 'has_cast',
    'description', 'description_length', 'title_length',
    'listed_in', 'country'
]

# Create the final export dataframe
df_export = df[powerbi_columns].copy()

# Export to CSV
output_path = 'powerbi_data/netflix_unified_dashboard.csv'
df_export.to_csv(output_path, index=False)

print(f"\n✓ Unified table exported: {output_path}")
print(f"✓ Total rows: {len(df_export)}")
print(f"✓ Total columns: {len(df_export.columns)}")

# ============================================================
# CREATE SUMMARY STATISTICS FOR VERIFICATION
# ============================================================

print("\n" + "-" * 60)
print("COLUMN SUMMARY FOR POWER BI DASHBOARD")
print("-" * 60)

print("\n📊 PAGE 1 - CONTENT DISTRIBUTION INTELLIGENCE")
print(f"   Drag 'type' -> Pie chart (Movies vs TV Shows)")
print(f"   Drag 'primary_genre' -> Bar chart (Genre Share)")
print(f"   Drag 'production_region' -> Map or Donut (Country Production)")
print(f"   Drag 'primary_country' -> Table (Detailed Country View)")

print("\n📅 PAGE 2 - CONTENT LIFECYCLE TRENDS")
print(f"   Drag 'release_year' -> Line chart (Release Trend)")
print(f"   Drag 'release_era' -> Stacked bar (Era Distribution)")
print(f"   Drag 'movie_duration_category' -> Column chart (Duration Analysis)")
print(f"   Drag 'rating_category' -> Treemap (Rating Distribution)")
print(f"   Drag 'content_age_category' -> Funnel (Age Distribution)")

print("\n📈 PAGE 3 - SATURATION & OPPORTUNITY ANALYSIS")
print(f"   Drag 'genre_saturation_level' -> Matrix (Saturation View)")
print(f"   Drag 'market_classification' -> Scatter plot with 'competition_index'")
print(f"   Drag 'investment_risk_level' -> Card/KPI (Risk Overview)")
print(f"   Drag 'genre_opportunity_score' -> Gauge (Opportunity Score)")

print("\n💰 PAGE 4 - 3-YEAR INVESTMENT PLAN")
print(f"   Drag 'content_strategy' -> Ribbon chart (Strategy Mix)")
print(f"   Drag 'investment_recommendation' -> Donut (Investment Split)")
print(f"   Drag 'investment_year' -> Timeline (3-Year Plan)")
print(f"   Drag 'investment_priority_score' -> Scatter plot")
print(f"   Drag 'performance_indicator' -> Histogram (Performance Distribution)")

# ============================================================
# EDA SUMMARY STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS (EDA) SUMMARY")
print("=" * 60)

print("\n🔢 BASIC STATISTICS")
print(f"   Total Titles: {len(df_export):,}")
print(f"   Movies: {(df_export['type'] == 'Movie').sum():,} ({(df_export['type'] == 'Movie').sum() / len(df_export) * 100:.1f}%)")
print(f"   TV Shows: {(df_export['type'] == 'TV Show').sum():,} ({(df_export['type'] == 'TV Show').sum() / len(df_export) * 100:.1f}%)")

print("\n🌍 GEOGRAPHIC DISTRIBUTION")
print(df_export['production_region'].value_counts().to_string())

print("\n🎭 GENRE SATURATION")
print(df_export['genre_saturation_level'].value_counts().to_string())

print("\n📊 MARKET CLASSIFICATION")
print(df_export['market_classification'].value_counts().to_string())

print("\n⚠️ INVESTMENT RISK LEVELS")
print(df_export['investment_risk_level'].value_counts().to_string())

print("\n💡 INVESTMENT RECOMMENDATIONS")
print(df_export['investment_recommendation'].value_counts().to_string())

print("\n📅 CONTENT STRATEGY DISTRIBUTION")
print(df_export['content_strategy'].value_counts().to_string())

print("\n🎯 3-YEAR INVESTMENT ALLOCATION")
print(df_export['investment_year'].value_counts().to_string())

print("\n" + "=" * 60)
print("✅ UNIFIED TABLE GENERATION COMPLETE!")
print("=" * 60)
print(f"\nNext Steps in Power BI:")
print(f"1. Import '{output_path}'")
print(f"2. Select columns to auto-generate charts")
print(f"3. Use slicers for interactive filtering")
print(f"4. Cross-filter between visuals for insights")
