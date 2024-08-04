import json
import logging
from typing import Dict, Optional, Any
from datetime import datetime as dt, timedelta

import requests

from src.definitions.credentials import Credentials
from src.services.google import GoogleAPI

# NOTE: Calendly does not have an endpoint to support scheduling events.
# Must use a different option
# https://developer.calendly.com/frequently-asked-questions

logger = logging.getLogger(__name__)


class Calendly:
    def __init__(self):
        self.google = GoogleAPI()
        self._api_key = Credentials.calendly_api_key()
        self.base_url = 'https://api.calendly.com'
        self.headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        self.user_uri = self.get_user_uri()
        self.last_recorded_email_address = ""
        self.last_recorded_meeting_start = ""
        self.last_recorded_meeting_end = ""

    def get_user_uri(self) -> str:
        endpoint = self.base_url + "/users/me"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()['resource']['uri']

    def list_user_availability_schedules(self) -> Optional[Dict[str, Any]]:
        logger.info("Getting user availability schedules..")
        endpoint = self.base_url + "/user_availability_schedules"
        params = {"user": self.user_uri}
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            available_schedule = {}
            schedules = response_json['collection'][0]['rules']
            timezone = response_json['collection'][0]['timezone']
            for schedule in schedules:
                if len(schedule['intervals']) == 0:
                    continue
                available_schedule[schedule['wday']] = schedule['intervals']
            # return self.to_readable_schedule(available_schedule, timezone)
            return available_schedule
        else:
            logger.info("Something went wrong..")

    def to_readable_schedule(self, schedule: Dict[str, any], timezone: str) -> str:
        schedules = [f"Timezone: {timezone}"]
        for day, times in schedule.items():
            schedules.append(day)
            for time in times:
                schedules.append(f" - {time['from']} - {time['to']}")
        return '\n'.join(schedules)

    def get_user_event_types(self):
        endpoint = self.base_url + "/event_types"
        params = {"user": self.user_uri}
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code:
            event_uri = response.json()['collection'][0]['uri']
        print(json.dumps(response.json(), indent=4))

    @staticmethod
    def get_meeting_end_timestamp(meeting_start: str) -> str:
        meeting_start_datetime = dt.fromisoformat(meeting_start)
        meeting_start_datetime += timedelta(minutes=30)
        return meeting_start_datetime.isoformat()

    def set_meeting(self, meeting_start: str, email_address: str) -> bool:
        meeting_end = self.get_meeting_end_timestamp(meeting_start)
        # Ignore empty inputs
        if meeting_start == "" or meeting_end == "" or email_address == "":
            logger.error(f"Failed to set meeting. Meeting information cannot be empty. Meeting Start: {meeting_start}, "
                         f"Meeting End: {meeting_end}, Customer Name: {email_address}")
            return False
        # Ignore repeat requests
        if (self.last_recorded_meeting_start == meeting_start and
                self.last_recorded_meeting_end == meeting_end and
                self.last_recorded_email_address == email_address):
            logger.error(f"Failed to set meeting. Duplicate requests")
            return False
        self.last_recorded_meeting_start = meeting_start
        self.last_recorded_meeting_end = meeting_end
        self.last_recorded_email_address = email_address
        logger.info(f"Setting meeting for: {email_address} from {meeting_start} to {meeting_end}")
        return self.google.create_meeting(meeting_start, meeting_end, email_address)
