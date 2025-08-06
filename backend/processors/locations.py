from db.queries import get_all_locations

def get_locations_processor():
    """
    Fetch and transform location data.
    
    Returns:
        dict: Response with location data.
    """
    results = get_all_locations()
    data = []
    for loc in results:
        data.append({
            "id": loc.get("location_id", "NA"),
            "name": loc.get("country_name", "NA"),  # Using country_name as the primary name
            "latitude": loc.get("latitude", "NA"),
            "longitude": loc.get("longitude", "NA")
        })
    
    return {
        "data": data
    }