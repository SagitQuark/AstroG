from backend.services.detection_service import detect_motion

res = detect_motion()   # auto uses VIDEO_PATH
print(res)
