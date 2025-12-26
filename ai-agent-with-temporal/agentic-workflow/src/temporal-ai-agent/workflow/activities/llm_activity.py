import importlib.util
from pathlib import Path
from temporalio import activity

# Load and call weather_record_by_id.py dynamically
llm_prompt_handler_path = Path(__file__).parent / "integration/ollama" / "llm_prompt_handler.py"
spec = importlib.util.spec_from_file_location("llm_prompt_handler", llm_prompt_handler_path)
llm_prompt_handler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_prompt_handler_module)

@activity.defn
def llm_call_activity(prompt: str) -> str:
    weather_type = llm_prompt_handler_module.llm_call(prompt)
    return weather_type