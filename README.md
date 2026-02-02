# Water Quality Dashboard

## Purpose
This Streamlit app visualizes water quality data (on Biscayne Bay) and demonstrates interactive data exploration, Plotly charts, and integration of an external API (NASA Astronomy Picture of the Day).

## App Features
- Upload your own CSV file or use the default dataset.
- Interactive filters for temperature and pH.
- Plotly scatter and line charts with titles, axes labels, and legends.
- 3D Plotly visualization of water column depth and temperature.
- NASA APOD API integration to display the Astronomy Picture of the Day.
   
## Dataset
**Source**   -
- `biscayneBay_waterquality.csv` (Biscayne Bay water quality measurements)

**Key variables** -
- **Temperature (°C)**: Water temperature measurements
- **pH**: Water acidity/alkalinity levels
- **ODO mg/L**: Dissolved oxygen concentration
- **Total Water Column (m)**: Water depth
- **Latitude/Longitude**: GPS sampling locations
- **Time**: Timestamp of measurements
- **Features**: Time series, spatial mapping, temperature-depth relationships

## User Instructions

### Local Setup
1. Clone repository: `git clone https://github.com/YOUR_USERNAME/water-quality-dashboard`
2. Install dependencies: `pip install -r requirements.txt`
3. Add NASA API key to `.env`:
NASA_API_KEY=your_key_here
4. Run: `streamlit run dashboard.py`

## AGILE Development Process
**User Stories Implemented:**
- As a scientist, I want to upload custom CSV files so I can analyze my own water quality data.
- As an analyst, I want interactive filters so I can focus on specific temperature/pH ranges.
- As a researcher, I want 2D/3D Plotly charts so I can visualize spatial-temporal patterns.
- As a user, I want clear section descriptions so I understand each visualization.

**Sprint Breakdown:**
1. **Sprint 1**: Data loading + table display (MVP)
2. **Sprint 2**: 2D Plotly charts + basic interactivity
3. **Sprint 3**: 3D visualization + advanced filters
4. **Sprint 4**: NASA APOD integration + deployment

**Continuous Integration**: Tested locally after each sprint, deployed to Streamlit Cloud for user feedback.

## Deployment Links
- **GitHub Repository**: https://github.com/AngelaNano/water-quality-dashboard
