from baseapp import BaseApplication
from shortcut import ShortcutMapper, Keystroke, parseKeySequence
from res import DirectoryWalker
import sys
import resource
import config

class Application(BaseApplication):

    def __init__(self, url):
        super(Application, self).__init__()
        self.config = config.loadConfig()
        self.setupWindow()
        self.setupKeymaps()
        self.dirwalker = DirectoryWalker(url)
        self.loadCurrentResource()

    def setupWindow(self):
        config = self.config
        section = 'window'
        if not config.has_section(section):
            return
        # fullscreen mode
        self.setFullscreen(config.getboolean(section, 'fullscreen'))
        # window size
        windowWidth = config.getint(section, 'width')
        windowHeight = config.getint(section, 'height')
        self.setWindowSize(windowWidth, windowHeight)

    def setupKeymaps(self):
        self.keymap = ShortcutMapper()
        keymap = self.keymap
        config = self.config
        functions = {
            "quit": self.quit,
            "next": self.next,
            "prev": self.prev,
            "fullscreen": self.toggleFullscreen,
            "zoom in": self.zoomIn,
            "zoom out": self.zoomOut,
            "restore": self.restore,
            "left": lambda: self.moveViewPort(-10, 0),
            "right": lambda: self.moveViewPort(+10, 0),
            "up": lambda: self.moveViewPort(0, -10),
            "down": lambda: self.moveViewPort(0, +10),
            "memory usage": self.printMemUsage,
        }
        # keybindings are written in the 'keymap' section
        for (name, value) in config.items('keymap'):
            if name in functions:
                # value is a space-delimited list of keybindings
                for keys in value.split():
                    keystrokes = parseKeySequence(keys)
                    if keys:
                        keymap.bind(keystrokes, functions[name])
                    else:
                        print "error: invalid keybinding value '%s'" % keys
            else:
                print "warning: unknown keybinding name '%s'" % name

    def onKeyPress(self, keystr):
        self.keymap.pressKey(Keystroke(keystr))

    def loadCurrentResource(self):
        res = self.dirwalker.currentResource()
        if res:
            self.loadImage(res.getUrl())
            self.updateWindowTitle()

    def updateWindowTitle(self):
        res = self.dirwalker.currentResource()
        if res:
            #self.drawText(res.getName(), 0, 0)
            self.setWindowTitle("jkbiv - %s" % res.getName())
        else:
            #self.drawText("No Image", 0, 0)
            pass
            self.setWindowTitle("jkbiv")

    # user-reachable functions

    def next(self):
        if self.dirwalker.next():
            self.loadCurrentResource()

    def prev(self):
        if self.dirwalker.prev():
            self.loadCurrentResource()

    def printMemUsage(self):
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print "usage: %d" % usage
