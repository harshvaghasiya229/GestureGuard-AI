def finger_count(landmarks):
    tips = [8, 12, 16, 20]
    return sum([1 if landmarks[tip].y < landmarks[tip - 2].y else 0 for tip in tips])