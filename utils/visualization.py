import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_deforestation_heatmap(location):
    """
    Create a heatmap visualization showing deforestation intensity.
    
    Parameters:
    -----------
    location : str
        Name of the location
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A heatmap figure showing deforestation intensity
    """
    # Generate sample data based on location
    if location == "Amazon Rainforest":
        months = 48  # 4 years
        start_date = datetime(2019, 1, 1)
        baseline = 100
        seasonal_factor = 30  # Higher seasonal variation
        trend_factor = 0.5
        random_factor = 15
    elif location == "Borneo":
        months = 48
        start_date = datetime(2019, 1, 1)
        baseline = 150
        seasonal_factor = 20
        trend_factor = 0.8
        random_factor = 20
    elif location == "Congo Basin":
        months = 48
        start_date = datetime(2019, 1, 1)
        baseline = 70
        seasonal_factor = 15
        trend_factor = 0.3
        random_factor = 10
    else:  # Custom upload
        months = 48
        start_date = datetime(2019, 1, 1)
        baseline = 100
        seasonal_factor = 20
        trend_factor = 0.5
        random_factor = 15
    
    # Generate dates
    dates = [start_date + timedelta(days=30*i) for i in range(months)]
    
    # Generate heatmap data
    data = []
    years = sorted(list(set([date.year for date in dates])))
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for year in years:
        for month in range(1, 13):
            if datetime(year, month, 1) >= start_date and datetime(year, month, 1) < datetime.now():
                # Calculate deforestation value with seasonal pattern, trend, and randomness
                month_idx = month - 1
                time_idx = (year - start_date.year) * 12 + month - start_date.month
                
                # Seasonal component (higher in dry seasons, depends on hemisphere)
                if location in ["Amazon Rainforest", "Congo Basin"]:
                    # Southern hemisphere dry season (June-September)
                    seasonal = seasonal_factor * np.sin(np.pi * month_idx / 6)
                else:
                    # Northern hemisphere dry season (January-April)
                    seasonal = seasonal_factor * np.sin(np.pi * (month_idx + 6) / 6)
                
                # Trend component (increasing over time)
                trend = trend_factor * time_idx
                
                # Random component
                noise = random.uniform(-random_factor, random_factor)
                
                # Combined value
                value = baseline + seasonal + trend + noise
                
                # Ensure non-negative value
                value = max(0, value)
                
                data.append({
                    "Year": str(year),
                    "Month": months[month_idx],
                    "Deforestation (hectares)": value
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Pivot the data for the heatmap
    pivot_df = df.pivot(index="Month", columns="Year", values="Deforestation (hectares)")
    
    # Reorder months chronologically
    pivot_df = pivot_df.reindex(months)
    
    # Create heatmap
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Year", y="Month", color="Deforestation (hectares)"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="Reds",
        title=f"Monthly Deforestation Intensity in {location}"
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Month",
        coloraxis_colorbar=dict(
            title="Hectares"
        )
    )
    
    return fig

def create_comparison_chart(locations, metric="Deforestation Rate"):
    """
    Create a comparison chart across different locations.
    
    Parameters:
    -----------
    locations : list
        List of location names
    metric : str
        The metric to compare
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A bar chart comparing the metric across locations
    """
    # Sample data for different metrics
    metrics = {
        "Deforestation Rate": {
            "Amazon Rainforest": 0.5,
            "Borneo": 1.3,
            "Congo Basin": 0.3,
            "Southeast Asia": 0.9,
            "Central America": 0.7
        },
        "Forest Cover": {
            "Amazon Rainforest": 83,
            "Borneo": 75,
            "Congo Basin": 90,
            "Southeast Asia": 65,
            "Central America": 70
        },
        "Protected Areas": {
            "Amazon Rainforest": 25,
            "Borneo": 15,
            "Congo Basin": 20,
            "Southeast Asia": 12,
            "Central America": 18
        }
    }
    
    # Filter to only include requested locations
    data = {loc: metrics[metric][loc] for loc in locations if loc in metrics[metric]}
    
    # Create DataFrame
    df = pd.DataFrame({
        "Location": list(data.keys()),
        metric: list(data.values())
    })
    
    # Create chart
    if metric == "Deforestation Rate":
        title = "Annual Deforestation Rate Comparison (%)"
        color_scale = "Reds"  # Higher is worse
    elif metric == "Forest Cover":
        title = "Remaining Forest Cover Comparison (%)"
        color_scale = "Greens_r"  # Lower is worse
    else:  # Protected Areas
        title = "Protected Areas Comparison (%)"
        color_scale = "Blues_r"  # Lower is worse
    
    fig = px.bar(
        df,
        x="Location",
        y=metric,
        title=title,
        color=metric,
        color_continuous_scale=color_scale
    )
    
    return fig
