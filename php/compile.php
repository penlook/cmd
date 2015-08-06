<?php
use Volt\Compiler;

$compiler = new Compiler();
$compiler->setOptions(array(
	"compiledPath"      => "./views/",
	"compiledExtension" => ".compiled"
));

echo $compiler->compileString('{{ "hello" }}') . "\n\n";