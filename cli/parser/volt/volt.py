#!/usr/bin/python
#
# Pengo Project
#
# Copyright (c) 2015 Penlook Development Team
#
# --------------------------------------------------------------------
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# Authors:
#     Loi Nguyen       <loint@penlook.com>

from php import *
import re

class Volt:

	def __init__(self):
		pass
	
	def renderString(self, template, data):
		content = ''
		start = 0
		end = -1
		for match in re.finditer(r"\{\{[a-zA-Z0-9_\s]+\}\}", template):
			end = match.start()
			if start < end:
				content += template[start:end]
			start = end + 1
			var_block = template[match.start():match.end()]
			var = re.split("\s+", var_block)[1]
			if var in data:
				content += data[var]
			start = match.end()
		content += template[start:]
		content = content.replace('"', '\"')
		return content

	def compileAll(self, cppHTMLPath):
		templateCPP = """// AUTO GENERATED
{{ viewHeader }}
namespace app {
namespace view {
void {{ funcName }}(View *view) {
{{ variableHeader }}
{{ htmlContent }}
}\n}\n}"""
		cppEmbedded = "";
		with open(cppHTMLPath, "r") as lines:
			for line in lines:
				line = line.strip()
				if len(line) > 0:
					cppEmbedded += line
		cppEmbedded = "<?cpp ?>" + cppEmbedded
		cppSegments = cppEmbedded.split("<?cpp")
		cppContent = ""
		for cppSegment in cppSegments:
			cppArr = cppSegment.split("?>");
			cppContent += cppArr[0].strip() + '\n';
			if len(cppArr) == 2:
				cppContent += 'view->stream += "' + cppArr[1].strip().replace('"', '\\"') + '";\n'
		cppPath = cppHTMLPath.split(".html")[0]
		cpp = open(cppPath, 'w')
		variableHeader = ""
		for variable in self.getData()["variables"]:
			variableHeader += variable['Type'] + ' ' + variable['Name'] + ' = view->getData()->get<' + variable['Type'] + '>("' + variable['Name'] + '");\n'
		cpp.write(self.renderString(templateCPP, {
			'htmlContent' : cppContent.strip(),
			'variableHeader' : variableHeader.strip(),
			'viewHeader' : self.data["viewHeader"],
			'funcName' : self.data["funcName"]
		}))
		cpp.close()

	def setData(self, data):
		self.data = data
		
	def getData(self):
		return self.data

	def generateHeader(self, viewPath, viewStack):
		viewHeaderTemplate = """// AUTO GENERATED
#include <sys/type.h>
#include <sys/func.h>
#include <app/view.h>
namespace app {
namespace view {
{{ headerContent }}
}\n}"""
		cpp = open(viewPath + "/view.h", 'w')
		headerContent = ''
		for viewHeader in viewStack:
			headerContent += 'void ' + viewHeader + "(View *view);\n"
		cpp.write(self.renderString(viewHeaderTemplate, {
			'headerContent' : headerContent
		}))
		cpp.close()

	def compile(self, target, dest):
		php = PHP("")
		code = '(new Volt\Compiler())->compileFile'
		code += "('" + target +"', '" + dest + "');"
		php.get_raw(code)
		self.compileAll(dest)