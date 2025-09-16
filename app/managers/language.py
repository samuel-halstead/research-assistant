import fasttext as ft

from app.core.config import settings


class LanguageManager:
    def __init__(self):
        self.model = ft.load_model(str(settings.MODELS_PATH / settings.FASTTEXT_MODEL))

    def detect_language(self, query: str) -> str:
        prediction = self.model.predict(query, k=1)
        return settings.FASTTEXT_LANGUAGES_MAP[prediction[0][0].replace("__label__", "")]


language_manager = LanguageManager()
