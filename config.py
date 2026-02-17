from dotenv import load_dotenv
import os
load_dotenv(".env")

bot_token = os.getenv("BOT_TOKEN")

full_camera_query = """
query {
  getCameraReport(cameraId: 1) {
    cameraId
    last_description_time
    peopleCountRow
    is_weapon_detected
  }
}
"""

