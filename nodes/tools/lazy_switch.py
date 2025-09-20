"""
Lazy Switch Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lazy switch functionality adapted from kjnodes.
Controls flow of execution based on a boolean switch with lazy evaluation.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

# Try to import IO.ANY from ComfyUI's typing system
try:
    from comfy.comfy_types.node_typing import IO
    ANY_TYPE = IO.ANY
except ImportError:
    # Fallback for older ComfyUI versions or different typing systems
    try:
        from comfy_extras.nodes_custom_sampler import AnyType
        ANY_TYPE = AnyType("*")
    except ImportError:
        # Create a simple ANY type fallback
        class AnyType(str):
            def __ne__(self, __value: object) -> bool:
                return False
        
        ANY_TYPE = AnyType("*")


class LazySwitchKJ_UTK:
    """
    Lazy Switch node that controls flow of execution based on a boolean switch.
    
    This node implements lazy evaluation, meaning it only evaluates the branch
    that will actually be used based on the switch value. This can improve
    performance by avoiding unnecessary computations.
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("BOOLEAN", {"tooltip": "Boolean value to control which input is returned"}),
                "on_false": (ANY_TYPE, {
                    "lazy": True,
                    "tooltip": "Value returned when switch is False"
                }),
                "on_true": (ANY_TYPE, {
                    "lazy": True,
                    "tooltip": "Value returned when switch is True"
                }),
            },
        }

    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("output",)
    FUNCTION = "switch"
    CATEGORY = "UniversalToolkit/Tools"
    
    DESCRIPTION = """
Controls flow of execution based on a boolean switch.

This node implements lazy evaluation - it only processes the input
that will actually be used based on the switch value. This can 
significantly improve performance by avoiding unnecessary computations
in complex workflows.

Features:
- **Lazy Evaluation**: Only evaluates the selected branch
- **Any Type Support**: Works with any data type (images, masks, strings, etc.)
- **Flow Control**: Essential for conditional workflow execution
- **Performance Optimization**: Reduces unnecessary processing

Usage:
- Connect your boolean condition to the 'switch' input
- Connect the value for False condition to 'on_false'  
- Connect the value for True condition to 'on_true'
- The node will output the appropriate value based on the switch

Common use cases:
- Conditional image processing pipelines
- A/B testing different parameters
- Workflow branching based on user input
- Performance optimization in complex workflows
"""

    def check_lazy_status(self, switch, on_false=None, on_true=None):
        """
        Check which inputs are needed for lazy evaluation.
        
        This method tells ComfyUI which inputs it needs to evaluate
        based on the current switch value.
        """
        if switch and on_true is None:
            return ["on_true"]
        if not switch and on_false is None:
            return ["on_false"]

    def switch(self, switch, on_false=None, on_true=None):
        """
        Switch between two values based on a boolean condition.
        
        Args:
            switch: Boolean value determining which input to return
            on_false: Value to return when switch is False
            on_true: Value to return when switch is True
            
        Returns:
            Tuple containing the selected value
        """
        value = on_true if switch else on_false
        return (value,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "LazySwitchKJ_UTK": LazySwitchKJ_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LazySwitchKJ_UTK": "Lazy Switch KJ (UTK)",
}
