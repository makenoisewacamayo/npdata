from . import AbstractCodeGenerator
from UserString import MutableString
import string

class PigCodeGenerator(AbstractCodeGenerator):

    def __init__(self, schema):
        self.schema = schema

    def loader(self, name = '', path = '{file}', delimiter = '\\t'):
        builder = []
        builder.append('{0} = LOAD \'{1}\' USING PigStorage(\'{2}\') AS ('.format(self.schema.name, path, delimiter))
        builder.append(',\n'.join(['    {0:<32} : {1}'.format(field.name, self.__type_map(field)) for field in self.schema.fields]))
        builder.append(');')
        return string.join(builder, '\n')


    def __type_map(self, field):
        if field.type is PrimitiveSchema:
            self.fullname
        else:
            print (field.type)
            return field.type 

"""
    def loader(self, fields, name, path, delimiter='\\t'):
        builder = MutableString()
        builder += '{0} = LOAD \'{1}\' USING PigStorage(\'{2}\') AS (\n'.format(name, path, delimiter)
        builder += string.join(['    {0:<32} : {1}'.format(aux.name, aux.type if aux.type != 'string' else 'chararray') for aux in fields], ',\n')
        builder += '\n);'
        return builder.__str__()

    def comparer(self, fields, actual, expected, output, delimiter='\\t',):
        keys = [aux.name for aux in fields if aux.key]

        component  = [ ]
        component += [ self.loader(fields, 'expected', expected if expected else '$expected' , delimiter) ]
        component += [ self.loader(fields, 'actual', actual if actual else '$actual', delimiter) ]
        component += [ 'comparer = JOIN expected BY ({0}) FULL, actual BY ({0});'.format(', '.join(keys))]
        component += [ self.__split_generator__(fields) ]
        component += self.__diff_generator__(keys, fields, output, delimiter)
        return '\n\n'.join(component)

    def store(self, path, delimiter):
        return 'STORE container INTO \'{0}\' USING PigStorage (\'{1}\');'.format(path if path else '$output', delimiter)

    def __split_generator__(self, fields):
        spaces = ',\n' + ' ' * 20

        builder = MutableString()
        builder += 'SPLIT comparer INTO '
        builder += spaces.join(['filter_{0} IF ({1}::{0} is not null) AND ({2}::{0} is not null) AND ({1}::{0} != {2}::{0})'.format(aux.name, 'expected', 'actual') for aux in fields if not aux.key])
        builder += spaces + 'split_exp IF ' + ' AND '.join(['{0}::{1} is null'.format('actual', aux.name) for aux in fields if aux.key])
        builder += spaces + 'split_act IF ' + ' AND '.join(['{0}::{1} is null'.format('expected', aux.name) for aux in fields if aux.key])
        builder += ';'
        return builder.__str__()

    def __diff_generator__(self, keys, fields, output, delimiter):
        diff_template = '''diff_{0} = FOREACH filter_{0} {{
    e = (chararray) expected::{0};
    a = (chararray) actual::{0};
    GENERATE {1}, e as expected, a as actual;
}};

STORE diff_{0} INTO \'{2}/{0}\' USING PigStorage (\'{3}\');'''

        side_template = '''just_{0} = FOREACH {1} {{
    GENERATE {2};
}};

STORE just_{0} INTO \'{3}/just_{0}\' USING PigStorage (\'{4}\');'''
        expected_fields = ', '.join(['expected::{0}'.format(key.name) for key in fields])
        actual_fields = ', '.join(['actual::{0}'.format(key.name) for key in fields])

        build  = [ ]
        build += [ diff_template.format(aux.name, expected_fields, output, delimiter) for aux in fields if not aux.key ]
        build += [ side_template.format('expected', 'split_exp', expected_fields, output, delimiter ) ]
        build += [ side_template.format('actual', 'split_act', actual_fields, output, delimiter) ]

        return build

    def __union_generator__(self, fields):
        spaces = ',\n' + ' ' * 18
        component  = [ 'diff_{0}'.format(aux.name) for aux in fields if not aux.key ]
        component += [ 'side_exp', 'side_act' ]

        builder = MutableString()
        builder += 'container = UNION '
        builder += spaces.join(component)
        builder += ';'
        return [ builder.__str__() ]
"""