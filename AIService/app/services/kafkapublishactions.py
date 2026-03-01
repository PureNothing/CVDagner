from app.core.kafkabroker import broker

async def action_publish(message: str):
    await broker.publish(message={"action":message}, topic="agent_actions")