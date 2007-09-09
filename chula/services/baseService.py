"""
Base class from which all service classes inherit.  The objective here is
to abstract away configuration logic that all service classes might need.
"""

class BaseService(object):
    
    def _appendAttributes(self):
        """
        Add/replace searcher attributes
        
        @return: Dictionary
        """
        return {}
        
    def _appendWsArgs(self):
         """
         Add/replace wsFetch attributes
         
         @return: Dictionary
         """
         return {}

