#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

#you need to import webkit and gobject, gobject is needed for threads
import webkit
import gobject

class Browser:
    default_site = "http://www.google.com/"

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(1024,768)
        self.window.set_title("Haggistech Browser")
        self.window.set_resizable(True)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)





        #webkit.WebView allows us to embed a webkit browser
        #it takes care of going backwards/fowards/reloading
        #it even handles flash
        self.web_view = webkit.WebView()
	self.web_view.connect("title-changed", self.new_title)
        self.web_view.open(self.default_site)

        toolbar = gtk.Toolbar()



        #create the back button and connect the action to
        #allow us to go backwards using webkit
        self.back_button = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.back_button.connect("clicked", self.go_back)

        #same idea for forward button
        self.forward_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.forward_button.connect("clicked", self.go_forward)

        #again for refresh
        refresh_button = gtk.ToolButton(gtk.STOCK_REFRESH)
        refresh_button.connect("clicked", self.refresh)

        #again for stop
        stop_button = gtk.ToolButton(gtk.STOCK_STOP)

       # stop_button.connect("clicked", self.stop)

        #again for home
        home_button = gtk.ToolButton(gtk.STOCK_HOME)
        home_button.connect("clicked", self.home)

        #add the buttons to the toolbar
        toolbar.add(self.back_button)
        toolbar.add(self.forward_button)
        toolbar.add(refresh_button)
        toolbar.add(home_button)
        toolbar.add(stop_button)

        #entry bar for typing in and display URLs, when they type in a site
        #and hit enter the on_active function is called
        self.url_bar = gtk.Entry()
        self.url_bar.connect("activate", self.on_active)

        #anytime a site is loaded the update_buttons will be called
        self.web_view.connect("load_committed", self.update_buttons)

	self.web_view.connect("load-finished", self.load_finished)




        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)
        


        self.statusbar = gtk.Statusbar()


        vbox = gtk.VBox(False, 0)
        vbox.pack_start(toolbar, False, False, 0)
        #vbox.pack_start(self.url_bar, False, True, 0)
	vbox.pack_start(self.url_bar, False, False, 0)
        vbox.add(scroll_window)
        vbox.pack_start(self.statusbar, False, False, 0)

        self.window.add(vbox)
        self.window.show_all()






    def on_active(self, widget, data=None):
        '''When the user enters an address in the bar, we check to make
           sure they added the http://, if not we add it for them.  Once
           the url is correct, we just ask webkit to open that site.'''
        url = self.url_bar.get_text()
        try:
            url.index("://")
        except:
            url = "http://"+url
        self.url_bar.set_text(url)
        self.web_view.open(url)
	self.statusbar.push(0, "Loading....")


    def go_back(self, widget, data=None):
        #Webkit will remember the links and this will allow us to go backwards
        self.web_view.go_back()
	self.statusbar.push(0, "Loading....")


    def go_forward(self, widget, data=None):
        #Webkit will remember the links and this will allow us to go forwards
        self.web_view.go_forward()
	self.statusbar.push(0, "Loading....")

    def refresh(self, widget, data=None):
        #Simple makes webkit reload the current back
        self.web_view.reload()
	self.statusbar.push(0, "Loading....")

    def load_finished(self, widget, data=None):
	self.statusbar.push(0, "Loading Complete")




    def home(self, widget, data=None):
	self.statusbar.push(0, "Loading....")
        self.web_view.open(self.default_site)


	

    def update_buttons(self, widget, data=None):
        '''Gets the current url entry and puts that into the url bar.
           It then checks to see if we can go back, if we can it makes the
           back button clickable.  Then it does the same for the foward
           button.'''
        self.url_bar.set_text( widget.get_main_frame().get_uri() )
        self.back_button.set_sensitive(self.web_view.can_go_back())
        self.forward_button.set_sensitive(self.web_view.can_go_forward())

    def new_title(self, window, frame, title):
	self.window.set_title('Haggistech Browser - ' + title)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    browser = Browser()
    browser.main()

