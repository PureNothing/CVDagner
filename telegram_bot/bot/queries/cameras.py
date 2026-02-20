full_camera1_query = """
query {
  getCameraReport(cameraId: 1) {
    cameraId
    last_description_time
    peopleCountRow
    is_weapon_detected
  }
}
"""

