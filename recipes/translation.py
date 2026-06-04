from modeltranslation.translator import register, TranslationOptions
from .models import Category, Difficulty

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", )

@register(Difficulty)
class DifficultyTranslationOptions(TranslationOptions):
    fields = ("name", )