import sublime, sublime_plugin
# move.py
class Move_caret_topCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        screenful = self.view.visible_region()

        col = self.view.rowcol(self.view.sel()[0].begin())[1]
        row = self.view.rowcol(screenful.a)[0] + 1
        target = self.view.text_point(row, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))

class Move_caret_middleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        screenful = self.view.visible_region()

        col = self.view.rowcol(self.view.sel()[0].begin())[1]
        row_a = self.view.rowcol(screenful.a)[0]
        row_b = self.view.rowcol(screenful.b)[0]

        middle_row = (row_a + row_b) / 2
        target = self.view.text_point(middle_row, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))

class Move_caret_bottomCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        screenful = self.view.visible_region()

        col = self.view.rowcol(self.view.sel()[0].begin())[1]
        row = self.view.rowcol(screenful.b)[0] - 1
        target = self.view.text_point(row, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))

class Move_caret_forwardCommand(sublime_plugin.TextCommand):
    def run(self, edit, nlines):
        screenful = self.view.visible_region()

        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        target = self.view.text_point(row+nlines, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)

class Move_caret_backCommand(sublime_plugin.TextCommand):
    def run(self, edit, nlines):
        screenful = self.view.visible_region()

        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        target = self.view.text_point(row-nlines, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)

# RunMultipleCommand
class RunMultipleCommand(sublime_plugin.TextCommand):
    """RunMultipleCommand plugin
    Takes an array of commands (same as those you'd provide to a key binding)
    with an optional context (defaults to view commands) & runs each command in
    order. Valid contexts are 'text', 'window', and 'app' for running a
    TextCommand, WindowCommands, or ApplicationCommand respectively."""

    def exec_command(self, command):
        if 'command' not in command:
            raise Exception('No command name provided.')

        args = None
        if 'args' in command:
            args = command['args']

        # default context is the view since it's easiest to get the other
        # contexts from the view
        context = self.view
        if 'context' in command:
            context_name = command['context']
            if context_name == 'window':
                context = context.window()
            elif context_name == 'app':
                context = sublime
            elif context_name == 'text':
                pass
            else:
                raise Exception('Invalid command context "'+context_name+'".')

        # skip args if not needed
        if args is None:
            context.run_command(command['command'])
        else:
            context.run_command(command['command'], args)

    def run(self, edit, commands=None):
        if commands is not None:
            for command in commands:
                self.exec_command(command)



# Snippets.py
class PythonSnippetsPrintTraceback(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            s = """import traceback; traceback.print_stack()"""
            self.view.replace(edit, selection, s)


class PythonSnippetsPdbTrace(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            s = """import ipdb; ipdb.set_trace()"""
            self.view.replace(edit, selection, s)


class PythonSnippetsIpythonConsole(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            s = """import IPython; IPython.embed()"""
            self.view.replace(edit, selection, s)


class PythonSnippetsSignedOff(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            s = """Signed-off-by: Alessio Deiana <alessio.deiana@cern.ch>"""
            self.view.replace(edit, selection, s)

class PythonSnippetsTested(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            s = """Tested-by: Alessio Deiana <alessio.deiana@cern.ch>"""
            self.view.replace(edit, selection, s)