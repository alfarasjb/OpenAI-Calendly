import logging
from datetime import datetime as dt

import pytz
from langchain.tools import tool
from pydantic import BaseModel, Field

from src.services.calendly import Calendly

logger = logging.getLogger(__name__)

CALENDLY = Calendly()

"""
Utils
"""


def datetime_now():
    return dt.now(pytz.utc).astimezone(pytz.timezone('Asia/Singapore')).isoformat()


""" 
Args Schemas 
"""


class SetMeetingInput(BaseModel):
    meeting_start: str = Field(..., description=f"Start time of the meeting in ISO 8601 format. This must be later than {datetime_now()}")
    email_address: str = Field(..., description="Email address of the person requesting the meeting.")


class CheckConflictInput(BaseModel):
    meeting_start: str = Field(..., description=f"Start time of the meeting in ISO 8601 format. This must be later than {datetime_now()}")

""" 
Function Declarations 
"""

@tool
def get_current_availability():
    """Gets current availability using the CalendlyAPI"""
    return CALENDLY.list_user_availability_schedules()


@tool(args_schema=SetMeetingInput)
def set_meeting(meeting_start: str, email_address: str):
    """Books a 30-minute meeting on Google Calendar"""
    logger.info(f"Set meeting function called. Start: {meeting_start}, Email: {email_address}")
    return CALENDLY.set_meeting(
        meeting_start=meeting_start,
        email_address=email_address
    )


@tool(args_schema=CheckConflictInput)
def check_conflicts(meeting_start: str):
    """Checks for scheduling conflicts on Google Calendar, given a meeting time in IS0 8601 format."""
    logger.info(f"Check conflicts function called. Start: {meeting_start}")
    return CALENDLY.google.existing_events(meeting_start)


"""
Tools variable: Called in chat model 
"""
TOOLS = [get_current_availability, set_meeting, check_conflicts]
