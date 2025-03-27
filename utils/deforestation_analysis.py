import pandas as pd
import numpy as np
from PIL import Image, ImageStat
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_forest_coverage(image):
    """
    Calculate approximate forest coverage from an image based on green channel dominance.
    
    Parameters:
    -----------
    image : PIL.Image
        The image to analyze
    
    Returns:
    --------
    float
        Percentage of forest coverage (0-100)
    """
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Simple approach: areas where green channel is dominant are likely forest
    # This is a simplified approach and would be more sophisticated in a real system
    is_green_dominant = (img_array[:,:,1] > img_array[:,:,0]) & (img_array[:,:,1] > img_array[:,:,2])
    is_green_significant = img_array[:,:,1] > 100
    
    # Combine conditions
    is_forest = is_green_dominant & is_green_significant
    
    # Calculate percentage
    forest_percentage = np.mean(is_forest) * 100
    
    return forest_percentage

def calculate_detailed_deforestation_metrics(before_image, after_image, time_difference_years=1):
    """
    Calculate detailed deforestation metrics between two satellite images.
    
    Parameters:
    -----------
    before_image : PIL.Image
        The earlier satellite image
    after_image : PIL.Image
        The later satellite image
    time_difference_years : float
        The time difference between images in years
    
    Returns:
    --------
    dict
        Dictionary containing detailed deforestation metrics
    """
    # Calculate forest coverage percentages
    before_coverage = calculate_forest_coverage(before_image)
    after_coverage = calculate_forest_coverage(after_image)
    
    # Calculate absolute change
    absolute_change = before_coverage - after_coverage
    
    # Ensure we don't divide by zero
    if before_coverage > 0:
        percentage_change = (absolute_change / before_coverage) * 100
    else:
        percentage_change = 0
    
    # Calculate annual rate
    annual_rate = percentage_change / time_difference_years
    
    # Determine severity level
    if annual_rate <= 0:
        severity = "Improving"
        severity_color = "#4CAF50"  # Green
    elif annual_rate < 0.5:
        severity = "Low"
        severity_color = "#8BC34A"  # Light Green
    elif annual_rate < 1.0:
        severity = "Moderate"
        severity_color = "#FFC107"  # Amber
    elif annual_rate < 2.0:
        severity = "High"
        severity_color = "#FF9800"  # Orange
    else:
        severity = "Critical"
        severity_color = "#F44336"  # Red
    
    # Calculate carbon impact (simplified)
    # Average tropical forest stores about 250 tons of carbon per hectare
    estimated_area_hectares = 100  # This would be calculated from image metadata in a real system
    carbon_impact_tons = (absolute_change / 100) * estimated_area_hectares * 250
    
    # Calculate biodiversity impact score (simplified)
    # Higher score means more biodiversity loss
    biodiversity_impact = min(10, absolute_change / 10)
    
    return {
        "before_coverage": before_coverage,
        "after_coverage": after_coverage,
        "absolute_change": absolute_change,
        "percentage_change": percentage_change,
        "annual_rate": annual_rate,
        "time_difference_years": time_difference_years,
        "severity": severity,
        "severity_color": severity_color,
        "carbon_impact_tons": carbon_impact_tons,
        "biodiversity_impact": biodiversity_impact,
        "estimated_area_hectares": estimated_area_hectares
    }

def compare_to_global_regions(deforestation_rate):
    """
    Compare the deforestation rate to global regions.
    
    Parameters:
    -----------
    deforestation_rate : float
        The annual deforestation rate to compare
    
    Returns:
    --------
    dict
        Dictionary with comparison results
    """
    # Global reference rates
    region_rates = {
        "Amazon": 0.9,
        "Borneo": 1.3,
        "Congo": 0.3,
        "Global Average": 0.5
    }
    
    comparisons = {}
    for region, rate in region_rates.items():
        if deforestation_rate < rate:
            comparisons[region] = {
                "relation": "lower than",
                "difference": rate - deforestation_rate,
                "color": "#4CAF50"  # Green
            }
        elif deforestation_rate > rate:
            comparisons[region] = {
                "relation": "higher than",
                "difference": deforestation_rate - rate,
                "color": "#F44336"  # Red
            }
        else:
            comparisons[region] = {
                "relation": "equal to",
                "difference": 0,
                "color": "#FFC107"  # Amber
            }
    
    return comparisons

