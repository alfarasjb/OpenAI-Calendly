TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_availability",
            "description": "Gets meeting availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The acknowledgement message for when the user requests to get meeting availability.",
                    }
                },
            },
            "required": ["message"]
        }
    }
]