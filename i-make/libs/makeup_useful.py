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

    def solo_makeup(self, target_image: str, target_landmarks: str, do_overlay: bool) -> np.ndarray:

        blended = self.blended
        self.initialization(blended)
        return self.render_effect(target_image, target_landmarks, do_overlay)

    def making_overlay_image(self, path: str, path_second: str) -> None:
        img = cv2.imread(path, -1)
        img2 = cv2.imread(path_second, -1)
        self.blended = cv2.addWeighted(src1=img, alpha=1.0, src2=img2, beta=1.0, gamma=0)
        """
        img2 = cv2.imread(second_path,-1)

        if img.shape[2] == 4:
            img[img[:,:,3]==0] = 0
        if img2.shape[2] == 4:
            img2[img2[:,:,3]==0] = 0

        self.blended = cv2.addWeighted(src1=img,alpha=1.0,src2=img2,beta=1.0,gamma=0)
        """

    def making_overlay_image_kahentyou_test(self, *pathes) -> None:
        images = np.zeros((1024, 1024, 4))
        for path in pathes:
            itiji = cv2.imread(path, -1)
            np.append(images, itiji)
        for i in range(len(images)):
            if images.shape[i][2] == 4:
                images[images[:, :, 3] == 0] = 0
        for image in images:
            self.blended = cv2.addWeighted(src1=self.blended, alpha=1.0, src2=image, beta=1.0, gamma=0)
