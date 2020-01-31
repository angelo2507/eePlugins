from version import Version
Info='@j00zek %s' % Version

########################### Tlumaczenia ###########################################
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Language import language
import gettext
from os import environ

PluginLanguagePath = resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/e2componentsInitiator/locale')
    
def localeInit():
    lang = language.getLanguage()[:2]
    environ["LANGUAGE"] = lang
    gettext.bindtextdomain("e2cInitiator", PluginLanguagePath)

def mygettext(txt):
    t = gettext.dgettext("e2cInitiator", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

localeInit()
language.addCallback(localeInit)
_ = mygettext

########################### KONFIGURACJA ###########################################
from Components.config import config, ConfigSubsection, ConfigDirectory, ConfigSelection, ConfigYesNo

MinFontChoices = [("0", _("Defined in skin")), ("1", _("same as max font")),
                  ("0.75", _("75%% of defined font")), ("0,67", _("67%% of defined font")),
                  ("0,5", _("50%% of defined font")) ]
#############################################################################################

config.plugins.j00zekCC = ConfigSubsection()

config.plugins.j00zekCC.PiconAnimation_UserPath = ConfigDirectory(default = _('not set'))  
config.plugins.j00zekCC.AlternateUserIconsPath = ConfigDirectory(default = _('not set'))
#j00zekLabel
config.plugins.j00zekCC.j00zekLabelSN = ConfigSelection(default = "0", choices = MinFontChoices )
config.plugins.j00zekCC.j00zekLabelEN = ConfigSelection(default = "0", choices = MinFontChoices )
#runningText
config.plugins.j00zekCC.rtType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("don't move")), ("2", _("RUNNING")), ("3", _("SWIMMING"))])
config.plugins.j00zekCC.rtFontSize = ConfigSelection(default = "0", choices = [("0", _("if defined in skin")), ("0.1", _("+/- 10%%")), ("0.2", "+/- 20%%")])
config.plugins.j00zekCC.rtStartDelay = ConfigSelection(default = "0", choices =   [ ("0", _("Defined in skin")), ("1000", _("1s")), ("2000", _("2s")),
                                                                                   ("4000", _("4s")), ("6000", _("6s")), ("8000", _("8s")) ])
config.plugins.j00zekCC.rtStepTimeout = ConfigSelection(default = "0", choices = [ ("0", _("Defined in skin")), ("25", _("40 px/s")),
                                                                             ("50", _("20 px/s")), ("100", _("10 px/s")) ])
config.plugins.j00zekCC.rtRepeat = ConfigSelection(default = "0", choices = [ ("0", _("Defined in skin")), ("1", _("one time")),
                                                                             ("5", _("5 times")), ("100", _("never stop")) ])
#EventName
config.plugins.j00zekCC.enDescrType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("Short")),
                                                                                ("2", _("Extended or Short")), ("3", _("Short and Extended")),
                                                                                ("4", _("Extended and short (if different)")) ])
config.plugins.j00zekCC.enTMDBratingFirst = ConfigYesNo(default = False)
#j00zekModServiceName2
config.plugins.j00zekCC.snVFDtype = ConfigSelection(default = "\x25N", choices = [("\x25N", _("Chanel name")), ("\x25n - \x25N", _("Channel number - Channel name")),
                                                                                  ("\x25N - \x25S", _("Chanel name - Sat name")), ("\x25E", _("Event name")),
                                                                                  ("\x25N - \x25E", _("CHname - EVname")), ("\x25n - \x25N - \x25E", _("CHnumber - CHname - EVname")),
                                                                                  ("\x25N - \x25E (\x25e)", _("CHname - EVname (progress \x25)")),
                                                                                  ("\x25n - \x25N - \x25E (\x25e)", _("CHnumber -CHname - EVname (progress \x25)")),
                                                                                  ("\x25D", _("HH:MM E.g. 07:23")), ("\x25d", _("HH:MM E.g. 7:23"))
                                                                                 ])
#rollerCharLCD
config.plugins.j00zekCC.scroll_speed = ConfigSelection(default = "300", choices = [("500", _("slow")), ("300", _("normal")), ("100", _("fast"))])
config.plugins.j00zekCC.scroll_delay = ConfigSelection(default = "10000", choices = [("10000", "10 " + _("seconds")), ("20000", "20 " + _("seconds")),
                                                                                     ("30000", "30 " + _("seconds")), ("60000", "1 " + _("minute")),
                                                                                     ("300000", "5 " + _("minutes")), ("noscrolling", _("off"))
                                                                                    ])
#j00zekModClockToText
config.plugins.j00zekCC.clockVFDstdby = ConfigSelection(default = "\x25H:\x25M", choices = [("\x25H:\x25M", _("HH:MM E.g. 07:23")),("\x25-H:\x25M", _("HH:MM E.g. 7:23")),  
                                                                                            ("\x25H:%M:\x25S", _("HH:MM:SS")),
                                                                                  ("\x25H:\x25M \x25d.\x25m.\x25Y", _("HH:MM day.month.year")),
                                                                                  ("\x25H:\x25M \x25a \x25d \x25b", _("HH:MM Weekday Day MonthName")) ])
config.plugins.j00zekCC.clockVFDpos = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("left")), ("2", _("center")), ("3", _("right"))])
#ConfigText(default = _("none")) #("", _(""))