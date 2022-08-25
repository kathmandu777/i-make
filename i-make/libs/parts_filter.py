import cv2
import numpy as np


class FacePartsFilter:
    def draw_line(self, image, part_points, landmarks, color):
        for start_index, end_index in part_points:
            start = landmarks.landmark[start_index]
            end = landmarks.landmark[end_index]
            relative_start = (int(start.x * image.shape[1]), int(start.y * image.shape[0]))
            relative_end = (int(end.x * image.shape[1]), int(end.y * image.shape[0]))
            cv2.line(image, relative_start, relative_end, color, thickness=2)

    @staticmethod
    def filter(image, part_points, landmarks, color):
        points = []
        for start_index, end_index in part_points:
            start = landmarks[start_index]
            end = landmarks[end_index]
            relative_start = (int(start[0]), int(start[1]))
            relative_end = (int(end[0]), int(end[1]))
            points.append([relative_start, relative_end])
        mask_image = np.zeros_like(image)
        mask_image = cv2.fillPoly(mask_image, np.int32(np.array(points)), color)
        filtered_image = np.zeros_like(image)
        filtered_image = cv2.bitwise_and(image, mask_image)
        filtered_image = cv2.GaussianBlur(filtered_image, (7, 7), 10)
        return cv2.addWeighted(image, 1.0, filtered_image, 1.0, 0)
