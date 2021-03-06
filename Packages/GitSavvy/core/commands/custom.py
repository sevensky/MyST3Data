import sublime
import threading
from sublime_plugin import WindowCommand

from ..git_command import GitCommand
from ...common import util


ALL_REMOTES = "All remotes."


class CustomCommandThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        super(CustomCommandThread, self).__init__(**kwargs)
        self.cmd_args = args
        self.cmd_func = func
        self.daemon = True

    def run(self):
        return self.cmd_func(*self.cmd_args)


class GsCustomCommand(WindowCommand, GitCommand):

    """
    Run the specified custom command asynchronously.
    """

    def run(self, **kwargs):
        sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

    def run_async(self,
                  output_to_panel=False,
                  args=None,
                  start_msg="Starting custom command...",
                  complete_msg="Completed custom command.",
                  run_in_thread=False):

        if not args:
            sublime.error_message("Custom command must provide args.")

        for idx, arg in enumerate(args):
            if arg == "{REPO_PATH}":
                args[idx] = self.repo_path
            elif arg == "{FILE_PATH}":
                args[idx] = self.file_path

        sublime.status_message(start_msg)
        if run_in_thread:
            stdout = ''
            cmd_thread = CustomCommandThread(self.git, *args)
            cmd_thread.start()
        else:
            stdout = self.git(*args)
        sublime.status_message(complete_msg)

        if output_to_panel:
            util.log.panel(stdout)
