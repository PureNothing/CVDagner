from app.logger import logger
from app.core.config import client
from app.tools.tools_json import tools
from app.core.toolcallpormpt import TOOLCALL_PROMT
from app.tools.call_airstrike import send_airstrike_tool
from app.tools.send_drone import send_drone_tool
import json
from app.services.kafkapublishactions import action_publish

async def tools_agent(message: str, mestnost: str):
    try:
        logger.debug("Пришло тревожное сообщение, отправляю агенту для выбора инструментов.")
        resonse = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": TOOLCALL_PROMT},
                {"role": "user", "content": f"{message}\n{mestnost}"}
            ],
            tools=tools
        )

        avaliable_tools = {
            "send_airstrike_tool": send_airstrike_tool,
            "send_drone_tool": send_drone_tool
        }

        if resonse.choices[0].message.tool_calls:
            tool = resonse.choices[0].message.tool_calls[0].function.name
            json_arguments = resonse.choices[0].message.tool_calls[0].function.arguments
            arguments = json.loads(json_arguments)
            tool_result = await avaliable_tools[tool](**arguments)
            await action_publish(tool_result)
    
    except Exception as e:
        logger.error("Не удалось вызвать инструмент или обратится к ЛЛМ.")
        raise




