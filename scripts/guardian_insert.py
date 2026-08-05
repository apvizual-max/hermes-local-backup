# ── MANDATORY ENFORCEMENT: Post-response Guardian validation ──────────
# This MUST run BEFORE returning the final response
try:
    from enforcement_engine import validate_output
    val_result = validate_output(final_response, original_user_message)
    if not val_result['valid']:
        logger.warning(f"GUARDIAN VIOLATION: {val_result['errors']}")
        # Attempt auto-fix for common violations
        fixed_response = final_response
        # Fix 1: Missing banner - prepend the enforcement banner
        if "MISSING OR INVALID BANNER" in str(val_result['errors']):
            # Get the banner from the agent's enforcement_banner if available
            if hasattr(agent, 'enforcement_banner') and agent.enforcement_banner:
                fixed_response = agent.enforcement_banner + '\n' + final_response
            else:
                # Fallback: generate a banner
                from enforcement_engine import enforce_response
                pre_result = enforce_response(original_user_message, 'A')
                if pre_result['banner']:
                    fixed_response = pre_result['banner'] + '\n' + final_response
        # Fix 2: Fabrication markers - cannot auto-fix, must return error
        elif "D2_JUST_FAB" in str(val_result['errors']):
            raise ValueError(f"Fabrication detected: {val_result['errors']}")
        # Fix 3: Banner sum error - recalculate
        elif "BANNER SUM" in str(val_result['errors']) or "sum != 100" in str(val_result['errors']):
            from enforcement_engine import enforce_response
            pre_result = enforce_response(original_user_message, 'A')
            if pre_result['banner']:
                fixed_response = pre_result['banner'] + '\n' + final_response
        # Re-validate
        val_result2 = validate_output(fixed_response, original_user_message)
        if val_result2['valid']:
            final_response = fixed_response
        else:
            logger.error(f"GUARDIAN: Could not auto-fix output: {val_result2['errors']}")
            raise ValueError(f"Output validation failed: {val_result2['errors']}")
except ImportError:
    # enforcement_engine not available - skip validation
    pass
except ValueError:
    # Re-raise validation errors
    raise
except Exception as e:
    logger.error(f"Guardian validation error: {e}")
# ──────────────────────────────────────────────────────────────────

# Note: Memory provider on_session_end() + shutdown_all() are NOT