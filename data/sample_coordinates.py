def get_coordinates_for_location(location):
    """
    Get sample coordinates for various locations.
    
    Parameters:
    -----------
    location : str
        Name of the location
        
    Returns:
    --------
    dict
        Dictionary with lat, lon, and zoom values
    """
    coordinates = {
        "Amazon Rainforest": {
            "lat": -3.4653,
            "lon": -62.2159,
            "zoom": 7
        },
        "Borneo": {
            "lat": 0.9619,
            "lon": 114.5548,
            "zoom": 7
        },
        "Congo Basin": {
            "lat": -0.7893,
            "lon": 23.6566,
            "zoom": 7
        },
        "Custom Upload": {
            "lat": 0.0,
            "lon": 0.0,
            "zoom": 2
        }
    }
    
    return coordinates.get(location, coordinates["Custom Upload"])
