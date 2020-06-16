
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


urls = [
    'http://www.google.com',
    'http://www.google.com/android',
    'http://www.greatstuff.com',
    'http://www.facebook.com',
    ]
liststore = Gtk.ListStore(str)
for s in urls:
    liststore.append([s])

print(liststore)

completion = Gtk.EntryCompletion()
completion.set_model(liststore)
completion.set_text_column(0)

entry = Gtk.Entry()
entry.set_completion(completion)

# boilerplate
window = Gtk.Window()
window.add(entry)

window.connect('destroy', lambda w: Gtk.main_quit())
window.show_all()
Gtk.main()