import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card

def generate_time_series_data(location):
    """
    Generate time series data for forest cover over time.
    
    Parameters:
    -----------
    location : str
        The name of the location
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with date and forest cover percentage
    """
    # Define starting points and rate of change based on location
    if location == "Amazon Rainforest":
        start_value = 95.0
        yearly_change = -0.72
        variation = 0.25
        # Add specific known deforestation events - represented as spikes
        deforestation_events = {
            "2004-07-01": -1.2,  # Increased logging
            "2007-11-01": -1.7,  # Major agricultural expansion
            "2016-05-01": -2.1,  # Severe drought and fires
            "2019-08-01": -2.4,  # Significant policy changes
            "2022-03-01": -1.8,  # Recent acceleration
        }
    elif location == "Borneo":
        start_value = 90.0
        yearly_change = -1.1
        variation = 0.3
        # Add specific known deforestation events
        deforestation_events = {
            "2005-04-01": -2.2,  # Palm oil expansion
            "2009-09-01": -1.9,  # Timber concessions
            "2015-02-01": -2.6,  # Major fires
            "2018-06-01": -1.5,  # Industrial plantations
            "2021-11-01": -1.3,  # Recent changes
        }
    elif location == "Congo Basin":
        start_value = 92.0
        yearly_change = -0.45
        variation = 0.2
        # Add specific known deforestation events
        deforestation_events = {
            "2006-03-01": -0.8,  # Road development
            "2010-08-01": -1.1,  # Mining concessions
            "2014-05-01": -1.4,  # Agricultural expansion
            "2017-11-01": -1.2,  # Increased logging
            "2020-07-01": -0.9,  # Recent pressures
        }
    else:
        start_value = 88.0
        yearly_change = -0.85
        variation = 0.3
        deforestation_events = {}
    
    # Generate dates and forest cover values
    start_date = datetime(2000, 1, 1)
    dates = []
    forest_cover = []
    urban_expansion = []
    agricultural_expansion = []
    logging_activity = []
    
    # Generate quarterly data for 23 years (2000-2023)
    for i in range(92):  
        current_date = start_date + timedelta(days=i*90)
        date_str = current_date.strftime("%Y-%m-%d")
        dates.append(current_date)
        
        # Calculate forest cover with seasonal variation and long-term trend
        years_passed = i / 4
        seasonal_factor = 0.2 * np.sin(i * np.pi / 2)  # Seasonal variation
        random_factor = variation * np.random.randn()  # Random variation
        
        # Base trend value
        value = start_value + yearly_change * years_passed + seasonal_factor + random_factor
        
        # Apply specific deforestation events
        if date_str in deforestation_events:
            value += deforestation_events[date_str]
        
        forest_cover.append(max(0, min(100, value)))  # Ensure value is between 0 and 100
        
        # Calculate urban expansion (inverse of forest loss but not exactly)
        urban_value = min(100 - value + 5, 35)  # Cap at reasonable level
        urban_variation = 0.15 * np.random.randn()
        urban_expansion.append(urban_value + urban_variation)
        
        # Calculate agricultural expansion (correlates with forest loss)
        agri_value = min(100 - value + 10, 70)  # Higher than urban but capped
        agri_variation = 0.2 * np.random.randn()
        agricultural_expansion.append(agri_value + agri_variation)
        
        # Calculate logging activity (fluctuates more)
        log_value = min(100 - value - 5, 40)  # Lower than agriculture
        log_seasonal = 0.4 * np.sin(i * np.pi / 2)  # Stronger seasonal effect
        log_variation = 0.4 * np.random.randn()
        logging_activity.append(max(0, log_value + log_seasonal + log_variation))
    
    # Create DataFrame with all metrics
    df = pd.DataFrame({
        'date': dates,
        'forest_cover': forest_cover,
        'urban_expansion': urban_expansion,
        'agricultural_expansion': agricultural_expansion,
        'logging_activity': logging_activity
    })
    
    # Calculate statistics
    stats = {
        'total_loss': start_value - df['forest_cover'].iloc[-1],
        'avg_yearly_loss': abs(yearly_change),
        'current_coverage': df['forest_cover'].iloc[-1],
        'urban_expansion': df['urban_expansion'].iloc[-1] - df['urban_expansion'].iloc[0],
        'deforestation_rate_change': ((df['forest_cover'].iloc[-4] - df['forest_cover'].iloc[-1]) / 
                                     (df['forest_cover'].iloc[-8] - df['forest_cover'].iloc[-5])) - 1,
        'peak_loss_year': 2016 if location == "Amazon Rainforest" else (2015 if location == "Borneo" else 2014),
        'recent_trend': "Accelerating" if location == "Amazon Rainforest" else ("Stabilizing" if location == "Borneo" else "Slowing")
    }
    
    return df, stats

