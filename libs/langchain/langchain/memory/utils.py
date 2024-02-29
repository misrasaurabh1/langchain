from typing import Any, Dict, List


def get_prompt_input_key(inputs: Dict[str, Any], memory_variables: List[str]) -> str:
    """
    Get the prompt input key.

    Args:
        inputs: Dict[str, Any]
        memory_variables: List[str]

    Returns:
        A prompt input key.
    """

    prompt_input_keys = set(inputs).difference(memory_variables)
    if "stop" in prompt_input_keys:
        prompt_input_keys.remove("stop")
    num_keys = len(prompt_input_keys)
    if num_keys != 1:
        raise ValueError(f"One input key expected got {list(prompt_input_keys)}")
    return next(iter(prompt_input_keys))
