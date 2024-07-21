TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_calendly_availability",
            "description": "Gets meeting availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The acknowledgement message for when the user requests to get meeting availability.",
                    }
                },
                "required": ["message"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_calendly_meeting",
            "description": "Sets calendly meeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Acknowledges the user's request to send a calendly meeting."
                    }
                },
                "required": ["message"]
            }
        }
    }
]