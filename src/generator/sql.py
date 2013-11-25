
from . import AbstractCodeGenerator
from UserString import MutableString
import string

class SqlCodeGenerator(AbstractCodeGenerator):    
    def comparer(self, fields, delimiter='\\t'):
        component  = [ 
                self.__table_maker__(fields, 'expected'), 
                self.__loader_maker__(fields, 'expected', delimiter),
                self.__table_maker__(fields, 'actual'),
                self.__loader_maker__(fields, 'actual', delimiter)
                ]
        return string.join(component, '\n\n')

    def loader(self, fields, name, delimiter='\\t'):
        return self.create_table(fields, name)

    def store(self, path, delimiter):
        return ''
        
    def __table_maker__(self, fields, name):
        builder = MutableString()
        builder = 'CREATE TABLE  #{0} (\n'.format(name)
        builder += string.join(['    {0:<32} : {1}'.format(aux.name, self.get_type(aux)) for aux in fields], ',\n')
        builder += ');\n'
        builder += 'COMMIT;'

        return builder.__str__()

    def __loader_maker__(self, fields, name, delimiter='\\t'):
        builder = MutableString()
        builder += 'LOAD TABLE  #{0} (\n'.format(name)
        builder += string.join(['    {0:<32}'.format(aux.name) for aux in fields], '\'{0}\',\n'.format(delimiter)) + '\'\\x0d\\x0a\'\n'
        builder += ') FROM \'{{file}}\'\n' 
        builder += 'ESCAPES OFF QUOTES OFF';
        return builder.__str__()

    def get_type(self, field):
        if(field.type == 'int'):
            return 'int'
        else:
            return 'varchar(255)'
