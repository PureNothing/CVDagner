tools = [
    {
        "type": "function",
        "function": {
            "name": "send_airstrike_tool",
            "description": "Вызвать авиаудар по координатам камеры.",
            "parameters": {
                "type": "object",
                "properties": {
                    "camera_id": {
                        "type": "integer",
                        "description": "Номер камеры."
                    }
                },
                "required": ["camera_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_drone_tool",
            "description": "Отправить разведывательного дрона по коордианатам камеры.",
            "parameters": {
                "type": "object",
                "properties": {
                    "camera_id": {
                        "type": "integer",
                        "description": "Номер камеры"
                    }
                },
                "required": ["camera_id"]
            }
        }
    }
]