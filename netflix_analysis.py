"""
Netflix Content Strategy Dashboard - Data Analysis Script
Author: Data Analytics Project
Date: February 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set styling
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class NetflixAnalyzer:
    def __init__(self, csv_path):
        """Initialize the analyzer with the dataset"""
        self.df = pd.read_csv(csv_path)
        self.df['date_added'] = pd.to_datetime(self.df['date_added'], errors='coerce')
        self.clean_data()
        
    def clean_data(self):
        """Clean and prepare the dataset"""
        # Extract year and month from date_added
        self.df['year_added'] = self.df['date_added'].dt.year
        self.df['month_added'] = self.df['date_added'].dt.month
        
        # Clean duration column
        self.df['duration_value'] = self.df['duration'].str.extract('(\d+)').astype(float)
        self.df['duration_type'] = self.df['duration'].str.extract('(min|Season)')
        
        # Split genres
        self.df['genres_list'] = self.df['listed_in'].str.split(', ')
        
        # Split countries
        self.df['countries_list'] = self.df['country'].str.split(', ')
        
        print(f"✓ Dataset loaded: {len(self.df)} titles")
        print(f"✓ Date range: {self.df['release_year'].min()} - {self.df['release_year'].max()}")
        
    def get_summary_stats(self):
        """Generate summary statistics"""
        stats = {
            'total_titles': len(self.df),
            'movies': len(self.df[self.df['type'] == 'Movie']),
            'tv_shows': len(self.df[self.df['type'] == 'TV Show']),
            'countries': self.df['country'].nunique(),
            'genres': self.df['listed_in'].nunique(),
            'ratings': self.df['rating'].nunique(),
            'directors': self.df['director'].nunique(),
            'avg_movie_duration': self.df[self.df['type'] == 'Movie']['duration_value'].mean(),
            'date_range': f"{self.df['release_year'].min()} to {self.df['release_year'].max()}"
        }
        return stats
    
    def analyze_content_distribution(self):
        """Page 1: Content Distribution Intelligence"""
        print("\n" + "="*50)
        print("PAGE 1: CONTENT DISTRIBUTION INTELLIGENCE")
        print("="*50)
        
        # Movies vs TV Shows
        type_dist = self.df['type'].value_counts()
        print(f"\n📊 Movies vs TV Shows:")
        print(type_dist)
        print(f"Movies: {type_dist['Movie']/len(self.df)*100:.2f}%")
        print(f"TV Shows: {type_dist['TV Show']/len(self.df)*100:.2f}%")
        
        # Genre distribution
        all_genres = [genre for genres in self.df['genres_list'].dropna() for genre in genres]
        genre_counts = pd.Series(all_genres).value_counts().head(15)
        print(f"\n🎭 Top 15 Genres:")
        print(genre_counts)
        
        # Country production share
        all_countries = [country.strip() for countries in self.df['countries_list'].dropna() 
                        for country in countries]
        country_counts = pd.Series(all_countries).value_counts().head(15)
        print(f"\n🌍 Top 15 Producing Countries:")
        print(country_counts)
        
        return {
            'type_distribution': type_dist,
            'genre_distribution': genre_counts,
            'country_distribution': country_counts
        }
    
    def analyze_content_lifecycle(self):
        """Page 2: Content Lifecycle Trends"""
        print("\n" + "="*50)
        print("PAGE 2: CONTENT LIFECYCLE TRENDS")
        print("="*50)
        
        # Release year trend
        yearly_releases = self.df.groupby(['release_year', 'type']).size().unstack(fill_value=0)
        print(f"\n📅 Content by Release Year (Last 10 years):")
        print(yearly_releases.tail(10))
        
        # Duration analysis
        movie_durations = self.df[self.df['type'] == 'Movie']['duration_value'].describe()
        tv_seasons = self.df[self.df['type'] == 'TV Show']['duration_value'].describe()
        
        print(f"\n⏱️ Movie Duration Statistics (minutes):")
        print(movie_durations)
        
        print(f"\n📺 TV Show Season Statistics:")
        print(tv_seasons)
        
        # Rating distribution
        rating_dist = self.df['rating'].value_counts()
        print(f"\n🔞 Rating Distribution:")
        print(rating_dist.head(10))
        
        return {
            'yearly_releases': yearly_releases,
            'movie_durations': movie_durations,
            'tv_seasons': tv_seasons,
            'rating_distribution': rating_dist
        }
    
    def analyze_saturation_opportunity(self):
        """Page 3: Saturation & Opportunity Analysis"""
        print("\n" + "="*50)
        print("PAGE 3: SATURATION & OPPORTUNITY ANALYSIS")
        print("="*50)
        
        # Genre saturation
        all_genres = [genre for genres in self.df['genres_list'].dropna() for genre in genres]
        genre_counts = pd.Series(all_genres).value_counts()
        
        total = len(genre_counts)
        oversaturated = genre_counts.head(5)
        underserved = genre_counts.tail(10)
        
        print(f"\n🔴 OVERSATURATED GENRES (High Competition):")
        for genre, count in oversaturated.items():
            print(f"  {genre}: {count} titles ({count/self.df.shape[0]*100:.2f}%)")
        
        print(f"\n🟢 UNDERSERVED GENRES (Opportunity Areas):")
        for genre, count in underserved.items():
            print(f"  {genre}: {count} titles ({count/self.df.shape[0]*100:.2f}%)")
        
        # Country market opportunity
        all_countries = [country.strip() for countries in self.df['countries_list'].dropna() 
                        for country in countries]
        country_counts = pd.Series(all_countries).value_counts()
        
        emerging_markets = country_counts[country_counts < 100].tail(10)
        print(f"\n🌏 EMERGING MARKETS (Growth Potential):")
        print(emerging_markets)
        
        # Content age analysis
        current_year = 2026
        self.df['content_age'] = current_year - self.df['release_year']
        age_groups = pd.cut(self.df['content_age'], 
                           bins=[0, 2, 5, 10, 20, 100], 
                           labels=['Very Recent (0-2yr)', 'Recent (2-5yr)', 
                                  'Medium (5-10yr)', 'Old (10-20yr)', 'Classic (20yr+)'])
        
        print(f"\n📊 Content Age Distribution:")
        print(age_groups.value_counts())
        
        return {
            'oversaturated_genres': oversaturated,
            'underserved_genres': underserved,
            'emerging_markets': emerging_markets,
            'content_age_distribution': age_groups.value_counts()
        }
    
    def generate_investment_plan(self):
        """Page 4: 3-Year Investment Plan Simulation"""
        print("\n" + "="*50)
        print("PAGE 4: 3-YEAR INVESTMENT PLAN SIMULATION")
        print("="*50)
        
        # Analyze recent trends (last 3 years of data)
        recent_data = self.df[self.df['release_year'] >= 2021]
        
        # Genre mix recommendation
        all_genres = [genre for genres in recent_data['genres_list'].dropna() for genre in genres]
        recent_genres = pd.Series(all_genres).value_counts().head(10)
        
        print(f"\n💡 PROPOSED CONTENT MIX (Based on Recent Trends):")
        print(f"\n1. GENRE ALLOCATION:")
        total_proposed = 300  # Proposed titles over 3 years
        
        for i, (genre, count) in enumerate(recent_genres.head(5).items(), 1):
            allocation = int((count / len(recent_data)) * total_proposed)
            print(f"   {i}. {genre}: {allocation} titles ({allocation/total_proposed*100:.1f}%)")
        
        print(f"\n2. CONTENT TYPE MIX:")
        type_ratio = recent_data['type'].value_counts(normalize=True)
        movies_proposed = int(type_ratio.get('Movie', 0) * total_proposed)
        tv_proposed = total_proposed - movies_proposed
        print(f"   - Movies: {movies_proposed} titles ({movies_proposed/total_proposed*100:.1f}%)")
        print(f"   - TV Shows: {tv_proposed} titles ({tv_proposed/total_proposed*100:.1f}%)")
        
        print(f"\n3. GEOGRAPHIC STRATEGY:")
        all_countries = [country.strip() for countries in recent_data['countries_list'].dropna() 
                        for country in countries]
        recent_countries = pd.Series(all_countries).value_counts().head(5)
        for i, (country, count) in enumerate(recent_countries.items(), 1):
            print(f"   {i}. {country}: Focus area with proven market")
        
        print(f"\n4. RATING STRATEGY:")
        rating_mix = recent_data['rating'].value_counts(normalize=True).head(3)
        for rating, ratio in rating_mix.items():
            print(f"   - {rating}: {ratio*100:.1f}% of content")
        
        print(f"\n⚠️ RISK FACTORS:")
        print(f"   1. Market saturation in dominant genres")
        print(f"   2. Competition from other streaming platforms")
        print(f"   3. Changing viewer preferences post-pandemic")
        print(f"   4. Regional content regulations")
        print(f"   5. Production cost inflation")
        
        print(f"\n📈 DATA-BACKED REASONING:")
        print(f"   • Analysis based on {len(self.df)} titles")
        print(f"   • Recent trend data: {len(recent_data)} titles (2021-2024)")
        print(f"   • Covers {self.df['country'].nunique()} countries")
        print(f"   • Spans {self.df['release_year'].max() - self.df['release_year'].min()} years of content")
        
        return {
            'proposed_genres': recent_genres.head(5),
            'content_type_mix': type_ratio,
            'geographic_focus': recent_countries.head(5),
            'rating_mix': rating_mix
        }
    
    def generate_key_insights(self):
        """Generate 10+ key insights for the report"""
        print("\n" + "="*50)
        print("KEY INSIGHTS & FINDINGS")
        print("="*50)
        
        insights = []
        
        # Insight 1: Content type dominance
        movie_pct = (self.df['type'] == 'Movie').sum() / len(self.df) * 100
        insights.append(f"1. Movies dominate Netflix catalog at {movie_pct:.1f}%, indicating strong focus on film content")
        
        # Insight 2: Top genre
        all_genres = [genre for genres in self.df['genres_list'].dropna() for genre in genres]
        top_genre = pd.Series(all_genres).value_counts().index[0]
        insights.append(f"2. '{top_genre}' is the most prevalent genre, suggesting high audience demand")
        
        # Insight 3: Country production
        all_countries = [country.strip() for countries in self.df['countries_list'].dropna() 
                        for country in countries]
        top_country = pd.Series(all_countries).value_counts().index[0]
        top_country_count = pd.Series(all_countries).value_counts().values[0]
        insights.append(f"3. {top_country} leads production with {top_country_count} titles, showing market dominance")
        
        # Insight 4: Recent content additions
        recent_years = self.df[self.df['release_year'] >= 2020]
        insights.append(f"4. {len(recent_years)} titles ({len(recent_years)/len(self.df)*100:.1f}%) released since 2020, showing rapid expansion")
        
        # Insight 5: Movie duration
        avg_duration = self.df[self.df['type'] == 'Movie']['duration_value'].mean()
        insights.append(f"5. Average movie duration is {avg_duration:.0f} minutes, aligning with standard feature film length")
        
        # Insight 6: TV Show seasons
        avg_seasons = self.df[self.df['type'] == 'TV Show']['duration_value'].mean()
        insights.append(f"6. TV shows average {avg_seasons:.1f} seasons, indicating preference for limited series")
        
        # Insight 7: Rating distribution
        top_rating = self.df['rating'].value_counts().index[0]
        insights.append(f"7. '{top_rating}' is the most common rating, reflecting target audience demographics")
        
        # Insight 8: International content
        intl_genres = [g for g in all_genres if 'International' in g]
        insights.append(f"8. {len(intl_genres)} international genre tags, showing global content strategy")
        
        # Insight 9: Content diversity
        total_genres = len(pd.Series(all_genres).unique())
        insights.append(f"9. {total_genres} unique genres available, demonstrating high content diversity")
        
        # Insight 10: Missing data
        missing_director = self.df['director'].isna().sum()
        insights.append(f"10. {missing_director} titles lack director information ({missing_director/len(self.df)*100:.1f}%), impacting metadata quality")
        
        # Insight 11: Recent additions trend
        recent_additions = self.df[self.df['year_added'] >= 2021]
        insights.append(f"11. {len(recent_additions)} titles added since 2021, showing active catalog growth")
        
        # Insight 12: Documentary presence
        doc_count = sum(1 for g in all_genres if 'Documentaries' in g)
        insights.append(f"12. {doc_count} documentary tags suggest significant non-fiction content investment")
        
        for insight in insights:
            print(f"\n{insight}")
        
        return insights
    
    def create_visualizations(self):
        """Create all visualizations for the dashboard"""
        print("\n📊 Generating visualizations...")
        
        # Create figure directory
        import os
        if not os.path.exists('visualizations'):
            os.makedirs('visualizations')
        
        # 1. Movies vs TV Shows Pie Chart
        fig, ax = plt.subplots(figsize=(10, 6))
        type_counts = self.df['type'].value_counts()
        colors = ['#E50914', '#221f1f']
        ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        ax.set_title('Netflix Content Distribution: Movies vs TV Shows', fontsize=16, weight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('visualizations/1_content_type_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Top 15 Genres
        all_genres = [genre for genres in self.df['genres_list'].dropna() for genre in genres]
        genre_counts = pd.Series(all_genres).value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        genre_counts.plot(kind='barh', ax=ax, color='#E50914')
        ax.set_title('Top 15 Genres on Netflix', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Number of Titles', fontsize=12)
        ax.set_ylabel('Genre', fontsize=12)
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('visualizations/2_top_genres.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Top 15 Countries
        all_countries = [country.strip() for countries in self.df['countries_list'].dropna() 
                        for country in countries]
        country_counts = pd.Series(all_countries).value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        country_counts.plot(kind='barh', ax=ax, color='#564d4d')
        ax.set_title('Top 15 Content Producing Countries', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Number of Titles', fontsize=12)
        ax.set_ylabel('Country', fontsize=12)
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('visualizations/3_top_countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Release Year Trend
        yearly_data = self.df[self.df['release_year'] >= 2000].groupby(['release_year', 'type']).size().unstack(fill_value=0)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        yearly_data.plot(kind='area', ax=ax, color=['#E50914', '#221f1f'], alpha=0.7)
        ax.set_title('Content Release Trend by Year (2000-2024)', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Release Year', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.legend(title='Content Type', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/4_release_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Rating Distribution
        rating_counts = self.df['rating'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        rating_counts.plot(kind='bar', ax=ax, color='#E50914')
        ax.set_title('Content Rating Distribution', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Rating', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.set_xticklabels(rating_counts.index, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('visualizations/5_rating_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 6. Movie Duration Distribution
        movie_durations = self.df[self.df['type'] == 'Movie']['duration_value'].dropna()
        
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.hist(movie_durations, bins=30, color='#E50914', edgecolor='black', alpha=0.7)
        ax.axvline(movie_durations.mean(), color='yellow', linestyle='--', linewidth=2, label=f'Mean: {movie_durations.mean():.0f} min')
        ax.set_title('Movie Duration Distribution', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Duration (minutes)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/6_movie_duration.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. Content Age Distribution
        current_year = 2026
        self.df['content_age'] = current_year - self.df['release_year']
        age_groups = pd.cut(self.df['content_age'], 
                           bins=[0, 2, 5, 10, 20, 100], 
                           labels=['Very Recent\n(0-2yr)', 'Recent\n(2-5yr)', 
                                  'Medium\n(5-10yr)', 'Old\n(10-20yr)', 'Classic\n(20yr+)'])
        age_counts = age_groups.value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(12, 7))
        age_counts.plot(kind='bar', ax=ax, color=['#00ff00', '#90EE90', '#FFA500', '#FF6347', '#8B0000'])
        ax.set_title('Content Age Distribution', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Age Category', fontsize=12)
        ax.set_ylabel('Number of Titles', fontsize=12)
        ax.set_xticklabels(age_counts.index, rotation=0)
        plt.tight_layout()
        plt.savefig('visualizations/7_content_age.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 8. Genre Saturation Heatmap (Top genres by content type)
        top_genres = pd.Series(all_genres).value_counts().head(10).index
        genre_type_matrix = []
        for genre in top_genres:
            genre_df = self.df[self.df['listed_in'].str.contains(genre, na=False)]
            genre_type_matrix.append([
                len(genre_df[genre_df['type'] == 'Movie']),
                len(genre_df[genre_df['type'] == 'TV Show'])
            ])
        
        genre_matrix = pd.DataFrame(genre_type_matrix, 
                                   columns=['Movies', 'TV Shows'], 
                                   index=top_genres)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(genre_matrix, annot=True, fmt='d', cmap='Reds', ax=ax, cbar_kws={'label': 'Number of Titles'})
        ax.set_title('Genre Saturation: Movies vs TV Shows', fontsize=16, weight='bold', pad=20)
        ax.set_ylabel('Genre', fontsize=12)
        ax.set_xlabel('Content Type', fontsize=12)
        plt.tight_layout()
        plt.savefig('visualizations/8_genre_saturation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ All visualizations created successfully!")
        print(f"✓ Saved to 'visualizations/' folder")
        
    def export_to_excel(self, filename='Netflix_Dashboard.xlsx'):
        """Export analysis results to Excel with formatting"""
        print(f"\n📊 Exporting to Excel: {filename}")
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Summary Statistics
            stats = self.get_summary_stats()
            stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
            stats_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 2: Content Distribution
            dist_data = self.analyze_content_distribution()
            
            # Type distribution
            type_df = dist_data['type_distribution'].reset_index()
            type_df.columns = ['Content Type', 'Count']
            type_df.to_excel(writer, sheet_name='Content Distribution', index=False, startrow=0)
            
            # Genre distribution
            genre_df = dist_data['genre_distribution'].reset_index()
            genre_df.columns = ['Genre', 'Count']
            genre_df.to_excel(writer, sheet_name='Content Distribution', index=False, startrow=len(type_df)+3)
            
            # Country distribution
            country_df = dist_data['country_distribution'].reset_index()
            country_df.columns = ['Country', 'Count']
            country_df.to_excel(writer, sheet_name='Content Distribution', index=False, startrow=len(type_df)+len(genre_df)+6)
            
            # Sheet 3: Lifecycle Trends
            lifecycle_data = self.analyze_content_lifecycle()
            lifecycle_data['yearly_releases'].to_excel(writer, sheet_name='Lifecycle Trends')
            
            # Sheet 4: Rating Analysis
            rating_df = lifecycle_data['rating_distribution'].reset_index()
            rating_df.columns = ['Rating', 'Count']
            rating_df.to_excel(writer, sheet_name='Ratings', index=False)
            
            # Sheet 5: Saturation Analysis
            saturation_data = self.analyze_saturation_opportunity()
            
            # Oversaturated genres
            over_df = saturation_data['oversaturated_genres'].reset_index()
            over_df.columns = ['Genre', 'Count']
            over_df.to_excel(writer, sheet_name='Saturation Analysis', index=False, startrow=0)
            
            # Underserved genres
            under_df = saturation_data['underserved_genres'].reset_index()
            under_df.columns = ['Genre', 'Count']
            under_df.to_excel(writer, sheet_name='Saturation Analysis', index=False, startrow=len(over_df)+3)
            
            # Sheet 6: Raw Data Sample
            self.df.head(100).to_excel(writer, sheet_name='Raw Data Sample', index=False)
            
        print(f"✓ Excel file '{filename}' created successfully!")
        return filename

def main():
    """Main execution function"""
    print("=" * 70)
    print(" " * 15 + "NETFLIX CONTENT STRATEGY DASHBOARD")
    print(" " * 20 + "Data Analytics Project")
    print("=" * 70)
    
    # Initialize analyzer
    analyzer = NetflixAnalyzer('netflix_titles.csv')
    
    # Display summary statistics
    print("\n📋 SUMMARY STATISTICS:")
    stats = analyzer.get_summary_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Run all analyses
    analyzer.analyze_content_distribution()
    analyzer.analyze_content_lifecycle()
    analyzer.analyze_saturation_opportunity()
    analyzer.generate_investment_plan()
    
    # Generate key insights
    insights = analyzer.generate_key_insights()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    # Export to Excel
    analyzer.export_to_excel()
    
    print("\n" + "=" * 70)
    print("✓ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nGenerated Files:")
    print("  1. Netflix_Dashboard.xlsx - Excel dashboard with data")
    print("  2. visualizations/ - Folder with 8 chart images")
    print("\nNext Steps:")
    print("  1. Review the Excel dashboard")
    print("  2. Check visualizations in 'visualizations/' folder")
    print("  3. Run the Flask web app: python app.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
