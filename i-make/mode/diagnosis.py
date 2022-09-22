from ..mode.base import BaseModeEffect


class DiagnosisMode(BaseModeEffect):
    """Diagnosis makeup mode."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def diagnosis(cls):
        """どの画像を重ね合わせるべきか診断する."""
        return  # FIXME: 未実装
