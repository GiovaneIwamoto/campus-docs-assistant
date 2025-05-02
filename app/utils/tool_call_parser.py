import json
import uuid
from config.logging_config import setup_logging, EnhancedLogger

logger = EnhancedLogger(setup_logging())

def parse_tool_call(response):
    """
    Parse the tool call from the LLM response when we've already identified it as a potential JSON.

    Args:
        response (str): The LLM response content.
        
    Returns:
        dict: Parsed tool call with function name and arguments.
        None: If the parsing fails or the structure is invalid.
    """
    try:
        # Attempt to parse as JSON
        parsed = json.loads(response.content)
        
        # Validate the structure
        if "tool_call" in parsed:
            call = parsed["tool_call"]
            
            # Ensure required fields are present
            if "function" not in call or "arguments" not in call:
                logger.parser_error("Invalid tool call format: Missing required fields")
                return None
                
            # Map the tool call to the expected format
            call["name"] = call.pop("function", "")
            call["args"] = call.pop("arguments", {})
            call["id"] = call.get("id", str(uuid.uuid4()))
            return call
        else:
            logger.parser_warning("No tool call field found in the parsed JSON")
            return None
            
    except json.JSONDecodeError as e:
        logger.parser_error(f"JSON decode error: {str(e)}")
        return None
    
    except Exception as e:
        logger.parser_error(f"Error parsing tool call: {str(e)}")
        return None