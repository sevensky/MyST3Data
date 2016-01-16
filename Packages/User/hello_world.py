import sublime, sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
	'''1 ctrl+n  2 ctrl+`  3view.run_command("example")'''

	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")
