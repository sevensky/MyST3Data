import re
import copy
import sublime_plugin

from FuzzyFilePath.common.config import config
from FuzzyFilePath.common.verbose import verbose
import FuzzyFilePath.project.validate as Validate
from FuzzyFilePath.project.CurrentFile import CurrentFile
from FuzzyFilePath.project.ProjectManager import ProjectManager

ID = "CurrentFileListener"

class CurrentFileListener(sublime_plugin.EventListener):
    """ Evaluates and caches current file`s project status """

    def on_post_save_async(self, view):
        if CurrentFile.is_temp():
            verbose(ID, "temp file saved, reevaluate")
            CurrentFile.cache[view.id()] = None
            ProjectManager.rebuild_filecache()
            self.on_activated(view)

    def on_activated(self, view):
        # view has gained focus
        CurrentFile.evaluate_current(view, ProjectManager.get_current_project())
