from abc import ABCMeta, abstractmethod

class AbstractCodeGenerator:
    __metaclass__ = ABCMeta

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
