from ..mode.base import BaseModeMultiEffects


class DiagnosisMode(BaseModeMultiEffects):
    """Diagnosis makeup mode."""

    def __init__(self, effect_image_path: list[str], use_filter_points: bool = True) -> None:
        super().__init__(effect_image_path, use_filter_points=use_filter_points)

    @classmethod
    def diagnosis(cls):
        """どの画像を重ね合わせるべきか診断する."""
        return  # FIXME: 未実装
