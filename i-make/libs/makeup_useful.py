import cv2
import numpy as np

from .effect import EffectRenderer2D


class MakeupUseful(EffectRenderer2D):
    def __init__(
        self,
        src_points_path: str = "i-make/res/source_landmarks.npy",
        filter_points_path: str = "i-make/res/filter_points.npy",
        use_filter_points: bool = True,
    ):
        """Initialize MakeupUseful.

        Args:
            src_points_path (str, optional): path to the source landmarks. Defaults to "i-make/res/source_landmarks.npy".
            filter_points_path (str, optional): path to the filter landmarks. Defaults to "i-make/res/filter_points.npy".
            use_filter_points (bool, optional): use filter landmarks. Defaults to True.
        """
        self.src_points = np.load(src_points_path)  # facemeshが返却する468(467)個のランドマークの座標
        self.filter_points = np.load(filter_points_path)  # src_pointsの中から選択するランドマークのindex
        self.use_filter_points = use_filter_points
        if use_filter_points:
            self.src_points = self.src_points[self.filter_points]

    def initialization(self, effect_image_path: str):
        """For initializing landmarks etc.every time
        Args:
            effect_image_path(str): path to the effect image (1024 x 1024)
        """
        self.effect_image = cv2.imread(effect_image_path, cv2.IMREAD_UNCHANGED)
        height, width, _ = self.effect_image.shape
        self.subdiv = cv2.Subdiv2D((0, 0, width, height))  # cv2.Subdiv2D((left, top, right, bottom))
        self.subdiv.insert(self.src_points.tolist())  # 対象の点を追加

        self.triangles_1D = np.array(
            [
                (self.src_points == value).all(axis=1).nonzero()
                for element in self.subdiv.getTriangleList()  # ドロネー三角形を取得 element=[1個目のx座標 1個目のy座標 2個目のx座標 2個目のy座標 3個目のx座標 3個目のy座標]
                for value in element.reshape((3, 2))
            ]
        )
        self.triangles = self.triangles_1D.reshape(len(self.triangles_1D) // 3, 3)

    def eye_bags0(self, target_image: str, target_landmarks: str, do_overlay: bool):
        path = "i-make/static/facepaints/custom/eye-bags/eye-bags0.png"
        self.initialization(path)
        return self.render_effect(target_image, target_landmarks, do_overlay)
