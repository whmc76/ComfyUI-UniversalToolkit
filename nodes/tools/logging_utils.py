"""
Logging Utilities for UniversalToolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logging utilities for UniversalToolkit.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

def log(message, message_type='info'):
    """简单的日志函数"""
    if message_type == 'error':
        print(f"❌ Error: {message}")
    elif message_type == 'warning':
        print(f"⚠️ Warning: {message}")
    elif message_type == 'finish':
        print(f"✅ {message}")
    else:
        print(f"ℹ️ {message}") 