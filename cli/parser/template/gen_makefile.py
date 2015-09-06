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

gen_makefile = """
GCC		  = gcc
G++       = g++
CCVER     = c++14
BUILD     = -std=$(CCVER) -Wall -O3
DEBUG     = -std=$(CCVER) -pipe -g0 -fno-inline -Wall -pthread
TESTF	  = -std=$(CCVER) -g -L/opt/gtest/lib -lgtest -lgtest_main -lpthread -I/opt/gtest/include
INCLUDE   = /usr/lib/pen
OBJECTD   = object
SOURCE    = $(shell find container excutable -name *.cpp)
OBJECTS   = $(shell find object/container -name *.o)
OBJECTCLI = $(shell find object/excutable/cli -name *.o)
OBJECT    = $(addprefix $(OBJECTD)/, $(patsubst %.cpp, %.o, $(SOURCE)))
FLAGS     = $(BUILD)

all: object

object: $(OBJECT)

$(OBJECTD)/%.o: %.cpp
	$(G++) -c $(FLAGS) -I./container -I$(INCLUDE) -lpen $< -o $@ 2>&1

$(OBJECT): mk_object

mk_object:
	for file in $(OBJECT) ; do if [ ! -f $$file ]; then mkdir -p $$file && rm -rf $$file; fi done

cli:
	mkdir -p ../bin
	$(G++) $(OBJECTS) $(OBJECTCLI) -I./container -I$(INCLUDE) -lpen -o ../bin/app-cli

install:
	cp -rf $(BINARY_CLI) /usr/bin/$(BINARY_CLI)
	cp -rf $(BINARY_SERVICE) /usr/bin/$(BINARY_SERVICE)
.PHONY: all
"""