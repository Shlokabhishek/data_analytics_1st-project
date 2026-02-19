# Netflix Content Analysis Dashboard

A comprehensive data analysis project featuring both an interactive web dashboard and Excel analytics for Netflix content strategy.

## Features

- **Web Dashboard**: Interactive Flask-based web application with real-time data visualization
- **Excel Dashboard**: Professional analytics workbook with 9 comprehensive sheets
- **Data Analysis**: Deep insights into Netflix content trends, genres, and market opportunities

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Web Dashboard
```bash
python app.py
```
Visit http://localhost:5000 to view the interactive dashboard.

### 3. View Excel Dashboard
Open `Netflix_Content_Strategy_Dashboard.xlsx` in Excel.

## Deployment

### Deploy to Vercel (Free & Easy)

This app is ready for one-click deployment on Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Shlokabhishek/data_analytics_1st-project)

Or follow the [detailed deployment guide](VERCEL_DEPLOYMENT.md).

## Project Structure

```
├── app.py                    # Flask web application
├── netflix_analysis.py       # Core analysis module
├── netflix_titles.csv        # Dataset (8,807 titles)
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web dashboard UI
└── visualizations/          # Generated charts
```

## Dataset

- **Source**: Netflix titles dataset
- **Records**: 8,807 titles
- **Date Range**: 1925 - 2021
- **Geographic Coverage**: 748 countries
- **Content Types**: Movies and TV Shows

## Technologies

- Python 3.x
- Flask (Web Framework)
- Pandas (Data Analysis)
- Matplotlib & Seaborn (Visualization)
- openpyxl (Excel Integration)

## License

This project is for educational and analytical purposes.
