from . import AbstractCodeGenerator
from abc import ABCMeta

import inflection
import os
import pystache
import string

class JavaHadoopCodeGenerator(AbstractCodeGenerator):
    __metaclass__ = ABCMeta

    JAVA_TYPE          = 'java_type'
    HADOOP_TYPE        = 'hadoop_type'
    HADOOP_TYPE_SIZE   = 'hadoop_type_size'
    HADOOP_GET_VALUE   = 'hadoop_get_value'
    DEFAULT_VALUE      = 'default_value'
    PARSER_TEMPLATE    = 'parser_template'
    HASH_CODE_TEMPLATE = 'hash_code_template'

    equivalence = {
        'string'  : {
            JAVA_TYPE           : 'String',
            HADOOP_TYPE         : 'Text',
            HADOOP_TYPE_SIZE    : 0,
            HADOOP_GET_VALUE    : 'toString()',
            DEFAULT_VALUE       : '""',
            PARSER_TEMPLATE     : '{0}'
        },
        'int'     : {
            JAVA_TYPE           : 'int',
            HADOOP_TYPE         : 'IntWritable',
            HADOOP_TYPE_SIZE    : 4,
            HADOOP_GET_VALUE    : 'get()',
            DEFAULT_VALUE       : '0',
            PARSER_TEMPLATE     : 'Integer.parseInt({0})'
        },
        'long'     : {
            JAVA_TYPE           : 'long',
            HADOOP_TYPE         : 'LongWritable',
            HADOOP_TYPE_SIZE    : 8,
            HADOOP_GET_VALUE    : 'get()',
            DEFAULT_VALUE       : '0L',
            PARSER_TEMPLATE     : 'Long.parseLong({0})'
        },
        'float'     : {
            JAVA_TYPE           : 'float',
            HADOOP_TYPE         : 'FloatWritable',
            HADOOP_TYPE_SIZE    : 4,
            HADOOP_GET_VALUE    : 'get()',
            DEFAULT_VALUE       : '0.0f',
            PARSER_TEMPLATE     : 'Float.parseFloat({0})'
        },
        'double'     : {
            JAVA_TYPE           : 'double',
            HADOOP_TYPE         : 'DoubleWritable',
            HADOOP_TYPE_SIZE    : 8,
            HADOOP_GET_VALUE    : 'get()',
            DEFAULT_VALUE       : '0.0d',
            PARSER_TEMPLATE     : 'Double.parseDouble({0})'
        },
        'boolean'     : {
            JAVA_TYPE           : 'boolean',
            HADOOP_TYPE         : 'BooleanWritable',
            HADOOP_TYPE_SIZE    : 1,
            HADOOP_GET_VALUE    : 'get()',
            DEFAULT_VALUE       : 'false',
            PARSER_TEMPLATE     : 'Boolean.parseBoolean({0})'
        }
    }

    def import_maker(self, library, schema = None):
        auxLibrary = set(library)
        if schema is not None:
          for field in schema.fields:
              auxLibrary.add('org.apache.hadoop.io.{0}'.format(self.get_equivalence(field, self.HADOOP_TYPE)))

        return [{ 'import': lib } for lib in sorted(auxLibrary) ]

class JavaHadoopEntityGenerator(JavaHadoopCodeGenerator):
    def make_file_name(self, schema):
        return os.path.join('/'.join(schema.namespace.split('.')),
                            '{0}.java'.format(inflection.camelize(schema.name)))

    def code_generator(self, schema):
        renderer      = pystache.Renderer()
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'mapreduce',
                                     'writable_comparable_class.tpl.java')

        return renderer.render_path(template_path,
                                    { 'namespace'             : schema.namespace,
                                      'class_name'            : inflection.camelize(schema.name),
                                      'imports'               : self.import_maker(['java.io.DataInput',
                                                                                   'java.io.DataOutput',
                                                                                   'java.io.IOException',
                                                                                   'org.apache.hadoop.io.WritableComparable'],
                                                                         schema),
                                      'items'                 : [ { 'name_cammel'         : inflection.camelize(field.name),
                                                                    'name_lower_cammel'   : inflection.camelize(field.name, False),
                                                                    'name_underscore'     : inflection.underscore(field.name),
                                                                    'type_basic'          : self.get_equivalence(field, self.JAVA_TYPE),
                                                                    'type_hadoop'         : self.get_equivalence(field, self.HADOOP_TYPE),
                                                                    'order_ascending'     : field.order.lower() != 'descending' if field.order else False,
                                                                    'order_descending'    : field.order.lower() == 'descending' if field.order else False,
                                                                    'position_enum'       : pos,
                                                                    'position_first'      : pos == 0,
                                                                    'doc'                 : field.doc } for pos, field in enumerate(schema.fields) ] } )

