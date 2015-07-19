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
import pprint

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

	def initControllerParser(self):
		self.commentFlag = False
		self.bracketFlag = 0
		self.methodStack = {}
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

	def parseController(self, cppPath):
		print "PARSE : ", cppPath
		self.initControllerParser()
		annotationStorage = {}
		self.annotationStack = {}
		# Pattern recognition
		pattern = Pattern()
		pattern.setContext(self)
		# Compile file
		with open(cppPath, "r") as lines :
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
					if pattern.isMethod() and self.bracketFlag == 0:
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
							indexL = method_without_am.index('(')
							indexR = indexL
							while indexR > 0:
								if method_without_am[indexR] == ' ':
									break
								indexR = indexR - 1
							currentMethod = method_without_am[indexR : indexL]
							self.currentMethod = currentMethod
							self.methodStack[self.currentMethod] = {}
							self.methodStack[self.currentMethod]["Header"] = method_without_am[0 : indexR] + " " + className + "::" + currentMethod.strip()
							self.methodStack[self.currentMethod]["Block"] = ''
							indexL = method_without_am.index('(')
							indexR = method_without_am.index(')')
							self.methodStack[self.currentMethod]["Header"] += method_without_am[indexL : indexR + 1]
							arguments = method_without_am[indexL + 1 : indexR]
							argumentPairs = arguments.split(',')
							argumentList = []
							if len(argumentPairs) > 0:
								for argumentPair in argumentPairs:
									variableCom  = argumentPair.split(' ')
									variableName = variableCom[-1].strip()
									variableType = ''
									variableType = variableType.join(variableCom[1:len(variableCom) - 1]).strip()
									if (len(variableType) > 0) and (len(variableName) > 0):
										argumentList.append([variableType, variableName])
							self.annotationStack['@Argument'] = argumentList
							self.annotationInfo[self.currentClass]['Method'].append(
								{'Name': currentMethod, '@': self.annotationStack }
							)
							#print self.annotationInfo
						self.annotationStack = {}
						continue
					if pattern.isProperty() and self.bracketFlag == 0:
						am = False
						property_without_am = ' '
						if pattern.isPublic():
							am = True
							property_without_am = self.line.split('public')[1]
							self.stackPublic.append(property_without_am.strip())
						if pattern.isPrivate():
							am = True
							property_without_am = self.line.split('private')[1]
							self.stackPrivate.append(property_without_am.strip())
						if pattern.isProtected():
							am = True
							property_without_am = self.line.split('protected')[1]
							self.stackProtected.append(property_without_am.strip())
						if am is False:
							print property_without_am
							self.stackNonAccessModifier.append(property_without_am.strip())
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
					if pattern.isMethodStart():
						self.bracketFlag = 1
						continue
					if pattern.isMethodStop():
						self.bracketFlag = 0
						continue
					if self.currentMethod is not None:
						for i in range(0, len(line)):
							if line[i] == '{':
								self.bracketFlag += 1
							if line[i] == '}':
								self.bracketFlag -= 1
						if self.bracketFlag > 0:
							self.methodStack[self.currentMethod]["Block"] += line + '\n'
						continue
					print 'IGNORE', line
		print self.methodStack
		if self.currentClass is None:
			print 'Controller class does not exist !'
			exit()

	def generateHeader(self):
		self.headerContent += 'class ' + self.currentClass + "\n{\n"
		if len(self.stackPublic) > 0:
			self.headerContent += '\tpublic:\n'
		for publicItem in self.stackPublic:
			self.headerContent += '\t\t' + publicItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ";"
			self.headerContent += '\n'
		if len(self.stackPrivate) > 0:
			self.headerContent += '\tprivate:\n'
		for privateItem in self.stackPrivate:
			self.headerContent += '\t\t' + privateItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		if len(self.stackProtected) > 0:
			self.headerContent += '\tprotected:\n'
		for protectedItem in self.stackProtected:
			self.headerContent += '\t\t' + protectedItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		for protectedItem in self.stackNonAccessModifier:
			self.headerContent += '\t' + protectedItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		self.headerContent += '};'
		
	def generateSource(self):
		for methodName in self.methodStack:
			self.cppContent += self.methodStack[methodName]['Header'].rstrip('\n') + '\n'
			self.cppContent += '{\n'
			self.cppContent += self.methodStack[methodName]['Block'].rstrip('\n') + '\n'
			self.cppContent += '}\n'
		
		
	def compileFile(self, filePath):
		fileName = filePath.split(".")[0]
		self.controllerName = fileName.split("/")[-1]
		cppPath	   = self.Input + "/" + fileName + ".cpp"
		destHeaderPath = self.Output + "/" + fileName + ".h"
		destCppPath = self.Output + "/" + fileName + ".cpp"

		self.headerContent = ''
		self.cppContent = '#include "'+ self.controllerName + '.h"\n'
		self.parseController(cppPath)
		self.generateHeader()
		self.generateSource()
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
		ListController controllers;{{ controllers }}
		return controllers;
	}
}"""
		controllerList = ''
		hashMd5 = hashlib.md5()
		for className in self.annotationInfo:
			controllerList += tab(2) + 'controllers["' + className +'"] = (new Controller)' + tab(9) +'->setName("' + className + '")'
			for methodInfo in self.annotationInfo[className]['Method']:
				actionName = methodInfo['Name'].strip()
				hashMd5.update(className + '-' + actionName)
				hashAction = hashMd5.hexdigest()
				controllerList += tab(9) + '->addAction(' + tab(10) +'(new Action)' + tab(11) + '->setName("' + actionName +'")'
				controllerList += tab(11) + '->setHash("' + hashAction + '")'
				if len(methodInfo['@']['@Argument']) > 0:
					for argumentPair in methodInfo['@']['@Argument']:
						controllerList += tab(11) + '->addArgument(new ActionArgument("' + argumentPair[0] + '","' + argumentPair[1] + '"))'
				controllerList += tab(9) + ')'
			controllerList += ';'
		controllersContent = self.renderString(controllersTemplate, {
			'controllers' : controllerList
		})
		controllers.write(controllersContent)

	def generateNginxConfig(self):
		annotationList = self.mergeAnnotation()
		#pprint.pprint(annotationList)
		location = ""
		configContent = """
location / {
	app 123456789;
}"""
		configContent = self.Template.nginx_config.replace('{{ app }}', configContent)
		app_config = self.Config + '/app.conf'
		print app_config
		nginx = open(app_config, 'w')
		nginx.write(configContent)

	def compile(self):
		controllers = os.listdir(self.Input)
		for controller in controllers:
			# Controller must have header file
			if controller.endswith('.cpp'):
				self.compileFile(controller)
		self.generateNginxConfig()
		self.generateControllerActionMapping()