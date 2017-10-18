
class Lang:

    entries = {
        'en': {'runDescription' : 'Applies the selected SPSS routine on every file individually, in the order provided in the input tab. Upon the first error, execution will pause and the operator may choose whether to proceed. Simulation will output the SPSS code applied to the very first file - in this case, no computation is performed. '},
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