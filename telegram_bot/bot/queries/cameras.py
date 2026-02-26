def query_parse(camera_id):
    return f"""
query{{
  getCameraReport(cameraId: {camera_id}) {{
    cameraIdReport
    lastDescriptionTime
  	objectsSummary{{
      label
      count
    }}
    isDangerDetected  
    statusCamera
  }}
}}
"""

full_general_report = """
query{
  getGeneralReport{
    mostDangerousCameraIdAndStats{
      cameraId
      label
      count
    }
    totalDetectionsAllTimeAllCameras{
      cameraId
      label
      count
    }
    statusOverviev
  }
}
"""