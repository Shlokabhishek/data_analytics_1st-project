"""
Create Excel files for Power BI Dashboard
Generates multiple Excel files with different data perspectives for Power BI analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# Create output directory if it doesn't exist
output_dir = "powerbi_data"
os.makedirs(output_dir, exist_ok=True)

# Load the Netflix dataset
print("Loading Netflix dataset...")
df = pd.read_csv('netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Clean and prepare data
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['quarter_added'] = df['date_added'].dt.quarter
df['day_of_week_added'] = df['date_added'].dt.day_name()

# Extract duration value and type
df['duration_value'] = df['duration'].str.extract('(\d+)').astype(float)
df['duration_type'] = df['duration'].str.extract('(min|Season)')

print("✓ Data loaded and cleaned")

# =============================================================================
# FILE 1: Netflix_Content_Strategy_Dashboard.xlsx
# =============================================================================
print("\nCreating Netflix_Content_Strategy_Dashboard.xlsx...")

with pd.ExcelWriter(os.path.join(output_dir, 'Netflix_Content_Strategy_Dashboard.xlsx'), 
                    engine='openpyxl') as writer:
    
    # Sheet 1: Executive Summary
    summary_data = {
        'Metric': [
            'Total Titles',
            'Total Movies',
            'Total TV Shows',
            'Countries Represented',
            'Content Genres',
            'Earliest Release Year',
            'Latest Release Year',
            'Content Age Range (Years)',
            'Average Movie Duration (min)',
            'Average TV Show Seasons'
        ],
        'Value': [
            len(df),
            len(df[df['type'] == 'Movie']),
            len(df[df['type'] == 'TV Show']),
            len(df['country'].dropna().str.split(', ').explode().unique()),
            len(df['listed_in'].dropna().str.split(', ').explode().unique()),
            int(df['release_year'].min()),
            int(df['release_year'].max()),
            int(df['release_year'].max() - df['release_year'].min()),
            round(df[df['type'] == 'Movie']['duration_value'].mean(), 1),
            round(df[df['type'] == 'TV Show']['duration_value'].mean(), 1)
        ],
        'Notes': [
            'All content in catalog',
            'Feature films',
            'Series content',
            'Global reach',
            'Content diversity',
            'Oldest content',
            'Newest content',
            'Content span',
            'Typical movie length',
            'Typical series length'
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
    
    # Sheet 2: Content by Year
    content_by_year = df.groupby(['release_year', 'type']).size().unstack(fill_value=0)
    content_by_year['Total'] = content_by_year.sum(axis=1)
    content_by_year = content_by_year.sort_index(ascending=False)
    content_by_year.to_excel(writer, sheet_name='Content by Release Year')
    
    # Sheet 3: Content Added Timeline
    content_added = df[df['date_added'].notna()].groupby(['year_added', 'type']).size().unstack(fill_value=0)
    content_added['Total'] = content_added.sum(axis=1)
    content_added = content_added.sort_index(ascending=False)
    content_added.to_excel(writer, sheet_name='Content Added by Year')
    
    # Sheet 4: Top Countries
    countries = df['country'].dropna().str.split(', ').explode()
    top_countries = countries.value_counts().head(30).reset_index()
    top_countries.columns = ['Country', 'Title Count']
    top_countries.to_excel(writer, sheet_name='Top Countries', index=False)
    
    # Sheet 5: Top Genres
    genres = df['listed_in'].dropna().str.split(', ').explode()
    top_genres = genres.value_counts().head(30).reset_index()
    top_genres.columns = ['Genre', 'Title Count']
    top_genres.to_excel(writer, sheet_name='Top Genres', index=False)
    
    # Sheet 6: Rating Distribution
    rating_dist = df.groupby(['rating', 'type']).size().unstack(fill_value=0)
    rating_dist['Total'] = rating_dist.sum(axis=1)
    rating_dist = rating_dist.sort_values('Total', ascending=False)
    rating_dist.to_excel(writer, sheet_name='Rating Distribution')
    
    # Sheet 7: Monthly Additions Pattern
    monthly_pattern = df[df['date_added'].notna()].groupby(['month_added', 'type']).size().unstack(fill_value=0)
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    monthly_pattern.index = monthly_pattern.index.map(month_names)
    monthly_pattern['Total'] = monthly_pattern.sum(axis=1)
    monthly_pattern.to_excel(writer, sheet_name='Monthly Addition Pattern')
    
    # Sheet 8: Duration Analysis
    duration_analysis = pd.DataFrame({
        'Type': ['Movie', 'TV Show'],
        'Average Duration': [
            df[df['type'] == 'Movie']['duration_value'].mean(),
            df[df['type'] == 'TV Show']['duration_value'].mean()
        ],
        'Median Duration': [
            df[df['type'] == 'Movie']['duration_value'].median(),
            df[df['type'] == 'TV Show']['duration_value'].median()
        ],
        'Min Duration': [
            df[df['type'] == 'Movie']['duration_value'].min(),
            df[df['type'] == 'TV Show']['duration_value'].min()
        ],
        'Max Duration': [
            df[df['type'] == 'Movie']['duration_value'].max(),
            df[df['type'] == 'TV Show']['duration_value'].max()
        ],
        'Unit': ['Minutes', 'Seasons']
    })
    duration_analysis.to_excel(writer, sheet_name='Duration Analysis', index=False)
    
    # Sheet 9: Full Dataset
    df.to_excel(writer, sheet_name='Full Dataset', index=False)

print("✓ Netflix_Content_Strategy_Dashboard.xlsx created successfully!")

# =============================================================================
# FILE 2: Netflix_Analytics_PowerBI.xlsx
# =============================================================================
print("\nCreating Netflix_Analytics_PowerBI.xlsx...")

with pd.ExcelWriter(os.path.join(output_dir, 'Netflix_Analytics_PowerBI.xlsx'), 
                    engine='openpyxl') as writer:
    
    # Sheet 1: Time Series Analysis
    time_series = df[df['date_added'].notna()].copy()
    time_series['year_month'] = time_series['date_added'].dt.to_period('M').astype(str)
    time_series_agg = time_series.groupby(['year_month', 'type']).agg({
        'show_id': 'count',
        'duration_value': 'mean'
    }).reset_index()
    time_series_agg.columns = ['Year_Month', 'Content_Type', 'Titles_Added', 'Avg_Duration']
    time_series_agg.to_excel(writer, sheet_name='Time Series', index=False)
    
    # Sheet 2: Country Analysis
    country_expanded = df.copy()
    country_expanded = country_expanded[country_expanded['country'].notna()]
    country_data = []
    for idx, row in country_expanded.iterrows():
        countries = str(row['country']).split(', ')
        for country in countries:
            country_data.append({
                'show_id': row['show_id'],
                'title': row['title'],
                'country': country.strip(),
                'type': row['type'],
                'release_year': row['release_year'],
                'rating': row['rating']
            })
    country_df = pd.DataFrame(country_data)
    country_summary = country_df.groupby(['country', 'type']).size().unstack(fill_value=0)
    country_summary['Total'] = country_summary.sum(axis=1)
    country_summary = country_summary.sort_values('Total', ascending=False).head(50)
    country_summary.to_excel(writer, sheet_name='Country Analysis')
    
    # Sheet 3: Genre Analysis
    genre_expanded = df.copy()
    genre_expanded = genre_expanded[genre_expanded['listed_in'].notna()]
    genre_data = []
    for idx, row in genre_expanded.iterrows():
        genres = str(row['listed_in']).split(', ')
        for genre in genres:
            genre_data.append({
                'show_id': row['show_id'],
                'title': row['title'],
                'genre': genre.strip(),
                'type': row['type'],
                'release_year': row['release_year'],
                'rating': row['rating']
            })
    genre_df = pd.DataFrame(genre_data)
    genre_summary = genre_df.groupby(['genre', 'type']).size().unstack(fill_value=0)
    genre_summary['Total'] = genre_summary.sum(axis=1)
    genre_summary = genre_summary.sort_values('Total', ascending=False).head(50)
    genre_summary.to_excel(writer, sheet_name='Genre Analysis')
    
    # Sheet 4: Year-over-Year Growth
    yoy_growth = df[df['year_added'].notna()].groupby('year_added').size().reset_index()
    yoy_growth.columns = ['Year', 'Titles_Added']
    yoy_growth['YoY_Growth'] = yoy_growth['Titles_Added'].pct_change() * 100
    yoy_growth['Cumulative_Total'] = yoy_growth['Titles_Added'].cumsum()
    yoy_growth.to_excel(writer, sheet_name='YoY Growth', index=False)
    
    # Sheet 5: Content Age Analysis
    content_age = df[df['date_added'].notna()].copy()
    content_age['content_age_years'] = content_age['year_added'] - content_age['release_year']
    content_age_summary = content_age.groupby('type')['content_age_years'].describe()
    content_age_summary.to_excel(writer, sheet_name='Content Age Analysis')
    
    # Sheet 6: Rating by Type Matrix
    rating_type_matrix = pd.crosstab(df['rating'], df['type'], margins=True)
    rating_type_matrix.to_excel(writer, sheet_name='Rating Type Matrix')
    
    # Sheet 7: Top Directors
    directors = df['director'].dropna().str.split(', ').explode()
    top_directors = directors.value_counts().head(30).reset_index()
    top_directors.columns = ['Director', 'Title Count']
    top_directors.to_excel(writer, sheet_name='Top Directors', index=False)
    
    # Sheet 8: Top Cast Members
    cast = df['cast'].dropna().str.split(', ').explode()
    top_cast = cast.value_counts().head(50).reset_index()
    top_cast.columns = ['Cast Member', 'Title Count']
    top_cast.to_excel(writer, sheet_name='Top Cast', index=False)
    
    # Sheet 9: Quarterly Trends
    quarterly_data = df[df['date_added'].notna()].groupby(['year_added', 'quarter_added', 'type']).size().reset_index()
    quarterly_data.columns = ['Year', 'Quarter', 'Type', 'Count']
    quarterly_data['Year_Quarter'] = quarterly_data['Year'].astype(str) + '-Q' + quarterly_data['Quarter'].astype(str)
    quarterly_pivot = quarterly_data.pivot_table(index='Year_Quarter', columns='Type', values='Count', fill_value=0)
    quarterly_pivot['Total'] = quarterly_pivot.sum(axis=1)
    quarterly_pivot.to_excel(writer, sheet_name='Quarterly Trends')

print("✓ Netflix_Analytics_PowerBI.xlsx created successfully!")

# =============================================================================
# Summary Report
# =============================================================================
print("\n" + "="*60)
print("EXCEL FILES CREATED SUCCESSFULLY!")
print("="*60)
print(f"\n📊 File 1: Netflix_Content_Strategy_Dashboard.xlsx")
print("   Location: powerbi_data/Netflix_Content_Strategy_Dashboard.xlsx")
print("   Sheets: 9")
print("   - Executive Summary")
print("   - Content by Release Year")
print("   - Content Added by Year")
print("   - Top Countries")
print("   - Top Genres")
print("   - Rating Distribution")
print("   - Monthly Addition Pattern")
print("   - Duration Analysis")
print("   - Full Dataset")

print(f"\n📊 File 2: Netflix_Analytics_PowerBI.xlsx")
print("   Location: powerbi_data/Netflix_Analytics_PowerBI.xlsx")
print("   Sheets: 9")
print("   - Time Series")
print("   - Country Analysis")
print("   - Genre Analysis")
print("   - YoY Growth")
print("   - Content Age Analysis")
print("   - Rating Type Matrix")
print("   - Top Directors")
print("   - Top Cast")
print("   - Quarterly Trends")

print("\n" + "="*60)
print("NEXT STEPS FOR POWER BI:")
print("="*60)
print("1. Open Power BI Desktop")
print("2. Click 'Get Data' → 'Excel'")
print("3. Select one of the created Excel files")
print("4. Choose the sheets you want to import")
print("5. Create relationships between tables if needed")
print("6. Build your visualizations")
print("7. Save as .pbix file")
print("\n⚠️  Note: .pbix files can only be created using Power BI Desktop software")
print("="*60)

print(f"\n✅ All Excel files are ready for Power BI import!")
print(f"📅 Export completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
