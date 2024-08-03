from langchain.tools import tool

from src.services.calendly import Calendly
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

CALENDLY = Calendly()


class SetMeetingInput(BaseModel):
    meeting_start: str = Field(..., description="Start time of the meeting in ISO 8601 format.")
    meeting_end: str = Field(..., description="End time of the meeting in ISO 8601 format")
    email_address: str = Field(..., description="Email address of the person requesting the meeting.")

@tool
def get_current_availability():
    """Gets current availability using the CalendlyAPI"""
    return CALENDLY.list_user_availability_schedules()


@tool(args_schema=SetMeetingInput)
def set_meeting(meeting_start: str, meeting_end: str, email_address: str):
    """Books a 30-minute meeting on Google Calendar"""
    logger.info(f"Set meeting function called. Start: {meeting_start}, End: {meeting_end}, Email: {email_address}")
    return CALENDLY.set_meeting(
        meeting_start=meeting_start,
        meeting_end=meeting_end,
        email_address=email_address
    )


TOOLS = [get_current_availability, set_meeting]
