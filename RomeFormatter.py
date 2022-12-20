__copyright__ = """
	Copyright 2022 Marek Piechut

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

		 http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
"""
__license__ = "Apache 2.0"

import sublime
import sublime_plugin
import subprocess
import os

from os import path
from sublime import Region, load_settings, expand_variables


settings = load_settings('RomeFormatter.sublime-settings')

supported_scopes = (
	("source.js", ".js"),
	("source.ts", ".ts"),
	("source.jsx", ".jsx"),
	("source.tsx", ".tsx"),
)

def find_binary(file):
	if not file:
		# Just return a binary name, so we try shell resolution if nothing found
		return 'rome'

	expected = path.join(file, 'node_modules', '.bin', 'rome')

	if path.exists(expected):
		return expected

	parent = path.dirname(path.abspath(file))
	if parent == file:
		parent = None

	return find_binary(parent)


class RomeFormatCommand(sublime_plugin.TextCommand):

	def extract_file_name(self):
		file_name = self.view.file_name()
		if file_name:
			return os.path.basename(file_name)
		else:
			view_main_scope = view.syntax().scope.partition(" ")[0]
			for scope, ext in supported_scopes:
				if sublime.score_selector(view_main_scope, scope):
					return ext

			return '.' + view_main_scope.split('.')[-1]

		return None

	def find_lookup_start_path(self):
		return \
			os.path.dirname(self.view.file_name() or '') or \
			sublime.active_window().extract_variables().get('file_path') or \
			os.path.dirname(sublime.active_window().project_file_name() or '') or \
			None

	def format_code(self, code):
		file_name = self.extract_file_name()
		path = self.find_lookup_start_path()
		binary = find_binary(path)
		config_file = find_config_file(path)
		cwd = os.path.dirname(config_file) if config_file else path

		proc = subprocess.Popen(
			[binary, "format", "--stdin-file-path", file_name ],
			stdin=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdout=subprocess.PIPE,
			cwd=cwd,
		)

		encoding = self.view.encoding()
		if not encoding or encoding == 'Undefined':
			encoding = 'utf-8'

		formatted, err = proc.communicate(code.encode(encoding))
		if err or proc.returncode != 0:
			print("Failed to exec Rome formatter", proc.returncode, err)
			return False

		return formatted.decode(encoding)

	def run(self, edit):
		selections = self.view.sel()
		if not selections or len(selections[0]) == 0:
			selections = [Region(0, self.view.size())]

		for region in selections:
			source = self.view.substr(region)
			replacement = self.format_code(source)
			if replacement:
				self.view.replace(edit, region, replacement)


def find_config_file(file):
	if not file:
		return None

	parent = path.dirname(path.abspath(file))
	if parent == file:
		return None

	expected = path.join(parent, 'rome.json')

	if path.exists(expected):
		return expected

	return check_config_exists(parent)


def format_on_save_enabled(file):
	enabled = settings.get('format_on_save') == True
	if enabled and settings.get('detect_config') == True:
		return bool(find_config_file(file))
	else:
		return enabled

class RomeFormatListener(sublime_plugin.EventListener):
		def on_pre_save(self, view):
			if format_on_save_enabled(view.file_name()):
				view.run_command('rome_format')
