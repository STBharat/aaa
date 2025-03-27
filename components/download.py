import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO, StringIO
from datetime import datetime
import os
from streamlit_extras.colored_header import colored_header

def generate_csv_download_link(df, filename="data.csv"):
    """
    Generate a link to download the dataframe as a CSV file.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataframe to download
    filename : str
        The name of the file to download
        
    Returns:
    --------
    str
        The HTML link for the download
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    # Add styling to ensure link is visible in both light and dark mode
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 10px 0; display: inline-block;">Download CSV</a>'
    return href

def create_pdf_report(location, data, stats):
    """
    Create a PDF report for the deforestation data.
    This is a simple implementation using a BytesIO buffer.
    
    Parameters:
    -----------
    location : str
        The name of the location
    data : pandas.DataFrame
        The dataframe with forest cover data
    stats : dict
        Dictionary with deforestation statistics
        
    Returns:
    --------
    BytesIO
        BytesIO object containing PDF content
    """
    try:
        # We'll use reportlab for PDF generation
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
    except ImportError:
        st.error("ReportLab is not available. Cannot generate PDF reports.")
        return None
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    title_style = styles['Heading1']
    title_style.textColor = colors.darkgreen
    elements.append(Paragraph(f"Deforestation Analysis Report - {location}", title_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Add date
    date_style = styles['Normal']
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary statistics
    elements.append(Paragraph("Forest Cover Statistics", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create a table for the statistics
    stats_data = [
        ["Metric", "Value"],
        ["Total Forest Loss", f"{stats['total_loss']:.1f}%"],
        ["Yearly Rate of Loss", f"{stats['avg_yearly_loss']:.2f}%"],
        ["Current Forest Coverage", f"{stats['current_coverage']:.1f}%"],
        ["Urban Area Expansion", f"{stats['urban_expansion']:.1f}%"]
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.darkgreen),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Add data section
    elements.append(Paragraph("Forest Cover Time Series Data", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create a table for the data (use just the first 10 rows to keep PDF compact)
    data_subset = data.head(10).copy()
    data_subset['date'] = data_subset['date'].dt.strftime('%Y-%m-%d')
    data_subset['forest_cover'] = data_subset['forest_cover'].round(2)
    data_subset['urban_expansion'] = data_subset['urban_expansion'].round(2)
    
    data_table_content = [["Date", "Forest Cover (%)", "Urban Expansion (%)"]]
    for _, row in data_subset.iterrows():
        data_table_content.append([
            row['date'], 
            f"{row['forest_cover']:.2f}",
            f"{row['urban_expansion']:.2f}"
        ])
    
    data_table = Table(data_table_content, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (2, 0), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (2, 0), colors.darkgreen),
        ('ALIGN', (0, 0), (2, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (2, 0), 12),
        ('BACKGROUND', (0, 1), (2, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (2, -1), 'RIGHT')
    ]))
    
    elements.append(data_table)
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Note: The table above shows only the first 10 rows of data.", styles['Italic']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Add footer
    footer_text = """
    This report was generated by the Deforestation Detection Dashboard.
    The data presented is based on historical forest cover trends and statistical projections.
    For more information on deforestation prevention, please visit conservation organizations
    such as WWF, Greenpeace, or Rainforest Alliance.
    """
    
    footer_style = ParagraphStyle(
        'footer',
        parent=styles['Normal'],
        textColor=colors.gray,
        fontSize=8
    )
    
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Reset buffer position
    buffer.seek(0)
    
    return buffer

def generate_pdf_download_link(location, data, stats, filename="deforestation_report.pdf"):
    """
    Generate a download link for a PDF report.
    
    Parameters:
    -----------
    location : str
        The name of the location
    data : pandas.DataFrame
        The dataframe with forest cover data
    stats : dict
        Dictionary with deforestation statistics
    filename : str
        The name of the file to download
        
    Returns:
    --------
    str
        The HTML link for the download
    """
    buffer = create_pdf_report(location, data, stats)
    if buffer is None:
        return None
    
    b64 = base64.b64encode(buffer.getvalue()).decode()
    # Add styling to ensure link is visible in both light and dark mode
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="background-color: #FF5722; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 10px 0; display: inline-block;">Download PDF Report</a>'
    return href

def download_section():
    """Display download options for reports and data."""
    colored_header(
        label="Download Reports",
        description="Export data and reports for offline analysis",
        color_name="blue-70"
    )
    
    st.write("Download the deforestation analysis results for offline use.")
    
    # Get location and check if time series data is available
    location = st.session_state.selected_location if 'selected_location' in st.session_state else None
    has_data = 'time_series_data' in st.session_state and st.session_state.time_series_data is not None
    has_stats = 'forest_loss_stats' in st.session_state and st.session_state.forest_loss_stats is not None
    
    if not location or not has_data or not has_stats:
        st.info("Please go to the Time Series Analysis section first to generate data for download.")
        return
    
    data = st.session_state.time_series_data
    stats = st.session_state.forest_loss_stats
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Download Data (CSV)")
        csv_link = generate_csv_download_link(data, f"{location.replace(' ', '_')}_forest_data.csv")
        st.markdown(csv_link, unsafe_allow_html=True)
        
        with st.expander("Preview Data"):
            st.dataframe(data.head(10))
    
    with col2:
        st.subheader("Download Report (PDF)")
        try:
            # See if reportlab is installed
            import reportlab
            pdf_link = generate_pdf_download_link(location, data, stats, 
                                                 f"{location.replace(' ', '_')}_report.pdf")
            if pdf_link:
                st.markdown(pdf_link, unsafe_allow_html=True)
            else:
                st.warning("Failed to generate PDF. Try installing ReportLab.")
        except ImportError:
            st.info("PDF generation requires ReportLab. Using CSV only.")
            
    st.markdown("---")
    
    # Additional formats expander
    with st.expander("Additional Export Options"):
        st.write("Download data in other formats:")
        
        # Excel download
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Forest Cover Data', index=False)
            
            # Create a stats sheet
            stats_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
            stats_df.index.name = 'Metric'
            stats_df.to_excel(writer, sheet_name='Statistics')
            
            # Format the excel file
            workbook = writer.book
            worksheet = writer.sheets['Forest Cover Data']
            
            # Add a format for the header
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Write the column headers with the defined format
            for col_num, value in enumerate(data.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Set columns width
            worksheet.set_column('A:A', 18)
            worksheet.set_column('B:C', 15)
            
        excel_buffer.seek(0)
        b64 = base64.b64encode(excel_buffer.getvalue()).decode()
        excel_href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{location.replace(" ", "_")}_forest_data.xlsx" style="background-color: #2196F3; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 10px 0; display: inline-block;">Download Excel File</a>'
        st.markdown(excel_href, unsafe_allow_html=True)
        
        # JSON download
        json_buffer = StringIO()
        json_data = data.to_json(orient='records', date_format='iso')
        json_buffer.write(json_data)
        
        b64 = base64.b64encode(json_buffer.getvalue().encode()).decode()
        json_href = f'<a href="data:application/json;base64,{b64}" download="{location.replace(" ", "_")}_forest_data.json" style="background-color: #9C27B0; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 10px 0; display: inline-block;">Download JSON File</a>'
        st.markdown(json_href, unsafe_allow_html=True)