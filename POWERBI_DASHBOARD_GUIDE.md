# Power BI Dashboard Creation Guide
## Netflix Content Strategy Dashboard

### 📁 Files Created

Two comprehensive Excel files have been created in the `powerbi_data` folder:

1. **Netflix_Content_Strategy_Dashboard.xlsx** (9 sheets)
2. **Netflix_Analytics_PowerBI.xlsx** (9 sheets)

---

## 🎯 How to Create the .pbix File

### Prerequisites
- Download and install **Power BI Desktop** (free)
  - Download from: https://powerbi.microsoft.com/desktop

### Step-by-Step Instructions

#### Step 1: Import Data
1. Open Power BI Desktop
2. Click **Home** → **Get Data** → **Excel**
3. Browse to `powerbi_data/Netflix_Content_Strategy_Dashboard.xlsx`
4. Select the sheets you want to import:
   - ✅ Executive Summary
   - ✅ Content by Release Year
   - ✅ Top Countries
   - ✅ Top Genres
   - ✅ Rating Distribution
   - ✅ Full Dataset
5. Click **Load**

#### Step 2: Import Additional Data (Optional)
1. Click **Get Data** → **Excel** again
2. Select `Netflix_Analytics_PowerBI.xlsx`
3. Choose relevant sheets:
   - ✅ Time Series
   - ✅ Country Analysis
   - ✅ Genre Analysis
   - ✅ YoY Growth

#### Step 3: Create Relationships
1. Click **Model** view (on the left sidebar)
2. Create relationships between tables if needed:
   - Drag fields to connect related tables
   - Example: Connect Full Dataset → Country Analysis by country

#### Step 4: Build Visualizations

##### Page 1: Executive Dashboard
- **Card visuals** for key metrics (from Executive Summary sheet)
  - Total Titles
  - Total Movies
  - Total TV Shows
  - Countries Represented
  
- **Pie Chart**: Content Type Distribution
  - Values: Count of titles
  - Legend: Type (Movie/TV Show)
  
- **Line Chart**: Content Growth Over Time
  - Axis: Year Added
  - Values: Count of titles
  - Legend: Type

##### Page 2: Geographic Analysis
- **Map Visual**: Content by Country
  - Location: Country
  - Size: Title Count
  
- **Bar Chart**: Top 20 Countries
  - Axis: Country
  - Values: Title Count

##### Page 3: Genre Analysis
- **Treemap**: Genre Distribution
  - Group: Genre
  - Values: Title Count
  
- **Stacked Bar Chart**: Genres by Type
  - Axis: Genre
  - Values: Count
  - Legend: Type

##### Page 4: Content Trends
- **Area Chart**: Year-over-Year Growth
  - Axis: Year
  - Values: Titles Added
  
- **Column Chart**: Monthly Addition Patterns
  - Axis: Month
  - Values: Title Count

##### Page 5: Rating & Duration
- **Funnel Chart**: Rating Distribution
  - Group: Rating
  - Values: Count
  
- **Clustered Column Chart**: Average Duration by Type
  - Axis: Type
  - Values: Average Duration

#### Step 5: Add Slicers (Filters)
Add slicers to make your dashboard interactive:
1. **Type Slicer** (Movie/TV Show)
2. **Year Range Slicer**
3. **Country Slicer**
4. **Genre Slicer**
5. **Rating Slicer**

#### Step 6: Format Your Dashboard
1. Apply a **Theme**:
   - View → Themes → Choose a professional theme
   
2. Format visuals:
   - Click each visual → Format pane
   - Adjust colors, titles, labels
   - Add data labels where appropriate
   
3. Add **Text boxes** for:
   - Dashboard title: "Netflix Content Strategy Dashboard"
   - Last updated date
   - Key insights

#### Step 7: Create Measures (DAX)
Click **New Measure** and create:

