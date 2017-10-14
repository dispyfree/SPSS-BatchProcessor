
class Lang:

    entries = {
        'en': {},
        'ch' :{'Load Configuration' : '调入配置'}
    }

    defaultLang = 'en'

    @classmethod
    def getLang(cls, lang = None):
        if (lang is None
            or not(lang in cls.entries)):
            return cls.defaultLang
        else:
            return lang

    @classmethod
    def get(cls, entry, lang=None):
        lang = cls.getLang(lang)
        langEntries = cls.entries[lang]

        if not(entry in langEntries):
            return entry
        else:
            return langEntries[entry]