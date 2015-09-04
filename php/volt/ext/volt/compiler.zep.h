
extern zend_class_entry *volt_compiler_ce;

ZEPHIR_INIT_CLASS(Volt_Compiler);

PHP_METHOD(Volt_Compiler, __construct);
PHP_METHOD(Volt_Compiler, setDI);
PHP_METHOD(Volt_Compiler, getDI);
PHP_METHOD(Volt_Compiler, setOptions);
PHP_METHOD(Volt_Compiler, setOption);
PHP_METHOD(Volt_Compiler, getOption);
PHP_METHOD(Volt_Compiler, getOptions);
PHP_METHOD(Volt_Compiler, fireExtensionEvent);
PHP_METHOD(Volt_Compiler, addExtension);
PHP_METHOD(Volt_Compiler, getExtensions);
PHP_METHOD(Volt_Compiler, addFunction);
PHP_METHOD(Volt_Compiler, getFunctions);
PHP_METHOD(Volt_Compiler, addFilter);
PHP_METHOD(Volt_Compiler, getFilters);
PHP_METHOD(Volt_Compiler, setUniquePrefix);
PHP_METHOD(Volt_Compiler, getUniquePrefix);
PHP_METHOD(Volt_Compiler, attributeReader);
PHP_METHOD(Volt_Compiler, functionCall);
PHP_METHOD(Volt_Compiler, resolveTest);
PHP_METHOD(Volt_Compiler, resolveFilter);
PHP_METHOD(Volt_Compiler, expression);
PHP_METHOD(Volt_Compiler, _statementListOrExtends);
PHP_METHOD(Volt_Compiler, compileForeach);
PHP_METHOD(Volt_Compiler, compileForElse);
PHP_METHOD(Volt_Compiler, compileIf);
PHP_METHOD(Volt_Compiler, compileElseIf);
PHP_METHOD(Volt_Compiler, compileCache);
PHP_METHOD(Volt_Compiler, compileSet);
PHP_METHOD(Volt_Compiler, compileDo);
PHP_METHOD(Volt_Compiler, compileReturn);
PHP_METHOD(Volt_Compiler, compileAutoEscape);
PHP_METHOD(Volt_Compiler, compileEcho);
PHP_METHOD(Volt_Compiler, compileInclude);
PHP_METHOD(Volt_Compiler, compileMacro);
PHP_METHOD(Volt_Compiler, compileCall);
PHP_METHOD(Volt_Compiler, _statementList);
PHP_METHOD(Volt_Compiler, _compileSource);
PHP_METHOD(Volt_Compiler, compileString);
PHP_METHOD(Volt_Compiler, compileFile);
PHP_METHOD(Volt_Compiler, compile);
PHP_METHOD(Volt_Compiler, getTemplatePath);
PHP_METHOD(Volt_Compiler, getCompiledTemplatePath);
PHP_METHOD(Volt_Compiler, parse);

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler___construct, 0, 0, 0)
	ZEND_ARG_OBJ_INFO(0, view, Phalcon\\Mvc\\ViewBaseInterface, 1)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_setdi, 0, 0, 1)
	ZEND_ARG_OBJ_INFO(0, dependencyInjector, Phalcon\\DiInterface, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_setoptions, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, options, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_setoption, 0, 0, 2)
	ZEND_ARG_INFO(0, option)
	ZEND_ARG_INFO(0, value)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_getoption, 0, 0, 1)
	ZEND_ARG_INFO(0, option)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_fireextensionevent, 0, 0, 1)
	ZEND_ARG_INFO(0, name)
	ZEND_ARG_INFO(0, arguments)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_addextension, 0, 0, 1)
	ZEND_ARG_INFO(0, extension)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_addfunction, 0, 0, 2)
	ZEND_ARG_INFO(0, name)
	ZEND_ARG_INFO(0, definition)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_addfilter, 0, 0, 2)
	ZEND_ARG_INFO(0, name)
	ZEND_ARG_INFO(0, definition)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_setuniqueprefix, 0, 0, 1)
	ZEND_ARG_INFO(0, prefix)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_attributereader, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, expr, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_functioncall, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, expr, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_resolvetest, 0, 0, 2)
	ZEND_ARG_ARRAY_INFO(0, test, 0)
	ZEND_ARG_INFO(0, left)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_resolvefilter, 0, 0, 2)
	ZEND_ARG_ARRAY_INFO(0, filter, 0)
	ZEND_ARG_INFO(0, left)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_expression, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, expr, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler__statementlistorextends, 0, 0, 1)
	ZEND_ARG_INFO(0, statements)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileforeach, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileif, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileelseif, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilecache, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileset, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compiledo, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilereturn, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileautoescape, 0, 0, 2)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileecho, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compileinclude, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilemacro, 0, 0, 2)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilecall, 0, 0, 2)
	ZEND_ARG_ARRAY_INFO(0, statement, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler__statementlist, 0, 0, 1)
	ZEND_ARG_ARRAY_INFO(0, statements, 0)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler__compilesource, 0, 0, 1)
	ZEND_ARG_INFO(0, viewCode)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilestring, 0, 0, 1)
	ZEND_ARG_INFO(0, viewCode)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compilefile, 0, 0, 2)
	ZEND_ARG_INFO(0, path)
	ZEND_ARG_INFO(0, compiledPath)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_compile, 0, 0, 1)
	ZEND_ARG_INFO(0, templatePath)
	ZEND_ARG_INFO(0, extendsMode)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO_EX(arginfo_volt_compiler_parse, 0, 0, 1)
	ZEND_ARG_INFO(0, viewCode)
