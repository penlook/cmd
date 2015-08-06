<?php
use Volt\Compiler;

$compiler = new Compiler();
$compiler->setOptions(array(
	"compiledPath"      => "./views/",
	"compiledExtension" => ".compiled"
));

$compiler->compileFile('views/app.volt', 'views/app.cpp');