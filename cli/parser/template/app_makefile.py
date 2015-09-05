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

app_makefile = """
BIN = /usr/bin

all: server service client

server:
	pen compile
	@cd gen && make

service:
	@cd src/_go_service && make

client:
	@cd src/_ts_client && make

install:
	@cd src/_go_service && make install
	@cp ./bin/app.sh $(BIN)/app
	@chmod +x $(BIN)/app
	@mkdir -p $(BIN)/app-bin
	@cp ./bin/app-* $(BIN)/app-bin/
	@chmod +x $(BIN)/app-bin/*

test:
	@cd gen && make test
	@cd src/_go_service && make test
	@cd src/_ts_client && make test

clean:
	@cd src/_go_service && make clean
	@cd src/_ts_client && make clean
	rm -rf $(BIN)/app
	rm -rf $(BIN)/app-bin

.PHONY: clean test server service client
"""