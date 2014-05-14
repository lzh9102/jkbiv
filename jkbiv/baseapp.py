import gtk

def computeDrawingArea(windowWidth, windowHeight, imageWidth, imageHeight):
    """ Determine how to draw the image at the center of the window as large as
        possible and without cropping. Returns (x, y, width, height) of the
        computed area.
    """
    return (0, 0, windowWidth, windowHeight)

class BaseApplication(object):

    def __init__(self, width, height):
        window = gtk.Window()
        window.connect("destroy", gtk.main_quit)
        window.set_size_request(width, height)
        window.set_position(gtk.WIN_POS_CENTER)
        self.window = window

        # drawing area
        drawarea = gtk.DrawingArea()
        drawarea.set_size_request(width, height)
        window.add(drawarea)
        #drawarea.window.set_background(gtk.gdk.Color(0, 255, 0))
        #drawarea.window.draw_text(self.gc, "hello")
        self.drawarea = drawarea

        self.width = width
        self.height = height

        self.pixbuf = None

        # events
        window.connect("key_press_event", self.__handleKeyPress)
        drawarea.connect("expose-event", self.gtkExposeEvent)

        window.show_all()

    def __isModifier(self, keystr):
        # TODO: improve efficiency by using numeric value
        return keystr.startswith("control_") or keystr.startswith("shift_") \
                or keystr.startswith("meta_") or keystr.startswith("alt_")

    def __handleKeyPress(self, widget, event):
        keystr = gtk.gdk.keyval_name(event.keyval).lower() # key name
        if self.__isModifier(keystr): # ignore modifier keys
            return
        if event.state & gtk.gdk.SHIFT_MASK: # with shift key
            keystr = "S-" + keystr
        if event.state & gtk.gdk.CONTROL_MASK: # with control key
            keystr = "C-" + keystr
        if event.state & gtk.gdk.MOD1_MASK: # with alt (meta) key
            keystr = "A-" + keystr
        self.onKeyPress(keystr)

    def quit(self):
        self.window.destroy()

    def gtkExposeEvent(self, widget, event):
        (x, y, width, height) = event.area
        self.width = width
        self.height = height
        self.redraw()

    def loadImage(self, url):
        # TODO: implement image loader
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(url)

    def redraw(self):
        print "Redraw(width=%d, height=%d)" % (self.width, self.height)
        self.redrawImage()

    def redrawImage(self):
        if self.pixbuf:
            # compute image area
            (x, y, width, height) = computeDrawingArea(self.width,
                                                       self.height,
                                                       self.pixbuf.get_width(),
                                                       self.pixbuf.get_height()
                                                       )
            # scale image
            pixbuf = self.pixbuf.scale_simple(width, height,
                                              gtk.gdk.INTERP_BILINEAR)
            # draw image
            self.drawarea.window.draw_pixbuf(None, pixbuf, 0, 0, x, y)

    # event callbacks

    def onKeyPress(self, keystr):
        """ this function will be called when a key is pressed """
        pass
