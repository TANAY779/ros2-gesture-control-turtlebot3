from typing import Dict, List, Optional, Tuple


class GestureClassifier:
    TIP_IDS = [4, 8, 12, 16, 20]

    def get_finger_states(self, lm_list: List[List[int]]) -> List[int]:
        if len(lm_list) < 21:
            return [0, 0, 0, 0, 0]

        fingers: List[int] = []
        palm_width = abs(lm_list[5][0] - lm_list[17][0]) or 1

        # compute palm center as average of wrist and four MCPs
        palm_ids = [0, 5, 9, 13, 17]
        px = sum([lm_list[i][0] for i in palm_ids]) / len(palm_ids)
        py = sum([lm_list[i][1] for i in palm_ids]) / len(palm_ids)

        thumb_tip_x, thumb_tip_y = lm_list[4][0], lm_list[4][1]
        thumb_ip_x, thumb_ip_y = lm_list[3][0], lm_list[3][1]

        # distance from thumb tip to palm center
        dx = thumb_tip_x - px
        dy = thumb_tip_y - py
        dist = (dx * dx + dy * dy) ** 0.5

        # dynamic threshold based on palm width
        dist_thresh = max(20, 0.4 * palm_width)

        # allow thumb to be considered extended if it is either:
        # - noticeably away from palm center (common for thumb-up/thumb-out), or
        # - has visible separation from the IP joint (thumb curled vs extended)
        ip_sep = abs(thumb_tip_y - thumb_ip_y)
        ip_sep_thresh = max(10, 0.12 * palm_width)

        thumb_extended = (dist > dist_thresh) or (ip_sep > ip_sep_thresh)
        fingers.append(1 if thumb_extended else 0)

        for tip in self.TIP_IDS[1:]:
            fingers.append(1 if lm_list[tip][2] < lm_list[tip - 2][2] else 0)

        return fingers

    def classify(
        self,
        fingers: List[int],
        landmarks: Optional[Dict[int, Tuple[int, int]]] = None,
    ) -> str:
        gesture = "Unknown"
        thumb, index, middle, ring, pinky = fingers

        if fingers == [1, 1, 1, 1, 1]:
            gesture = "STOP"
        elif fingers == [0, 0, 0, 0, 0]:
            gesture = "EMERGENCY STOP"
        elif index == 1 and middle == 0 and ring == 0 and pinky == 0 and landmarks is not None:
            index_tip_x = landmarks[8][0]
            index_pip_x = landmarks[6][0]
            if index_tip_x < index_pip_x:
                gesture = "LEFT"
            elif index_tip_x > index_pip_x:
                gesture = "RIGHT"
        # if all four fingers are folded but thumb may be noisy, detect fist
        elif index == 0 and middle == 0 and ring == 0 and pinky == 0 and landmarks is not None:
            palm_ids = [0, 5, 9, 13, 17]
            px = sum([landmarks[i][0] for i in palm_ids]) / len(palm_ids)
            py = sum([landmarks[i][1] for i in palm_ids]) / len(palm_ids)
            thumb_tip_x, thumb_tip_y = landmarks[4][0], landmarks[4][1]
            dx = thumb_tip_x - px
            dy = thumb_tip_y - py
            dist = (dx * dx + dy * dy) ** 0.5
            palm_width = abs(landmarks[5][0] - landmarks[17][0]) or 1
            # if thumb is close to palm center, treat as fist -> EMERGENCY STOP
            if dist < max(25, 0.25 * palm_width):
                gesture = "EMERGENCY STOP"
            else:
                # otherwise decide forward/backward from thumb vertical position
                thumb_tip_y = landmarks[4][1]
                thumb_ip_y = landmarks[3][1]
                gesture = "FORWARD" if thumb_tip_y < thumb_ip_y else "BACKWARD"
        elif thumb == 1 and index == 0 and middle == 0 and ring == 0 and pinky == 0 and landmarks is not None:
            thumb_tip_y = landmarks[4][1]
            thumb_ip_y = landmarks[3][1]
            gesture = "FORWARD" if thumb_tip_y < thumb_ip_y else "BACKWARD"

        return gesture
