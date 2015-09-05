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

cli_main = """// AUTO GENERATED
#include <app/command.h>
{{ listInclude }}
int main(int argc, char* argv[])
{
Cli *cli = new Cli();
Input *input = new Input();
Output *output = new Output();
{{ listInstance }}
cli ->parse(argc, argv)
	->setInput(input)
	->setOutput(output)
	->execute();
delete cli;
return 0;
}
"""