from langchain.tools import tool

from src.services.calendly import Calendly

CALENDLY = Calendly()


@tool
def get_current_availability():
    """Gets current availability using the CalendlyAPI"""
    return CALENDLY.list_user_availability_schedules()


TOOLS = [get_current_availability]
