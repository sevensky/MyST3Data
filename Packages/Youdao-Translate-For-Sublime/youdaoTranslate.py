#coding:utf-8
import sys, sublime, sublime_plugin ,threading
from json import loads
try:
    from urllib import urlopen, urlencode, quote
except:
    from urllib.request import urlopen, build_opener, Request
    from urllib.parse import urlencode, quote

# if sublime.version() < '3':
    # from urllib2 import urlopen, build_opener, Request
    # from handler_st2 import *
    # from socks_st2 import *
# else:
	# from .handler_st3 import *
	# from .socks_st3 import *

PY2 = sys.version_info < (3, 0)
PY32 = sys.version_info < (3, 3)    # Python 2.5 to 3.2
PY33 = sys.version_info < (3, 4)    # Python 2.5 to 3.3

api="http://fanyi.youdao.com/openapi.do?keyfrom=friskfly&key=1410212834&type=data&doctype=json&version=1.1&q="

class TranslateException(Exception):
    """
    Default Translate exception
    >>> TranslateException("DoctestError")
    TranslateException('DoctestError',)
    """
    def __init__(self, msgs):
        super(TranslateException, self).__init__()
        self.msgs = msgs
    def __repr__(self):
        # return "\n".join(self.msgs)
        return self.msgs
    

class YoudaoTranslateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# print (self.view.sel()[0]) 光标x,y
		selection = self.view.substr( self.view.sel()[0] ).encode('utf-8')
		selection = selection.decode('utf-8')	#.replace('_', ' ')
		selection = self.camel_to_space(selection)
		selection = self.underline_to_camel(selection)
		thread = TranslateApi(selection)
		thread.start()
		self.handle_thread(thread)

	def camel_to_space(self, camel_format):  
	    ''''' 
	        驼峰命名格式转空格命名格式 
	    '''  
	    underline_format=''  
	    if isinstance(camel_format, str):  
	        for _s_ in camel_format:  
	            underline_format += _s_ if _s_.islower() else ' '+_s_.lower()  
	    return underline_format

	def underline_to_camel(self, underline_format):  
	    ''''' 
	        下划线命名格式驼峰命名格式 
	    '''  
	    camel_format = ''  
	    if isinstance(underline_format, str):  
	        for _s_ in underline_format.split('_'):  
	            camel_format += _s_.capitalize()  
	    return camel_format 

	def handle_thread(self,thread):
		if thread.is_alive():
			sublime.set_timeout(lambda: self.handle_thread(thread), 100)
			return
		if thread.result == False:
			sublime.status_message("connect youdao api failed,please try later.")
		else :
			# self.createWindowWithText(thread.result)	#.decode('utf-8')
			# print( type( thread.result ) )
			result = thread.result
			print(result)
			if thread.consoleshow:
				self.view.window().run_command('show_panel', {'panel': 'console'})

	def get_edit(view, edit_token=None):
		edit = None
		try:
			edit = view.begin_edit()
		except:
			pass

		if not edit and edit_token:
			try:
				edit = view.begin_edit(edit_token, 'YoudaoTranslate')
			except Exception as e:
				pass

		return edit

	def createWindowWithText(self, textToDisplay):
		newView = self.view.window().new_file()		# newView = sublime.active_window().new_file()
		edit = self.get_edit(newView)
		newView.insert(edit, 0, textToDisplay) # insert(edit, point, string)
		newView.end_edit(edit)
		newView.set_scratch(True)
		newView.set_read_only(True)
		newView.set_name("translate result")
		# newView.set_syntax_file("Packages/JavaScript/JSON.tmLanguage")
		return newView.id()
		
	def is_visible(self):
		is_visible = False
		# Only enable menu option if at least one region contains selected text.
		for region in self.view.sel():
			if not region.empty():
				is_visible = True
		return is_visible

	def is_enabled(self):
		return self.is_visible()

class TranslateApi(threading.Thread):
	def __init__(self,selection):
		threading.Thread.__init__(self);
		self.selection = selection;
		self.result = None;
		self.consoleshow = 0
	def run(self):
		url = api + quote(self.selection)
		#print (url)
		try:
			data = loads(urlopen(url).read().decode('utf-8')) 	#.decode('utf-8')
			# print (type(data['basic']) ) # data dict | data['v'] List
			if 'basic' in data.keys(): 
				sublime.status_message("基本释义：" + data['basic']['explains'][0])
			elif 'web' in data.keys():
				sublime.status_message( quote(self.selection) + "相关：" + data['translation'][0])
				self.consoleshow =	1
			else :
				sublime.status_message("最优结果：" + data['translation'][0])

			result = {
				'0': self.format(data),
				'20': "要翻译的文本过长",
				'30': "无法进行有效的翻译",
				'40': "不支持的语言类型",
				'50': "有道api接口出了点问题，请联系作者 weibo/friskfly"
			}[str(data['errorCode'])]
			# print (result)
			# result = result.encode('utf-8')
			# print (result.decode('utf-8'))
			self.result = result;
			return
		except IOError:
			raise TranslateException(self.error_codes[501])
		except ValueError:
			raise TranslateException(self.result)
	def format(self,data):
		# print ( type( data['query'] ) )
		result = data['query']
		result += "\n\n最优结果："
		if 'translation' in data:
			for i in data['translation']:
				result += i + ','
		result = result + "\n\n基本释义："
		if 'basic' in data:
			for i in data['basic']['explains']:
				result += i + ','
		result = result + "\n\n相关释义：\n----------------------------------------------------------\n"
		if 'web' in data:
			for i in data['web']:
				result += i['key'] + "  "
				for y in i['value'] :
					result += y + ','
				result +="\n"
		return result