def get_historical_weather_data(location, start_date, end_date):
    """
    Generate simulated historical weather data for the given location and time period.
    
    Parameters:
    -----------
    location : str
        Name of the location
    start_date : datetime
        Start date of the weather data
    end_date : datetime
        End date of the weather data
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with simulated weather data
    """
    # Set a seed for reproducible random data
    np.random.seed(hash(location) % 2**32)
    
    # Generate dates for the time period
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Base values for different regions
    if "Amazon" in location:
        base_temp = 27
        base_rain = 200
        seasonality = 20
    elif "Borneo" in location:
        base_temp = 28
        base_rain = 220
        seasonality = 100
    elif "Congo" in location:
        base_temp = 25
        base_rain = 150
        seasonality = 80
    else:
        base_temp = 22
        base_rain = 120
        seasonality = 50
    
    # Generate data
    temperatures = []
    precipitation = []
    humidity = []
    
    for date in dates:
        # Seasonal component - higher in wet season, lower in dry season
        month_factor = np.sin((date.month / 12) * 2 * np.pi)
        season_temp = 3 * month_factor
        season_rain = seasonality * month_factor
        
        # Daily variation
        daily_temp_var = np.random.normal(0, 1.5)
        daily_rain_var = np.random.exponential(10)
        
        # Calculate values
        temp = base_temp + season_temp + daily_temp_var
        rain = max(0, base_rain + season_rain + daily_rain_var)
        humid = min(100, max(40, 70 + 20 * month_factor + np.random.normal(0, 5)))
        
        temperatures.append(temp)
        precipitation.append(rain)
        humidity.append(humid)
    
    # Create DataFrame
    weather_data = pd.DataFrame({
        'date': dates,
        'temperature': temperatures,
        'precipitation': precipitation,
        'humidity': humidity
    })
    
    return weather_data

def analyze_weather_impact(location, time_difference_years):
    """
    Analyze the potential impact of weather patterns on deforestation.
    
    Parameters:
    -----------
    location : str
        Name of the location
    time_difference_years : float
        Number of years between the before and after images
    
    Returns:
    --------
    dict
        Dictionary with weather impact analysis
    """
    # Generate end date (present)
    end_date = datetime.now()
    
    # Generate start date based on time difference
    start_date = end_date - timedelta(days=int(time_difference_years * 365))
    
    # Get weather data
    weather_data = get_historical_weather_data(location, start_date, end_date)
    
    # Calculate metrics
    avg_temp = weather_data['temperature'].mean()
    total_precipitation = weather_data['precipitation'].sum()
    avg_monthly_precipitation = total_precipitation / (time_difference_years * 12)
    
    # Determine if there were drought conditions
    # This is a simplified approach
    monthly_precip = []
    current_month = start_date.month
    current_year = start_date.year
    monthly_sum = 0
    drought_months = 0
    
    for idx, row in weather_data.iterrows():
        if row['date'].month == current_month and row['date'].year == current_year:
            monthly_sum += row['precipitation']
        else:
            monthly_precip.append(monthly_sum)
            if monthly_sum < 100:  # Simplified drought threshold
                drought_months += 1
            monthly_sum = row['precipitation']
            current_month = row['date'].month
            current_year = row['date'].year
    
    # Add the last month
    monthly_precip.append(monthly_sum)
    if monthly_sum < 100:
        drought_months += 1
    
    # Calculate reference values for comparison
    if "Amazon" in location:
        reference_temp = 27
        reference_precip = 2400
    elif "Borneo" in location:
        reference_temp = 28
        reference_precip = 2600
    elif "Congo" in location:
        reference_temp = 25
        reference_precip = 1800
    else:
        reference_temp = 22
        reference_precip = 1500
    
    # Calculate anomalies
    temp_anomaly = avg_temp - reference_temp
    precip_anomaly_pct = ((total_precipitation / time_difference_years) - reference_precip) / reference_precip * 100
    
    # Determine impact factors
    impact_factors = []
    impact_level = "Low"
    
    if temp_anomaly > 1.0:
        impact_factors.append("Higher temperatures (+{:.1f}°C)".format(temp_anomaly))
        impact_level = "Moderate"
    
    if precip_anomaly_pct < -15:
        impact_factors.append("Significant precipitation deficit ({:.1f}%)".format(precip_anomaly_pct))
        impact_level = "High"
    
    if drought_months > 3:
        impact_factors.append("Extended drought periods ({} months)".format(drought_months))
        impact_level = "High"
    
    if not impact_factors:
        impact_factors.append("No significant weather anomalies detected")
    
    # Create recommendation based on weather patterns
    if impact_level == "High":
        recommendation = "Implement drought-resistant reforestation and enhanced fire prevention"
    elif impact_level == "Moderate":
        recommendation = "Monitor for increased fire risk and adapt planting schedules"
    else:
        recommendation = "Standard conservation practices should be effective"
    
    # Create plots and visualization data
    monthly_avg_temp = weather_data.groupby(weather_data['date'].dt.to_period("M")).agg({
        'temperature': 'mean',
        'precipitation': 'sum'
    }).reset_index()
    monthly_avg_temp['date'] = monthly_avg_temp['date'].dt.to_timestamp()
    
    return {
        "average_temperature": avg_temp,
        "temperature_anomaly": temp_anomaly,
        "total_precipitation": total_precipitation,
        "precipitation_anomaly_percent": precip_anomaly_pct,
        "drought_months": drought_months,
        "weather_impact_level": impact_level,
        "impact_factors": impact_factors,
        "recommendation": recommendation,
        "weather_data": weather_data,
        "monthly_data": monthly_avg_temp
    }