def time_series_analysis():
    """
    Display time series analysis of forest cover changes.
    """
    colored_header(
        label="Time Series Analysis",
        description="Comprehensive tracking of forest cover changes over time with predictive analysis",
        color_name="green-70"
    )
    
    # If no location is selected, default to Amazon Rainforest
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = "Amazon Rainforest"
    
    # Create a location selector to allow users to change the data view
    location_options = ["Amazon Rainforest", "Borneo", "Congo Basin"]
    location = st.selectbox(
        "Select region to analyze:", 
        options=location_options,
        index=location_options.index(st.session_state.selected_location)
    )
    
    # Update session state with selected location
    st.session_state.selected_location = location
    
    # Generate or retrieve time series data
    if st.session_state.time_series_data is None or location != st.session_state.prev_location:
        df, stats = generate_time_series_data(location)
        st.session_state.time_series_data = df
        st.session_state.forest_loss_stats = stats
        st.session_state.prev_location = location
    else:
        df = st.session_state.time_series_data
        stats = st.session_state.forest_loss_stats
    
    # Add a trend status based on recent data
    trend_status = stats.get('recent_trend', "Accelerating")  # Default to accelerating if not available
    
    # Display trend information with styled indicators
    st.markdown(
        f"""
        <div style="background-color: rgba(46, 125, 50, 0.05); padding: 20px; border-radius: 10px; 
                    margin-bottom: 25px; border-left: 5px solid #2e7d32;">
            <h3 style="margin-top: 0; margin-bottom: 15px; color: #2e7d32;">Deforestation Trend Analysis</h3>
            <p style="margin-bottom: 15px;">Based on data from 2000 to 2023, our analysis shows that deforestation in {location} is:</p>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 50px; margin-right: 15px; color: {'#d32f2f' if trend_status == 'Accelerating' else ('#ff9800' if trend_status == 'Stabilizing' else '#2e7d32')}">
                    {'⚠️' if trend_status == 'Accelerating' else ('⚖️' if trend_status == 'Stabilizing' else '✅')}
                </div>
                <div>
                    <h4 style="margin: 0; color: {'#d32f2f' if trend_status == 'Accelerating' else ('#ff9800' if trend_status == 'Stabilizing' else '#2e7d32')};">
                        {trend_status}
                    </h4>
                    <p>Peak deforestation rates were observed in {stats.get('peak_loss_year', 2015)}.</p>
                </div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display key metrics in improved cards
    st.markdown("### Key Forest Cover Metrics")
    
    # Create a metrics container with more attractive styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card(
            title="Total Forest Loss",
            text=f"{stats['total_loss']:.1f}%\nSince 2000",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "150px",
                    "border-radius": "10px",
                    "box-shadow": "0 6px 15px rgba(0,0,0,0.1)",
                    "background-color": "#2e7d32",
                    "transition": "transform 0.3s ease, box-shadow 0.3s ease",
                    ":hover": {
                        "transform": "translateY(-5px)",
                        "box-shadow": "0 12px 20px rgba(0,0,0,0.15)"
                    }
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                    "margin-bottom": "10px",
                    "font-weight": "500",
                },
                "text": {
                    "font-size": "28px",
                    "font-weight": "bold",
                    "color": "white",
                    "line-height": "1.2"
                }
            },
        )
    
    with col2:
        card(
            title="Annual Rate of Loss",
            text=f"{stats['avg_yearly_loss']:.2f}%\nPer year",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "150px",
                    "border-radius": "10px",
                    "box-shadow": "0 6px 15px rgba(0,0,0,0.1)",
                    "background-color": "#ff9800",
                    "transition": "transform 0.3s ease, box-shadow 0.3s ease",
                    ":hover": {
                        "transform": "translateY(-5px)",
                        "box-shadow": "0 12px 20px rgba(0,0,0,0.15)"
                    }
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                    "margin-bottom": "10px",
                    "font-weight": "500",
                },
                "text": {
                    "font-size": "28px",
                    "font-weight": "bold",
                    "color": "white",
                    "line-height": "1.2"
                }
            },
        )
    
    with col3:
        card(
            title="Current Forest Cover",
            text=f"{stats['current_coverage']:.1f}%\nRemaining",
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "150px",
                    "border-radius": "10px",
                    "box-shadow": "0 6px 15px rgba(0,0,0,0.1)",
                    "background-color": "#1976d2",
                    "transition": "transform 0.3s ease, box-shadow 0.3s ease",
                    ":hover": {
                        "transform": "translateY(-5px)",
                        "box-shadow": "0 12px 20px rgba(0,0,0,0.15)"
                    }
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                    "margin-bottom": "10px",
                    "font-weight": "500",
                },
                "text": {
                    "font-size": "28px",
                    "font-weight": "bold",
                    "color": "white",
                    "line-height": "1.2"
                }
            },
        )
    
    with col4:
        # Calculate a value to display based on the trend
        rate_change = stats.get('deforestation_rate_change', 0.1) * 100  # Convert to percentage
        trend_text = f"{abs(rate_change):.1f}%\n{'Increase' if rate_change > 0 else 'Decrease'}"
        trend_color = "#d32f2f" if rate_change > 0 else "#4caf50"
        
        card(
            title="Recent Rate Change",
            text=trend_text,
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "150px",
                    "border-radius": "10px",
                    "box-shadow": "0 6px 15px rgba(0,0,0,0.1)",
                    "background-color": trend_color,
                    "transition": "transform 0.3s ease, box-shadow 0.3s ease",
                    ":hover": {
                        "transform": "translateY(-5px)",
                        "box-shadow": "0 12px 20px rgba(0,0,0,0.15)"
                    }
                },
                "title": {
                    "color": "white",
                    "font-size": "16px",
                    "margin-bottom": "10px",
                    "font-weight": "500",
                },
                "text": {
                    "font-size": "28px",
                    "font-weight": "bold",
                    "color": "white",
                    "line-height": "1.2"
                }
            },
        )
    
    # Add a styled separator
    st.markdown("""
    <div style="height: 3px; background: linear-gradient(90deg, #2e7d32, rgba(46, 125, 50, 0.3), transparent); 
                margin: 30px 0;"></div>
    """, unsafe_allow_html=True)
    
    # Improved time range selector with tabs
    st.markdown("### Historical Forest Cover Analysis")
    
    # Create tabs for different time periods
    time_options = ["Last 5 Years", "Last 10 Years", "Last 20 Years", "All Time"]
    time_tabs = st.tabs(time_options)
    
    # Set up the data visualization in each tab
    for i, tab in enumerate(time_tabs):
        with tab:
            # Filter data based on selected time range
            end_date = df['date'].max()
            if i == 0:  # Last 5 Years
                start_date = end_date - timedelta(days=365*5)
                filtered_df = df[df['date'] >= start_date]
                period_name = "Last 5 Years"
            elif i == 1:  # Last 10 Years
                start_date = end_date - timedelta(days=365*10)
                filtered_df = df[df['date'] >= start_date]
                period_name = "Last 10 Years"
            elif i == 2:  # Last 20 Years
                start_date = end_date - timedelta(days=365*20)
                filtered_df = df[df['date'] >= start_date]
                period_name = "Last 20 Years"
            else:  # All Time
                filtered_df = df
                period_name = "2000-2023"
            
            # Create a copy with string dates for visualization
            plot_df = filtered_df.copy()
            plot_df['date_str'] = plot_df['date'].dt.strftime('%Y-%m-%d')
            
            # Two columns layout for charts
            chart_col1, chart_col2 = st.columns([2, 1])
            
            with chart_col1:
                # Create enhanced time series chart
                fig = px.line(
                    plot_df, 
                    x='date_str', 
                    y='forest_cover',
                    labels={'date_str': 'Date', 'forest_cover': 'Forest Cover (%)'},
                    title=f"Forest Cover Trends in {location} ({period_name})",
                    line_shape='spline',
                    template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
                    height=400,
                )
                
                # Improved styling
                fig.update_traces(
                    line=dict(color="#2e7d32", width=3),
                    mode='lines+markers',
                    marker=dict(
                        size=6, 
                        color="#2e7d32", 
                        line=dict(width=1, color="#ffffff")
                    )
                )
                
                # Add shaded area under line
                fig.add_traces(
                    go.Scatter(
                        x=plot_df['date_str'],
                        y=plot_df['forest_cover'],
                        mode='none',
                        fill='tozeroy',
                        fillcolor='rgba(46, 125, 50, 0.2)',
                        showlegend=False
                    )
                )
                
                # Add horizontal line for critical threshold
                fig.add_shape(
                    type="line",
                    x0=plot_df['date_str'].iloc[0],
                    x1=plot_df['date_str'].iloc[-1],
                    y0=70,  # Critical threshold
                    y1=70,
                    line=dict(color="red", width=2, dash="dash"),
                )
                
                # Add annotation for threshold
                fig.add_annotation(
                    x=plot_df['date_str'].iloc[-1],
                    y=70,
                    text="Critical Threshold",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="red",
                    arrowsize=1,
                    arrowwidth=2,
                    ax=-50,
                    ay=-30
                )
                
                # Add annotations for specific deforestation events
                if location == "Amazon Rainforest":
                    events = {
                        "2016-05-01": "Severe drought and fires",
                        "2019-08-01": "Policy changes"
                    }
                elif location == "Borneo":
                    events = {
                        "2015-02-01": "Major fires",
                        "2018-06-01": "Industrial plantations"
                    }
                else:  # Congo Basin
                    events = {
                        "2014-05-01": "Agricultural expansion",
                        "2017-11-01": "Increased logging"
                    }
                
                # Add annotations for events that are in the filtered timeframe
                for date, event in events.items():
                    if date in plot_df['date_str'].values:
                        # Find the forest cover value for this date
                        event_value = plot_df.loc[plot_df['date_str'] == date, 'forest_cover'].values[0]
                        
                        # Add annotation
                        fig.add_annotation(
                            x=date,
                            y=event_value,
                            text=event,
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor="#ff9800",
                            arrowsize=1,
                            arrowwidth=2,
                            ax=0,
                            ay=-40,
                            bordercolor="#ff9800",
                            borderwidth=2,
                            borderpad=4,
                            bgcolor="rgba(255, 255, 255, 0.8)",
                            opacity=0.8
                        )
                
                fig.update_layout(
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    font=dict(family="Arial", size=12),
                    margin=dict(l=40, r=40, t=60, b=60),
                    xaxis=dict(
                        tickfont=dict(family="Arial", size=10),
                        title_font=dict(family="Arial", size=14),
                        tickangle=-45,
                        gridcolor="rgba(230, 230, 230, 0.5)",
                        showgrid=True,
                        title=dict(text="Year", standoff=15)
                    ),
                    yaxis=dict(
                        tickfont=dict(family="Arial", size=10),
                        title_font=dict(family="Arial", size=14),
                        gridcolor="rgba(230, 230, 230, 0.5)",
                        showgrid=True,
                        title=dict(text="Forest Cover (%)", standoff=15)
                    ),
                    plot_bgcolor="rgba(255, 255, 255, 0.0)",
                    paper_bgcolor="rgba(255, 255, 255, 0.0)",
                    title=dict(
                        font=dict(size=18, family="Arial", color="#2e7d32")
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with chart_col2:
                # Calculate some period-specific statistics
                start_cover = filtered_df['forest_cover'].iloc[0]
                end_cover = filtered_df['forest_cover'].iloc[-1]
                period_loss = start_cover - end_cover
                period_loss_rate = period_loss / (len(filtered_df) / 4)  # quarterly data, so divide by 4 for years
                
                # Display period-specific stats
                st.markdown(f"#### Key Metrics ({period_name})")
                
                metrics = [
                    {"name": "Total Loss", "value": f"{period_loss:.2f}%", "desc": "Forest cover reduction", "color": "#d32f2f"},
                    {"name": "Average Rate", "value": f"{period_loss_rate:.2f}%", "desc": "Annual loss", "color": "#ff9800"},
                    {"name": "Start Coverage", "value": f"{start_cover:.2f}%", "desc": f"At beginning of period", "color": "#1976d2"},
                    {"name": "End Coverage", "value": f"{end_cover:.2f}%", "desc": f"At end of period", "color": "#2e7d32"}
                ]
                
                for metric in metrics:
                    st.markdown(
                        f"""
                        <div style="padding: 12px; border-left: 4px solid {metric['color']}; 
                                   background-color: rgba({int(metric['color'][1:3], 16)}, 
                                                         {int(metric['color'][3:5], 16)}, 
                                                         {int(metric['color'][5:7], 16)}, 0.1); 
                                   border-radius: 4px; margin-bottom: 10px;">
                            <span style="font-size: 14px;">{metric['name']}</span>
                            <div style="display: flex; align-items: baseline; justify-content: space-between;">
                                <span style="font-size: 22px; font-weight: bold; color: {metric['color']};">
                                    {metric['value']}
                                </span>
                                <span style="font-size: 12px; color: #666; font-style: italic;">
                                    {metric['desc']}
                                </span>
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Add explanation or context
                if period_name == "Last 5 Years":
                    st.markdown("""
                    <div style="background-color: rgba(46, 125, 50, 0.05); padding: 15px; 
                               border-radius: 5px; font-size: 0.9em; margin-top: 20px;">
                        <p style="margin: 0;">Recent trends are crucial indicators of current policy effectiveness 
                        and emerging threats to forest conservation.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Full width section for additional analysis
            st.markdown("#### Deeper Analysis")
            
            # Create tabs for different types of analysis
            analysis_tabs = st.tabs(["Comparative", "Annual Change", "Factors"])
            
            with analysis_tabs[0]:  # Comparative analysis
                # Create comparison chart between forest cover and other factors
                comp_df = filtered_df.copy()
                comp_df['date_str'] = comp_df['date'].dt.strftime('%Y-%m-%d')
                
                fig2 = go.Figure()
                
                # Add forest cover line
                fig2.add_trace(
                    go.Scatter(
                        x=comp_df['date_str'],
                        y=comp_df['forest_cover'],
                        name="Forest Cover",
                        line=dict(color="#2e7d32", width=3),
                        mode='lines',
                    )
                )
                
                # Add other factors
                fig2.add_trace(
                    go.Scatter(
                        x=comp_df['date_str'],
                        y=comp_df['urban_expansion'],
                        name="Urban Areas",
                        line=dict(color="#d32f2f", width=2.5),
                        mode='lines',
                    )
                )
                
                fig2.add_trace(
                    go.Scatter(
                        x=comp_df['date_str'],
                        y=comp_df['agricultural_expansion'],
                        name="Agriculture",
                        line=dict(color="#ff9800", width=2.5),
                        mode='lines',
                    )
                )
                
                fig2.add_trace(
                    go.Scatter(
                        x=comp_df['date_str'],
                        y=comp_df['logging_activity'],
                        name="Logging",
                        line=dict(color="#795548", width=2.5),
                        mode='lines',
                    )
                )
                
                # Enhance the chart appearance
                fig2.update_layout(
                    title=dict(
                        text=f"Forest Cover vs. Human Activities in {location}",
                        font=dict(size=18, family="Arial", color="#2e7d32")
                    ),
                    xaxis_title="Year",
                    yaxis_title="Percentage (%)",
                    height=400,
                    template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    font=dict(family="Arial", size=12),
                    margin=dict(l=40, r=40, t=60, b=60),
                    plot_bgcolor="rgba(255, 255, 255, 0.0)",
                    paper_bgcolor="rgba(255, 255, 255, 0.0)",
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
            with analysis_tabs[1]:  # Annual Change analysis
                # Calculate annual rate of change
                annual_data = []
                years = sorted(filtered_df['date'].dt.year.unique())
                
                for i in range(len(years)-1):
                    year1 = years[i]
                    year2 = years[i+1]
                    
                    # Get average forest cover for each year
                    cover1 = filtered_df[filtered_df['date'].dt.year == year1]['forest_cover'].mean()
                    cover2 = filtered_df[filtered_df['date'].dt.year == year2]['forest_cover'].mean()
                    
                    # Calculate rate of change
                    rate = cover1 - cover2
                    
                    annual_data.append({
                        'year': year2,
                        'rate': rate
                    })
                
                if annual_data:
                    annual_df = pd.DataFrame(annual_data)
                    
                    # Create enhanced bar chart
                    fig3 = px.bar(
                        annual_df,
                        x='year',
                        y='rate',
                        labels={'year': 'Year', 'rate': 'Annual Forest Loss (%)'},
                        title=f"Annual Rate of Forest Loss in {location}",
                        template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
                        height=400,
                        text_auto='.2f',
                    )
                    
                    # Use a custom color scale based on value intensity
                    fig3.update_traces(
                        marker_color=[
                            f'rgba({46 + int(180 * rate/max(annual_df["rate"]))}, '
                            f'{125 - int(90 * rate/max(annual_df["rate"]))}, '
                            f'{50 - int(20 * rate/max(annual_df["rate"]))}, 0.8)'
                            for rate in annual_df['rate']
                        ],
                        textposition='outside',
                        textfont=dict(size=10)
                    )
                    
                    # Add a trend line
                    fig3.add_trace(
                        go.Scatter(
                            x=annual_df['year'],
                            y=annual_df['rate'],
                            mode='lines',
                            name='Trend',
                            line=dict(color='rgba(255, 87, 34, 0.7)', width=2, dash='dot'),
                            showlegend=False
                        )
                    )
                    
                    # Enhanced styling
                    fig3.update_layout(
                        title_font=dict(size=18, family="Arial", color="#2e7d32"),
                        font=dict(family="Arial"),
                        margin=dict(l=40, r=40, t=60, b=60),
                        plot_bgcolor="rgba(255, 255, 255, 0.0)",
                        paper_bgcolor="rgba(255, 255, 255, 0.0)",
                        xaxis=dict(
                            tickfont=dict(family="Arial", size=10),
                            title_font=dict(family="Arial", size=14),
                            tickangle=-45,
                            title=dict(text="Year", standoff=15)
                        ),
                        yaxis=dict(
                            tickfont=dict(family="Arial", size=10),
                            title_font=dict(family="Arial", size=14),
                            title=dict(text="Annual Forest Loss (%)", standoff=15)
                        ),
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    # Add explanatory text
                    highest_year = annual_df.loc[annual_df['rate'].idxmax(), 'year']
                    highest_rate = annual_df['rate'].max()
                    lowest_year = annual_df.loc[annual_df['rate'].idxmin(), 'year']
                    lowest_rate = annual_df['rate'].min()
                    
                    st.markdown(f"""
                    <div style="background-color: rgba(46, 125, 50, 0.05); padding: 15px; border-radius: 5px; font-size: 0.9em;">
                        <p>🔍 <strong>Annual Change Analysis:</strong></p>
                        <ul>
                            <li>Highest annual deforestation rate: <strong>{highest_rate:.2f}%</strong> in {highest_year}</li>
                            <li>Lowest annual deforestation rate: <strong>{lowest_rate:.2f}%</strong> in {lowest_year}</li>
                            <li>Average annual loss rate over this period: <strong>{annual_df['rate'].mean():.2f}%</strong></li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with analysis_tabs[2]:  # Factors analysis
                # Create a pie chart showing deforestation drivers
                if location == "Amazon Rainforest":
                    drivers = {
                        "Agriculture": 45,
                        "Cattle Ranching": 30,
                        "Logging": 15,
                        "Mining": 5,
                        "Infrastructure": 5
                    }
                elif location == "Borneo":
                    drivers = {
                        "Palm Oil Plantations": 55,
                        "Logging": 20,
                        "Agriculture": 15,
                        "Mining": 7,
                        "Urban Development": 3
                    }
                else:  # Congo Basin
                    drivers = {
                        "Subsistence Farming": 35,
                        "Commercial Logging": 30,
                        "Fuelwood Collection": 20,
                        "Mining": 10,
                        "Infrastructure": 5
                    }
                
                # Create DataFrame for the chart
                drivers_df = pd.DataFrame({
                    'Driver': list(drivers.keys()),
                    'Percentage': list(drivers.values())
                })
                
                # Create enhanced pie chart
                fig4 = px.pie(
                    drivers_df,
                    values='Percentage',
                    names='Driver',
                    title=f'Primary Deforestation Drivers in {location}',
                    template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Greens_r,
                    hole=0.4,
                    height=400
                )
                
                # Enhance styling
                fig4.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hoverinfo='label+percent',
                    marker=dict(line=dict(color='white', width=2))
                )
                
                fig4.update_layout(
                    title_font=dict(size=18, family="Arial", color="#2e7d32"),
                    font=dict(family="Arial"),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(l=40, r=40, t=60, b=40),
                    plot_bgcolor="rgba(255, 255, 255, 0.0)",
                    paper_bgcolor="rgba(255, 255, 255, 0.0)",
                    annotations=[dict(
                        text=f"Drivers<br>Analysis",
                        x=0.5, y=0.5,
                        font_size=14,
                        font_family="Arial",
                        font_color="#2e7d32",
                        showarrow=False
                    )]
                )
                
                # Two-column layout for the drivers section
                factor_col1, factor_col2 = st.columns([3, 2])
                
                with factor_col1:
                    st.plotly_chart(fig4, use_container_width=True)
                
                with factor_col2:
                    # Display information about primary drivers
                    st.markdown("#### Primary Deforestation Drivers")
                    
                    # Create a styled table of drivers with descriptions
                    if location == "Amazon Rainforest":
                        descriptions = {
                            "Agriculture": "Clearing for soy production and other commercial crops",
                            "Cattle Ranching": "Expansion of pastureland for beef production",
                            "Logging": "Both legal and illegal timber extraction",
                            "Mining": "Gold mining operations and other mineral extraction",
                            "Infrastructure": "Road construction and hydroelectric dams"
                        }
                    elif location == "Borneo":
                        descriptions = {
                            "Palm Oil Plantations": "Clearing for industrial-scale palm oil production",
                            "Logging": "Commercial timber harvesting, often unsustainable",
                            "Agriculture": "Various cash crops including rubber and cocoa",
                            "Mining": "Coal and mineral extraction operations",
                            "Urban Development": "Expansion of cities and settlements"
                        }
                    else:  # Congo Basin
                        descriptions = {
                            "Subsistence Farming": "Small-scale agriculture by local communities",
                            "Commercial Logging": "Timber extraction by large companies",
                            "Fuelwood Collection": "Gathering wood for cooking and heating",
                            "Mining": "Extraction of minerals and precious metals",
                            "Infrastructure": "Roads, settlements and development projects"
                        }
                    
                    # Display each driver with percentage and description
                    for driver, percentage in drivers.items():
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 10px; padding: 10px; 
                                      background-color: rgba(46, 125, 50, 0.05); 
                                      border-radius: 5px;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="font-weight: bold;">{driver}</span>
                                    <span style="font-weight: bold; color: #2e7d32;">{percentage}%</span>
                                </div>
                                <div style="font-size: 0.9em; margin-top: 5px;">
                                    {descriptions[driver]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    
    # Add a styled separator
    st.markdown("""
    <div style="height: 3px; background: linear-gradient(90deg, #2e7d32, rgba(46, 125, 50, 0.3), transparent); 
                margin: 30px 0;"></div>
    """, unsafe_allow_html=True)
    
    # Future projections section
    st.markdown("### Future Projections")
    
    # Projection parameters
    projection_col1, projection_col2 = st.columns([1, 3])
    
    with projection_col1:
        projection_years = st.slider("Years to project:", 1, 30, 10, 
                                     help="Select how many years into the future to project forest cover trends")
        
        # Add scenario selection
        scenario = st.radio(
            "Select scenario:",
            ["Current Trends Continue", "Increased Protection", "Accelerated Deforestation"],
            help="Choose different policy and environmental scenarios to see their potential impact"
        )
    
    with projection_col2:
        # Get the last date and value
        last_date = df['date'].max()
        last_value = df.loc[df['date'] == last_date, 'forest_cover'].values[0]
        
        # Set scenario modifiers
        if scenario == "Current Trends Continue":
            yearly_modifier = 1.0
            description = "This scenario assumes that current deforestation rates and policies remain unchanged."
        elif scenario == "Increased Protection":
            yearly_modifier = 0.5  # Half the deforestation rate
            description = "This scenario assumes implementation of stronger protection policies and sustainable practices."
        else:  # Accelerated Deforestation
            yearly_modifier = 1.8  # 80% higher deforestation rate
            description = "This scenario assumes weakening of forest protection, increased development, and climate impacts."
        
        # Calculate projected values
        projected_dates = [last_date + timedelta(days=365*i) for i in range(1, projection_years+1)]
        
        # Use the average yearly loss rate with some randomness, modified by scenario
        yearly_loss = stats['avg_yearly_loss'] * yearly_modifier
        projected_values = []
        current_value = last_value
        
        # Add some randomness to make projection more realistic
        for _ in range(projection_years):
            random_factor = 0.2 * np.random.randn()
            adjusted_loss = yearly_loss * (1 + random_factor)
            current_value = max(0, current_value - adjusted_loss)
            projected_values.append(current_value)
        
        # Create projection DataFrame
        projection_df = pd.DataFrame({
            'date': projected_dates,
            'forest_cover': projected_values
        })
        
        # Combine historical and projected data
        combined_df = pd.concat([df, projection_df])
        
        # Convert dates to strings for plotting
        combined_df['date_str'] = combined_df['date'].dt.strftime('%Y-%m-%d')
        
        # Create the projection chart
        fig5 = go.Figure()
        
        # Add historical data
        fig5.add_trace(
            go.Scatter(
                x=df['date'].dt.strftime('%Y-%m-%d'),
                y=df['forest_cover'],
                name="Historical Data",
                line=dict(color="#2e7d32", width=3),
                mode='lines',
            )
        )
        
        # Add projection
        fig5.add_trace(
            go.Scatter(
                x=projection_df['date'].dt.strftime('%Y-%m-%d'),
                y=projection_df['forest_cover'],
                name="Projected Data",
                line=dict(
                    color="#ff9800" if scenario == "Current Trends Continue" else 
                          ("#4caf50" if scenario == "Increased Protection" else "#d32f2f"),
                    width=3, 
                    dash="dot"
                ),
                mode='lines',
            )
        )
        
        # Add vertical line at current date
        fig5.add_shape(
            type="line",
            yref="paper", y0=0, y1=1,
            xref="x", x0=last_date.strftime('%Y-%m-%d'), x1=last_date.strftime('%Y-%m-%d'),
            line=dict(color="rgba(0, 0, 0, 0.5)", width=1, dash="dash")
        )
        
        # Add annotation for current date
        fig5.add_annotation(
            x=last_date.strftime('%Y-%m-%d'),
            y=1.05,
            xref="x",
            yref="paper",
            text="Present Day",
            showarrow=False,
            xanchor="center",
            bgcolor="rgba(255, 255, 255, 0.8)",
            borderpad=4
        )
        
        # Add critical threshold line
        fig5.add_shape(
            type="line",
            x0=combined_df['date_str'].iloc[0],
            x1=combined_df['date_str'].iloc[-1],
            y0=70,  # Critical threshold
            y1=70,
            line=dict(color="red", width=2, dash="dash"),
        )
        
        # Add annotation for threshold
        fig5.add_annotation(
            x=combined_df['date_str'].iloc[-1],
            y=70,
            text="Critical Threshold",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            arrowsize=1,
            arrowwidth=2,
            ax=-50,
            ay=-30
        )
        
        # Calculate when the forest cover will reach the critical threshold
        critical_threshold = 70
        years_to_critical = None
        
        if last_value > critical_threshold and yearly_loss > 0:
            years_to_critical = (last_value - critical_threshold) / yearly_loss
        
        # Enhanced styling
        fig5.update_layout(
            title=dict(
                text=f"Forest Cover Projection for {location} - {scenario}",
                font=dict(size=18, family="Arial", color="#2e7d32")
            ),
            xaxis_title="Year",
            yaxis_title="Forest Cover (%)",
            height=400,
            template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family="Arial", size=12),
            margin=dict(l=40, r=40, t=60, b=60),
            plot_bgcolor="rgba(255, 255, 255, 0.0)",
            paper_bgcolor="rgba(255, 255, 255, 0.0)",
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # Add caption explaining the scenario
        st.markdown(
            f"""
            <div style="background-color: rgba({
                76 if scenario == "Current Trends Continue" else (
                76 if scenario == "Increased Protection" else 211)}, {
                175 if scenario == "Current Trends Continue" else (
                175 if scenario == "Increased Protection" else 47)}, {
                80 if scenario == "Current Trends Continue" else (
                80 if scenario == "Increased Protection" else 47)}, 0.1); 
                        padding: 15px; border-radius: 5px; font-size: 0.9em;">
                <p><strong>Scenario Description:</strong> {description}</p>
                {f'<p><strong>Estimated time to reach critical threshold (70%):</strong> {years_to_critical:.1f} years</p>' if years_to_critical is not None else ''}
                <p><strong>Projected forest cover after {projection_years} years:</strong> {projected_values[-1]:.2f}%</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Add timestamp for the analysis
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: right; color: #888; font-size: 0.8em; 
                   margin-top: 20px; font-style: italic;">
            Time series analysis generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Future projection
    st.subheader("Future Projection")
    
    # Add projection years selector
    projection_years = st.slider("Years to project into the future", 1, 20, 10)
    
    # Get the last date and value
    last_date = df['date'].max()
    last_value = df.loc[df['date'] == last_date, 'forest_cover'].values[0]
    
    # Calculate projected values
    projected_dates = [last_date + timedelta(days=365*i) for i in range(1, projection_years+1)]
    
    # Use the average yearly loss rate with some randomness
    yearly_loss = stats['avg_yearly_loss']
    projected_values = []
    current_value = last_value
    
    for _ in range(projection_years):
        # Add some randomness to the yearly loss
        random_factor = 0.2 * np.random.randn()
        adjusted_loss = yearly_loss * (1 + random_factor)
        
        # Calculate new value
        current_value = max(0, current_value - adjusted_loss)
        projected_values.append(current_value)
    
    # Create projection DataFrame
    projection_df = pd.DataFrame({
        'date': projected_dates,
        'forest_cover': projected_values
    })
    
    # Combine historical and projected data
    combined_df = pd.concat([df, projection_df])
    
    # Create the projection chart
    fig4 = go.Figure()
    
    # Add historical data - convert dates to strings to avoid timestamp arithmetic issues
    fig4.add_trace(
        go.Scatter(
            x=df['date'].dt.strftime('%Y-%m-%d'),
            y=df['forest_cover'],
            name="Historical Data",
            line=dict(color="#2e7d32", width=3),
            mode='lines',
        )
    )
    
    # Add projection - convert dates to strings to avoid timestamp arithmetic issues
    fig4.add_trace(
        go.Scatter(
            x=projection_df['date'].dt.strftime('%Y-%m-%d'),
            y=projection_df['forest_cover'],
            name="Projected Data",
            line=dict(color="#ff9800", width=3, dash="dot"),
            mode='lines',
        )
    )
    
    # Instead of using add_vline (which has issues with string dates), 
    # let's add a vertical line as a shape
    fig4.update_layout(
        shapes=[
            dict(
                type="line",
                yref="paper", y0=0, y1=1,
                xref="x", x0=last_date.strftime('%Y-%m-%d'), x1=last_date.strftime('%Y-%m-%d'),
                line=dict(color="rgba(0, 0, 0, 0.5)", width=1, dash="dash")
            )
        ],
        annotations=[
            dict(
                x=last_date.strftime('%Y-%m-%d'),
                y=1.0,
                xref="x",
                yref="paper",
                text="Current",
                showarrow=False,
                xanchor="left",
                bgcolor="rgba(255, 255, 255, 0.8)",
                borderpad=4
            )
        ]
    )
    
    fig4.update_layout(
        title=f"Forest Cover Projection for {location} (Next {projection_years} Years)",
        xaxis_title="Year",
        yaxis_title="Forest Cover (%)",
        height=500,
        template="plotly_white" if st.session_state.theme == "light" else "plotly_dark",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Arial", size=12),
        margin=dict(l=40, r=40, t=60, b=60),
        plot_bgcolor="rgba(255, 255, 255, 0.0)",
        paper_bgcolor="rgba(255, 255, 255, 0.0)",
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # Calculate when forest cover might reach critical levels
    if projected_values:
        critical_threshold = 50  # Define critical threshold
        years_to_critical = None
        
        for i, value in enumerate(projected_values):
            if value <= critical_threshold:
                years_to_critical = i + 1
                break
        
        if years_to_critical:
            st.warning(f"⚠️ At the current rate of deforestation, {location} could reach a critical forest cover of {critical_threshold}% within approximately {years_to_critical} years.")
        else:
            # Calculate how long until critical threshold based on current rate
            years_to_critical = (last_value - critical_threshold) / yearly_loss
            if years_to_critical > 0:
                st.info(f"ℹ️ At the current rate of deforestation, {location} could reach a critical forest cover of {critical_threshold}% in approximately {int(years_to_critical)} years.")
            else:
                st.success(f"✅ {location} is not projected to reach critical forest cover levels within the foreseeable future.")