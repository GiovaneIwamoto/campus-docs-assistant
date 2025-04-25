import json
import uuid
import logging

logger = logging.getLogger(__name__)

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
                logger.error("[#FF4F4F][PARSER][/#FF4F4F] Invalid tool call format - missing required fields\n")
                return None
                
            # Map the tool call to the expected format
            call["name"] = call.pop("function", "")
            call["args"] = call.pop("arguments", {})
            call["id"] = call.get("id", str(uuid.uuid4()))
            return call
        else:
            logger.warning("[#FF4F4F][PARSER][/#FF4F4F] No 'tool_call' field found in the parsed JSON\n")
            return None
            
    except json.JSONDecodeError as e:
        logger.error(f"[#FF4F4F][PARSER][/#FF4F4F] JSON decode error: {str(e)}\n")
        return None
    
    except Exception as e:
        logger.error(f"[#FF4F4F][PARSER][/#FF4F4F] Error parsing tool call: {str(e)}\n")
        return None