def create_weather_plots(weather_impact):
    """
    Create weather visualization plots.
    
    Parameters:
    -----------
    weather_impact : dict
        Dictionary with weather impact analysis
    
    Returns:
    --------
    dict
        Dictionary containing plotly figures
    """
    # Monthly temperature plot
    temp_fig = px.line(
        weather_impact["monthly_data"], 
        x='date', 
        y='temperature',
        title='Monthly Average Temperature',
        labels={'date': 'Date', 'temperature': 'Temperature (°C)'}
    )
    temp_fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        title_font=dict(size=16),
        hovermode="x unified"
    )
    
    # Monthly precipitation plot
    precip_fig = px.bar(
        weather_impact["monthly_data"], 
        x='date', 
        y='precipitation',
        title='Monthly Precipitation',
        labels={'date': 'Date', 'precipitation': 'Precipitation (mm)'}
    )
    precip_fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        title_font=dict(size=16),
        hovermode="x unified"
    )
    
    return {
        "temperature_plot": temp_fig,
        "precipitation_plot": precip_fig
    }

def create_deforestation_projection(metrics, years_to_project=10):
    """
    Create a projection of future deforestation trends.
    
    Parameters:
    -----------
    metrics : dict
        Dictionary with deforestation metrics
    years_to_project : int
        Number of years to project into the future
    
    Returns:
    --------
    dict
        Dictionary with projection data and plots
    """
    # Start with current forest coverage
    current_coverage = metrics["after_coverage"]
    annual_rate = metrics["annual_rate"]
    
    # Project years
    years = list(range(datetime.now().year, datetime.now().year + years_to_project + 1))
    
    # Create 3 scenarios
    scenarios = {
        "Current Trend": annual_rate,
        "Improved Conservation (50% reduction)": annual_rate * 0.5,
        "Accelerated Loss (50% increase)": annual_rate * 1.5
    }
    
    projection_data = {}
    for scenario, rate in scenarios.items():
        coverage_values = [current_coverage]
        for i in range(years_to_project):
            next_coverage = coverage_values[-1] * (1 - rate/100)
            coverage_values.append(next_coverage)
        projection_data[scenario] = coverage_values
    
    # Create projection plot
    projection_df = pd.DataFrame({
        'Year': years
    })
    
    for scenario, values in projection_data.items():
        projection_df[scenario] = values
    
    # Convert to long format for plotting
    projection_df_long = pd.melt(
        projection_df, 
        id_vars=['Year'], 
        value_vars=list(scenarios.keys()),
        var_name='Scenario', 
        value_name='Forest Coverage (%)'
    )
    
    # Create plot
    projection_fig = px.line(
        projection_df_long, 
        x='Year', 
        y='Forest Coverage (%)', 
        color='Scenario',
        title='Projected Forest Coverage'
    )
    projection_fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        title_font=dict(size=16),
        hovermode="x unified"
    )
    
    # Calculate critical metrics
    years_to_50_percent = None
    if annual_rate > 0:
        years_to_50_percent = int(50 / annual_rate)
    
    return {
        "projection_data": projection_df,
        "projection_plot": projection_fig,
        "years_to_50_percent": years_to_50_percent
    }