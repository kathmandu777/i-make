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
        super().__init__(src_points_path, filter_points_path, use_filter_points)

    def initialization(self, blended_image: np.ndarray):
        """For initializing landmarks etc.every time
        Args:
            effect_image_path(str): path to the effect image (1024 x 1024)
        """

        self.effect_image = blended_image
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

    def making_overlay_image(self, *pathes) -> None:
        self.blended = cv2.imread("i-make/static/facepaints/black.png", -1)
        for path in pathes:
            image = cv2.imread(path, -1)
            self.blended = cv2.addWeighted(src1=self.blended, alpha=1.0, src2=image, beta=1.0, gamma=0)

    def makeup(self, target_image: np.ndarray, target_landmarks: np.ndarray, do_overlay: bool) -> np.ndarray:
        """単体又は合成画像からメイクを導出する
        Args:
            target_image(_type_): 描画する画像(カメラ画像)
            target_landmarks(_type_):target_image上でのランドマークの座標
            do_overlay(_type_):メイクを元画像(target_image)の上に貼り付けるかどうか

        Returns:
            np.array:メイクのみ、もしくは描画された画像
        """

        blended = self.blended
        self.initialization(blended)
        return self.render_effect(target_image, target_landmarks, do_overlay)
