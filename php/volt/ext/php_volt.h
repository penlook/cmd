
/* This file was generated automatically by Zephir do not modify it! */

#ifndef PHP_VOLT_H
#define PHP_VOLT_H 1

#ifdef PHP_WIN32
#define ZEPHIR_RELEASE 1
#endif

#include "kernel/globals.h"

#define PHP_VOLT_NAME        "volt"
#define PHP_VOLT_VERSION     "0.0.1"
#define PHP_VOLT_EXTNAME     "volt"
#define PHP_VOLT_AUTHOR      ""
#define PHP_VOLT_ZEPVERSION  "0.7.1b"
#define PHP_VOLT_DESCRIPTION ""



ZEND_BEGIN_MODULE_GLOBALS(volt)

	int initialized;

	/* Memory */
	zephir_memory_entry *start_memory; /**< The first preallocated frame */
	zephir_memory_entry *end_memory; /**< The last preallocate frame */
	zephir_memory_entry *active_memory; /**< The current memory frame */

	/* Virtual Symbol Tables */
	zephir_symbol_table *active_symbol_table;

	/** Function cache */
	HashTable *fcache;

	zephir_fcall_cache_entry *scache[ZEPHIR_MAX_CACHE_SLOTS];

	/* Cache enabled */
	unsigned int cache_enabled;

	/* Max recursion control */
	unsigned int recursive_lock;

	/* Global constants */
	zval *global_true;
	zval *global_false;
	zval *global_null;
	
ZEND_END_MODULE_GLOBALS(volt)

#ifdef ZTS
#include "TSRM.h"
#endif

ZEND_EXTERN_MODULE_GLOBALS(volt)

#ifdef ZTS
	#define ZEPHIR_GLOBAL(v) TSRMG(volt_globals_id, zend_volt_globals *, v)
#else
	#define ZEPHIR_GLOBAL(v) (volt_globals.v)
#endif

#ifdef ZTS
	#define ZEPHIR_VGLOBAL ((zend_volt_globals *) (*((void ***) tsrm_ls))[TSRM_UNSHUFFLE_RSRC_ID(volt_globals_id)])
#else
	#define ZEPHIR_VGLOBAL &(volt_globals)
#endif

#define ZEPHIR_API ZEND_API

#define zephir_globals_def volt_globals
#define zend_zephir_globals_def zend_volt_globals

extern zend_module_entry volt_module_entry;
#define phpext_volt_ptr &volt_module_entry

#endif
