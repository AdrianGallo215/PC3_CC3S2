from abc import ABC, abstractmethod

class LogicOperator(ABC):

    @abstractmethod
    def evaluate(self, codicion1, codicion2):
        pass

class AndOperator(LogicOperator):

    def evaluate(self, condicion1, condicion2):
        return condicion1 & condicion2
    
class OrOperator(LogicOperator):

    def evaluate(self, condicion1, condicion2):
        return condicion1 | condicion2
    
class NotOperator(LogicOperator):

    def evaluate(self, condicion1, condicion2):
        return condicion1 - condicion2
    
class XorOperator(LogicOperator):

    def evaluate(self, condicion1, condicion2):
        return condicion1 ^ condicion2
