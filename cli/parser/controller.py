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

# Controller parser

import os
import sys
import pprint
import hashlib
from pattern import *

def tab(times):
	tabContent = '\n'
	for i in range(0, times):
		tabContent += '\t'
	return tabContent

class Controller:

	def __init__(self):
		self.annotationInfo = {}
		self.defaultAnnotation = {
			'@Route': None,
			'@Method': '*',
			'@Type': 'HTML'
		}

	def initHeaderParser(self):
		self.annotationStack = {}
		self.lineStack = []
		self.currentClass = None
		self.currentMethod = None
		self.isAction = False

		self.stackPublic = []
		self.stackPrivate = []
		self.stackProtected = []
		self.stackNonAccessModifier = []
		self.methodBlockContent = {}

	def setInput(self, targetDir):
		self.Input = targetDir
		return self

	def setOutput(self, destDir):
		self.Output = destDir
		if not os.path.isdir(self.Output):
			os.makedirs(self.Output)
		return self

	def setTemplate(self, templateContext):
		self.Template = templateContext
		return self

	def setConfig(self, configDir):
		self.Config = configDir
		return self

	def parseSourceFile(self, sourcePath):
		pass

	def parseHeaderFile(self, headerPath):
		self.initHeaderParser()
		annotationStorage = {}
		self.annotationStack = {}
		# Pattern recognition
		pattern = Pattern()
		pattern.setContext(self)
		# Compile file
		with open(headerPath, "r") as lines :
			for line in lines:
				line = line.strip()
				if len(line) > 0:
					self.line = line
					self.lineStack.append(line)
					if pattern.isComment():
						continue
					if pattern.isHeader():
						self.headerContent += self.line + "\n"
						continue
					if pattern.isAnnotation():
						annotationArr = self.line.split(' ')
						annotationName = annotationArr[0].strip()
						annotationValue = ' '.join(annotationArr[1:])
						if annotationName == '@Route':
							self.isAction = True
						self.annotationStack[annotationName] = annotationValue
						continue
					if pattern.isMethod():
						# Default
						method_without_am = self.line
						action_type = ''
						am = False
						if self.isAction:
							 action_type = 'void'
						if pattern.isPublic():
							method_without_am = self.line.split('public')[1]
							method_without_am = action_type + method_without_am
							self.stackPublic.append(method_without_am)
							am = True
						if pattern.isPrivate():
							method_without_am = self.line.split('private')[1]
							method_without_am = action_type + method_without_am
							self.stackPrivate.append(method_without_am)
							am = True
						if pattern.isProtected():
							method_without_am = self.line.split('protected')[1]
							method_without_am = action_type + method_without_am
							self.stackProtected.append(method_without_am)
							am = True
						if am is False:
							method_without_am = action_type + method_without_am
							self.stackNonAccessModifier.append(method_without_am)
						if len(self.annotationStack) > 0:
							indexL = method_without_am.index('(');
							indexR = indexL
							while indexR > 0:
								if method_without_am[indexR] == ' ':
									break
								indexR = indexR - 1
							currentMethod = method_without_am[indexR : indexL]
							self.annotationInfo[self.currentClass]['Method'].append(
								{'Name': currentMethod, '@': self.annotationStack }
							)
						self.annotationStack = {}
						continue
					if pattern.isProperty():
						am = False
						if pattern.isPublic():
							am = True
							property_without_am = self.line.split('public')[1]
							self.stackPublic.append(property_without_am)
						if pattern.isPrivate():
							am = True
							property_without_am = self.line.split('private')[1]
							self.stackPrivate.append(property_without_am)
						if pattern.isProtected():
							am = True
							property_without_am = self.line.split('protected')[1]
							self.stackProtected.append(property_without_am)
						if am is False:
							self.stackNonAccessModifier.append(property_without_am)
						continue
					if pattern.isClass():
						class_without_bracket = self.line
						if pattern.isEndWithBracket():
							class_without_bracket = self.line.split('{')[0]
						className = class_without_bracket.split(' ')[1]
						self.currentClass = className
						self.annotationInfo[self.currentClass] = {'@': self.annotationStack, 'Method': []}
						self.annotationStack = {}
						continue
		if self.currentClass is None:
			print 'Controller class does not exist !'
			print headerPath
			exit()

	def generateHeader(self):
		self.headerContent += 'class ' + self.currentClass + "\n{\n"
		if len(self.stackPublic) > 0:
			self.headerContent += '\tpublic:\n'
		for publicItem in self.stackPublic:
			self.headerContent += '\t\t' + publicItem.strip() + ';\n'
		if len(self.stackPrivate) > 0:
			self.headerContent += '\tprivate:\n'
		for privateItem in self.stackPrivate:
			self.headerContent += '\t\t' + privateItem.strip() + ';\n'
		if len(self.stackProtected) > 0:
			self.headerContent += '\tprotected:\n'
		for protectedItem in self.stackProtected:
			self.headerContent += '\t\t' + protectedItem.strip() + ';\n'
		for protectedItem in self.stackNonAccessModifier:
			self.headerContent += '\t' + protectedItem.strip() + ';\n'
		self.headerContent += '};'

	def compileFile(self, filePath):
		fileName = filePath.split(".")[0]
		self.controllerName = fileName.split("/")[-1]
		headerPath = self.Input + "/" + fileName + ".h"
		cppPath	   = self.Input + "/" + fileName + ".cpp"
		destHeaderPath = self.Output + "/" + fileName + ".h"
		destCppPath = self.Output + "/" + fileName + ".cpp"

		self.headerContent = ''
		self.cppContent = '#include "'+ self.controllerName + '.h"\n'
		self.parseHeaderFile(headerPath)
		self.generateHeader()
		#self.parseSourceFile(cppPath)

		# Prepare to write
		header = open(destHeaderPath, 'w')
		cpp = open(destCppPath, 'w')

		# Write content to file
		header.write(self.headerContent)
		header.close()
		cpp.write(self.cppContent)
		cpp.close()

	def mergeAnnotation(self):
		annotationList = []
		for className in self.annotationInfo:
			classAnnotation = self.annotationInfo[className]['@']
			for methodInfo in self.annotationInfo[className]['Method']:
				# Override class annotation
				for defaultAnnotation in classAnnotation:
					if defaultAnnotation not in methodInfo['@']:
						methodInfo['@'][defaultAnnotation] = classAnnotation[defaultAnnotation]
				# If really missing annotation, then using default annotation
				for defaultAnnotation in self.defaultAnnotation:
					if defaultAnnotation not in methodInfo['@']:
						methodInfo['@'][defaultAnnotation] = self.defaultAnnotation[defaultAnnotation]
				# Add controller - action
				methodInfo['@']['@Controller'] = className
				methodInfo['@']['@Action'] = methodInfo['Name']
				annotationList.append(methodInfo['@'])
		return annotationList
	
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
	
	def generateControllerActionMapping(self):
		controllesH = os.path.abspath(self.Output + '/../main/controllers.h')
		controllers = open(controllesH, 'w')
		controllersTemplate = """
// AUTO GENERATED
#include <map>
#include <vector>
#include <functional>
#include <app/controller.h>
namespace app {
	ListController getControllers() {
		ListController controllers = new ListController;{{ controllers }}
		return controllers;
	}
}"""
		controllerList = ''
		print 'Scan controller - action \n\n'
		print self.Input
		hashMd5 = hashlib.md5()
		for className in self.annotationInfo:
			controllerList += tab(2) + 'controllers["' + className +'"] = (new Controller)' + tab(9) +'->setName("' + className + '")'
			for methodInfo in self.annotationInfo[className]['Method']:
				actionName = methodInfo['Name']
				hashMd5.update(className + '-' + actionName)
				hashAction = hashMd5.hexdigest()
				controllerList += tab(9) + '->addAction(' + tab(10) +'(new Action)' + tab(11) + '->setName("' + actionName +'")'
				controllerList += tab(11) + '->setHash("' + hashAction + '")'
				if 
				#print hashAction
				controllerList += tab(9) + ')'
			controllerList += ';';
		controllersContent = self.renderString(controllersTemplate, {
			'controllers' : controllerList
		})
		controllers.write(controllersContent)
		print 'Write done'
		exit()

	def generateNginxConfig(self):
		annotationList = self.mergeAnnotation()
		pprint.pprint(annotationList)
		location = ""
		configContent = """
		location /test {
		}
		"""
		configContent = self.Template.nginx_config.replace('{{ app }}', configContent)
		nginx = open(self.Config + '/app.conf', 'w')
		nginx.write(configContent)

	def compile(self):
		controllers = os.listdir(self.Input)
		for controller in controllers:
			# Controller must have header file
			if controller.endswith('.h'):
				self.compileFile(controller)
		self.generateNginxConfig()
		self.generateControllerActionMapping()