#!/usr/bin/env python3
"""
LRDEnE Guardian - i18n Module
=============================

Localization and internationalization support for the core engine.
"""

import os
import gettext
from typing import Optional

class LocaleManager:
    """Manages translations and locales for LRDEnE Guardian."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocaleManager, cls).__new__(cls)
            cls._instance.locales_path = os.path.join(os.path.dirname(__file__), "locales")
            cls._instance.current_locale = "en"
            cls._instance.translator = None
        return cls._instance
    
    def set_locale(self, locale: str):
        """Sets the current locale and loads translations."""
        self.current_locale = locale
        try:
            self.translator = gettext.translation(
                "guardian", 
                localedir=self.locales_path, 
                languages=[locale],
                fallback=True
            )
        except Exception:
            self.translator = gettext.NullTranslations()
            
    def _(self, message: str) -> str:
        """Translates a message."""
        if self.translator is None:
            self.set_locale(self.current_locale)
        return self.translator.gettext(message)

# Global instances
locale_manager = LocaleManager()
_ = locale_manager._
