from langchain.tools import tool


@tool
def get_current_availability():
    """Gets current availability using the CalendlyAPI"""
    availability = {
        "Monday": "9:00AM-10:00PM",
        "Tuesday": "9:00AM-10:00PM"
    }
    return availability


TOOLS = [get_current_availability]
