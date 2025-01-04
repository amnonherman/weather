from datetime import datetime
import pytz

def get_date_time_for_timezones(user_timezone, location_timezone):
    """
    Retrieve and format the date and time for the user and the specified location.
    Args:
        user_timezone (str): User's time zone.
        location_timezone (str): Target location's time zone.
    Returns:
        dict: Formatted local and location date/time strings.
    """
    try:
        # Current date and time in user's time zone
        user_time = datetime.now(pytz.timezone(user_timezone))
        formatted_user_time = user_time.strftime("%A, %B %d, %Y, %I:%M %p")

        # Current date and time in the location's time zone
        location_time = user_time.astimezone(pytz.timezone(location_timezone))
        formatted_location_time = location_time.strftime("%A, %B %d, %Y, %I:%M %p")

        return {
            "user_time": formatted_user_time,
            "location_time": formatted_location_time
        }
    except Exception as e:
        return {"error": str(e)}
