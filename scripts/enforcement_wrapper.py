#!/usr/bin/env python3
"""
SIMPLE ENFORCEMENT WRAPPER
Use this before EVERY response.
"""

import sys
sys.path.insert(0, 'E:/CLAUDE')

from enforcement_engine import enforce_response, validate_output

def pre_response(user_input: str, mod: str = 'A') -> dict:
    """MANDATORY: Call BEFORE generating any response."""
    return enforce_response(user_input, mod)

def post_response(output: str, user_input: str) -> dict:
    """MANDATORY: Call AFTER generating response, BEFORE sending."""
    return validate_output(output, user_input)

# Usage example:
# pre = pre_response("user input here")
# print(pre['banner'])  # MUST print this first
# ... generate response ...
# post = post_response(generated_output, user_input)
# if not post['valid']: fix and re-validate
# then send