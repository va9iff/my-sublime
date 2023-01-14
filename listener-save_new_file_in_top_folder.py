import sublime_plugin

class NewFileListener(sublime_plugin.EventListener):
    def on_new_async(self, view):
        if not view.window() or not view.window().folders():
            return
        view.settings().set("default_dir", view.window().folders()[0])

