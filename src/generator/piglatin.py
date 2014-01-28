from . import AbstractCodeGenerator
from abc import ABCMeta

import inflection
import os
import pystache
import re
import string

class PigCodeGenerator(AbstractCodeGenerator):
    __metaclass__ = ABCMeta

    PIG_TYPE           = 'hadoop_type'
    
    equivalence = {
        'string'  : {
            PIG_TYPE            : 'chararray'
        },
        'int'     : {
            PIG_TYPE            : 'int'
        },
        'long'     : {
            PIG_TYPE            : 'long'
        },
        'float'     : {
            PIG_TYPE            : 'float'
        },
        'double'     : {
            PIG_TYPE            : 'double'
        },
        'boolean'     : {
            PIG_TYPE            : 'boolean'
        }
    }

    def import_maker(self, library, schema = None):
        pass

class PigLatinComparerGenerator(PigCodeGenerator):
    def make_file_name(self, schema):
        return os.path.join('/'.join(schema.namespace.split('.')),
                            '{0}_comparer.pig'.format(underscore.camelize(schema.name)))

    def code_generator(self, schema):
        renderer      = pystache.Renderer()
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'piglatin',
                                     'diff_finder.tpl.pig')

        
        schema_size = len(schema.fields)
        
        qakey_list = [ field for field in schema.fields if field.get_prop('qa_key') ]
        qakey_size = len(qakey_list)

        qavalue_list = [ field for field in schema.fields if not field.get_prop('qa_key') ]
        qavalue_size = len(qavalue_list)

        return renderer.render_path(template_path,
                                    { 'namespace'             : schema.namespace,
                                      'entity_name'           : inflection.underscore(schema.name),
                                      'items'                 : [ { 'name_underscore'           : inflection.underscore(field.name),
                                                                    'type_pig'                  : self.get_equivalence(field, self.PIG_TYPE),
                                                                    'position_enum'             : pos,
                                                                    'position_last'             : pos == schema_size - 1,
                                                                    'separator_comma'           : '' if pos == schema_size - 1 else ', ',
                                                                    'separator_comma_semicolon' : ';' if pos == schema_size - 1 else ', '
                                                                  } for pos, field in enumerate(schema.fields) ],
                                      'qakey'                 : [ { 'name_underscore'           : inflection.underscore(field.name),
                                                                    'position_enum'             : pos,
                                                                    'position_last'             : pos == qakey_size - 1,
                                                                    'separator_comma'           : '' if pos == qakey_size - 1 else ', ',
                                                                    'separator_and_comma'       : ',' if pos == qakey_size - 1 else ' AND ',
                                                                    'separator_and_semicolon'   : ';' if pos == qakey_size - 1 else ' AND '
                                                                  } for pos, field in enumerate(qakey_list) ],
                                      'qavalue'               : [ { 'name_underscore'           : inflection.underscore(field.name),
                                                                    'position_enum'             : pos,
                                                                    'position_last'             : pos == qavalue_size - 1,
                                                                    'separator_comma'           : '' if pos == qavalue_size - 1 else ', ',
                                                                    'separator_comma_semicolon' : ';' if pos == qavalue_size - 1 else ', ',
                                                                  } for pos, field in enumerate(qavalue_list) ]
                                    })

