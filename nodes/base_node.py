from abc import ABC, abstractmethod
from typing import Any
from llms.base import BaseLLM
from state.state import State

class BaseNode(ABC):
    def __init__(self, llm_client: BaseLLM, node_name: str = ""):
        self.llm_client = llm_client
        self.node_name = node_name or self.__class__.__name__

    @abstractmethod
    def run(self, input_data: Any, **kwargs) -> Any:
        pass


    def validate_input(self, input_data: Any) -> bool:
        return True

    def before_run(self, input_data: Any):
        pass

    def after_run(self, result: Any):
        pass

    def process_output(self, output: Any) -> Any:
        return output

    def log_info(self, message: str):
        print(f"[{self.node_name}] {message}")

    def log_error(self, message: str):
        print(f"[{self.node_name}] 错误: {message}")



class StateMutationNode(BaseNode):
    @abstractmethod
    def mutate_state(self, input_data: Any, state: State, **kwargs) -> State:
        pass


