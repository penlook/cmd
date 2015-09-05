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

import argparse
import sys
from os import *
from parser import *

#$ pen build app
class Build(argparse.Action):
	
	def prepare(self):
		system("pkill pendev")
		self.cwd += '/gen/_production'
		chdir(self.cwd)
		# Clean up system
		system("pkill pendev && service nginx stop")

	def parse(self):
		app = App()
		app.setRoot(self.root)\
		   .parse()
		system("cd .. && find -name *.cpp ")
		exit()

	def config(self):
		system('./config.sh')

	def build(self):
		system('./build.sh')

	def __call__(self, parser, args, values, option_string = None):
		self.root = getcwd()
		if len(values) > 0 :
			self.root += "/" + values[0]
		chdir(self.root)
		self.cwd = self.root

		self.prepare()
		self.parse()
		self.config()
		self.build()