```dax
Total Content = COUNTROWS('Full Dataset')

Total Movies = CALCULATE(
    COUNTROWS('Full Dataset'),
    'Full Dataset'[type] = "Movie"
)

Total TV Shows = CALCULATE(
    COUNTROWS('Full Dataset'),
    'Full Dataset'[type] = "TV Show"
)

Avg Movie Duration = 
CALCULATE(
    AVERAGE('Full Dataset'[duration_value]),
    'Full Dataset'[type] = "Movie"
)

YoY Growth % = 
VAR CurrentYear = CALCULATE(COUNT('Full Dataset'[show_id]))
VAR PreviousYear = CALCULATE(
    COUNT('Full Dataset'[show_id]),
    DATEADD('Full Dataset'[date_added], -1, YEAR)
)
RETURN
DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100
```

#### Step 8: Save Your Work
1. Click **File** → **Save As**
2. Name it: `Netflix_Content_Strategy_Dashboard.pbix`
3. Save to your `powerbi_data` folder

#### Step 9: Publish (Optional)
1. Click **File** → **Publish** → **Publish to Power BI**
2. Sign in with your Microsoft account
3. Choose a workspace
4. Share with stakeholders

---

## 📊 Recommended Dashboard Layout

### Dashboard 1: Executive Overview
```
┌────────────────────────────────────────────────┐
│  Netflix Content Strategy Dashboard - 2026    │
├───────┬───────┬───────┬───────────────────────┤
│ Total │Movies │TV Show│   Content Growth      │
│ 8,807 │ 6,131 │ 2,676 │   [Line Chart]        │
├───────┴───────┴───────┤                       │
│  Content Type Mix     │                       │
│  [Pie Chart]          │                       │
├───────────────────────┼───────────────────────┤
│  Top Countries        │  Top Genres           │
│  [Bar Chart]          │  [Treemap]            │
└───────────────────────┴───────────────────────┘
```

### Dashboard 2: Content Analysis
```
┌────────────────────────────────────────────────┐
│  Filters: [Type] [Year] [Country] [Rating]    │
├────────────────────┬───────────────────────────┤
│  Geographic Map    │  Rating Distribution      │
│  [Map Visual]      │  [Funnel Chart]           │
├────────────────────┼───────────────────────────┤
│  Monthly Trends    │  Duration Analysis        │
│  [Area Chart]      │  [Clustered Column]       │
└────────────────────┴───────────────────────────┘
```

---

## 🎨 Design Tips

1. **Color Scheme**:
   - Netflix Red: #E50914
   - Dark Background: #141414
   - White Text: #FFFFFF
   - Gray Accents: #564d4d

2. **Fonts**:
   - Titles: Segoe UI Bold, 20-24pt
   - Labels: Segoe UI, 12-14pt
   - Values: Segoe UI Bold, 16-18pt

3. **Best Practices**:
   - Keep it simple and clean
   - Use consistent colors
   - Add tooltips for detailed information
   - Include a "Last Refreshed" date
   - Test all slicers and filters

---

## 🔄 Refreshing Data

To update your dashboard with new data:
1. Update the source Excel files
2. Open your .pbix file
3. Click **Home** → **Refresh**
4. Save the updated report

---

## ❓ Troubleshooting

**Issue**: Tables won't connect
- **Solution**: Ensure common fields have the same name and data type

**Issue**: Visuals show blank
- **Solution**: Check that fields have data and relationships are correct

**Issue**: Performance is slow
- **Solution**: Reduce number of visuals per page or use filters

---

## 📚 Additional Resources

- Power BI Documentation: https://docs.microsoft.com/power-bi
- DAX Formula Reference: https://dax.guide
- Power BI Community: https://community.powerbi.com

---

**Created**: February 20, 2026
**Data Source**: Netflix Titles Dataset
**Excel Files**: Netflix_Content_Strategy_Dashboard.xlsx, Netflix_Analytics_PowerBI.xlsx
