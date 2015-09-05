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

# Command generator

import re
import os
from template import *

class Generator:

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

	def setOutput(self, outputDir):
		self.outputDir = outputDir
		return self

	def getOutput(self):
		return self.outputDir

	def setListCommand(self, listCommand):
		self.listCommand = listCommand
		return self

	def getListCommand(self):
		return self.listCommand

	def generateCli(self):
		cliMainPath = self.getOutput() + '/main.cpp'
		cli = open(cliMainPath, 'w')
		includeContent = ''
		for command in self.getListCommand():
			includeContent += '#include <' + command.replace('::', '/') +'.h>\n'
		instanceContent = ''
		for command in self.getListCommand():
			className = command.split("::")[-1]
			instanceContent += 'cli->addCommand(new ' + className + '());\n'
		cli.write(self.renderString(cli_main, {
			'listInclude' : includeContent,
			'listInstance' : instanceContent
		}))
		cli.close()
		return self
	
	def generateServer(self):
		serverMainPath = self.getOutput() + '/main.cpp'
		server = open(serverMainPath, 'w')
		server.write(self.renderString(server_main, {
			'listInclude' : '',
			'listInstance' : ''
		}))
		server.close()
	
	def generateAppMakefile(self):
		appMakefile = self.getOutput() + '/Makefile'
		makefile = open(appMakefile, 'w')
		makefile.write(self.renderString(app_makefile, {
		}))
		makefile.close()
		return self
	
	def generateGenMakefile(self):
		genMakefile = self.getOutput() + '/Makefile'
		makefile = open(genMakefile, 'w')
		makefile.write(self.renderString(gen_makefile, {
		}))
		makefile.close()
		return self