class JavaHadoopComparatorGenerator(JavaHadoopCodeGenerator):

    ORDER = 0
    GROUPING = 1

    def __init__(self, sortMode):
        self.sortMode = sortMode

    def make_file_name(self, schema):
        return os.path.join('/'.join(schema.namespace.split('.')),
                            '{0}{1}.java'.format(inflection.camelize(schema.name),
                                                                'GroupingComparator' if self.sortMode == JavaHadoopComparatorGenerator.GROUPING else 'OrderComparator'))

    def code_generator(self, schema):
        renderer      = pystache.Renderer()
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'mapreduce',
                                     'raw_comparator.tpl.java')


        return renderer.render_path(template_path,
                                    { 'namespace'             : schema.namespace,
                                      'class_name'            : inflection.camelize(('{0}GroupingComparator' if self.sortMode == JavaHadoopComparatorGenerator.GROUPING else '{0}OrderComparator').format(schema.name)),
                                      'class_name_container'  : inflection.camelize(schema.name),
                                      'imports'               : self.import_maker( ['java.io.IOException',
                                                                                    'org.apache.hadoop.io.RawComparator',
                                                                                    'org.apache.hadoop.io.WritableComparator',
                                                                                    'org.apache.hadoop.io.WritableUtils' ],
                                                                                  schema),
                                      'items'                 : [ { 'name_cammel'         : inflection.camelize(field.name),
                                                                    'name_underscore'     : inflection.camelize(inflection.underscore(field.name)),
                                                                    'comparator_name'     : inflection.camelize('{0}Comparator'.format(field.name)),
                                                                    'comparator_obj'      : '{0}.Comparator'.format(self.get_equivalence(field, self.HADOOP_TYPE)),
                                                                    'order_ascending'     : field.order.lower() != 'descending' if field.order else True,
                                                                    'order_descending'    : field.order.lower() == 'descending' if field.order else False,
                                                                    'order_ignore'        : (field.order.lower() == 'ignore' and self.sortMode == JavaHadoopComparatorGenerator.GROUPING) if field.order else False,
                                                                    'size_name'           : 'FIELD_{0}_SIZE'.format(inflection.underscore(field.name).upper()),
                                                                    'size_value'          : self.get_equivalence(field, self.HADOOP_TYPE_SIZE) } for pos, field in enumerate(schema.fields) ] } )

class JavaHadoopParser(JavaHadoopCodeGenerator):
    def make_file_name(self, schema):
        return os.path.join('/'.join(schema.namespace.split('.')),
                            '{0}Parser.java'.format(inflection.camelize(schema.name)))

    def code_generator(self, schema):
        renderer      = pystache.Renderer()
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'mapreduce',
                                     'parser_class.tpl.java')

        return renderer.render_path(template_path,
                                    { 'namespace'             : schema.namespace,
                                      'class_name'            : inflection.camelize('{0}Parser'.format(schema.name)),
                                      'class_name_container'  : inflection.camelize(schema.name),
                                      'imports'               : self.import_maker(['java.io.IOException',
                                                                                   'org.apache.hadoop.io.RawComparator',
                                                                                   'org.apache.hadoop.io.WritableComparator',
                                                                                   'org.apache.hadoop.io.WritableUtils'],
                                                                                 schema),
                                      'items'                 : [ { 'name_cammel'         : inflection.camelize(field.name),
                                                                    'name_underscore'     : inflection.underscore(field.name),
                                                                    'position_name'       : 'FIELD_{0}_POSITION'.format(inflection.underscore(field.name).upper()),
                                                                    'position_value'      : pos,
                                                                    'value_parser'        : self.get_equivalence(field, self.PARSER_TEMPLATE).format('tmp'),
                                                                    'value_default'       : field.default if field.default else self.get_equivalence(field, self.DEFAULT_VALUE),
                                                                    'value_nullable'      : field.get_prop('nullable') if field.get_prop('nullable') else False } for pos, field in enumerate(schema.fields) ] } )
