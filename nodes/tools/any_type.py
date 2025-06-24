"""
AnyType for UniversalToolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AnyType class for accepting any input type in nodes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""
    def __eq__(self, __value: object) -> bool:
        return True
    def __ne__(self, __value: object) -> bool:
        return False 