from abc import ABCMeta, abstractmethod
from avro.schema import PrimitiveSchema

class AbstractCodeGenerator:
    __metaclass__ = ABCMeta

    equivalence = {}

    def get_equivalence(self, field, value):
        if not type(field.type) is PrimitiveSchema:
            raise Exception('Only primitive schemas are implemented')

        if not field.type.type in self.equivalence:
            raise Exception('Map for {0} was not found' % field.type.type)

        if not value in self.equivalence[field.type.type]:
            raise Exception('{0} equivalence was not found' % value)

        return self.equivalence[field.type.type][value]

    @abstractmethod
    def make_file_name(self, schema):
        return NotImplemented

    @abstractmethod
    def code_generator(self, schema):
        return NotImplemented


#    def comparer(self, fields, delimiter='\\t', actual='{{actual}}', expected='{{expected}}', output='{{output}}'):
#        return NotImplemented

#    @abstractmethod
#    def loader(self, fields, name, delimiter='\\t'):
#        return NotImplemented

#    @abstractmethod
#    def store(self, path, delimiter):
#        return NotImplemented