ZEND_END_ARG_INFO()

ZEPHIR_INIT_FUNCS(volt_compiler_method_entry) {
	PHP_ME(Volt_Compiler, __construct, arginfo_volt_compiler___construct, ZEND_ACC_PUBLIC|ZEND_ACC_CTOR)
	PHP_ME(Volt_Compiler, setDI, arginfo_volt_compiler_setdi, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getDI, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, setOptions, arginfo_volt_compiler_setoptions, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, setOption, arginfo_volt_compiler_setoption, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getOption, arginfo_volt_compiler_getoption, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getOptions, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, fireExtensionEvent, arginfo_volt_compiler_fireextensionevent, ZEND_ACC_PUBLIC|ZEND_ACC_FINAL)
	PHP_ME(Volt_Compiler, addExtension, arginfo_volt_compiler_addextension, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getExtensions, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, addFunction, arginfo_volt_compiler_addfunction, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getFunctions, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, addFilter, arginfo_volt_compiler_addfilter, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getFilters, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, setUniquePrefix, arginfo_volt_compiler_setuniqueprefix, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getUniquePrefix, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, attributeReader, arginfo_volt_compiler_attributereader, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, functionCall, arginfo_volt_compiler_functioncall, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, resolveTest, arginfo_volt_compiler_resolvetest, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, resolveFilter, arginfo_volt_compiler_resolvefilter, ZEND_ACC_FINAL|ZEND_ACC_PROTECTED)
	PHP_ME(Volt_Compiler, expression, arginfo_volt_compiler_expression, ZEND_ACC_FINAL|ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, _statementListOrExtends, arginfo_volt_compiler__statementlistorextends, ZEND_ACC_FINAL|ZEND_ACC_PROTECTED)
	PHP_ME(Volt_Compiler, compileForeach, arginfo_volt_compiler_compileforeach, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileForElse, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileIf, arginfo_volt_compiler_compileif, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileElseIf, arginfo_volt_compiler_compileelseif, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileCache, arginfo_volt_compiler_compilecache, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileSet, arginfo_volt_compiler_compileset, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileDo, arginfo_volt_compiler_compiledo, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileReturn, arginfo_volt_compiler_compilereturn, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileAutoEscape, arginfo_volt_compiler_compileautoescape, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileEcho, arginfo_volt_compiler_compileecho, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileInclude, arginfo_volt_compiler_compileinclude, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileMacro, arginfo_volt_compiler_compilemacro, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileCall, arginfo_volt_compiler_compilecall, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, _statementList, arginfo_volt_compiler__statementlist, ZEND_ACC_FINAL|ZEND_ACC_PROTECTED)
	PHP_ME(Volt_Compiler, _compileSource, arginfo_volt_compiler__compilesource, ZEND_ACC_PROTECTED)
	PHP_ME(Volt_Compiler, compileString, arginfo_volt_compiler_compilestring, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compileFile, arginfo_volt_compiler_compilefile, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, compile, arginfo_volt_compiler_compile, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getTemplatePath, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, getCompiledTemplatePath, NULL, ZEND_ACC_PUBLIC)
	PHP_ME(Volt_Compiler, parse, arginfo_volt_compiler_parse, ZEND_ACC_PUBLIC)
	PHP_FE_END
};
