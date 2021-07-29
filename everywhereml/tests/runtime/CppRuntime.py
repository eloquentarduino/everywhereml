from everywhereml.tests.runtime.BaseRuntime import BaseRuntime


class CppRuntime(BaseRuntime):
    """
    C++ runtime
    """
    def get_cmd(self):
        return [
            ['g++', '-w', 'main.cpp', '-o', 'main.o'],
            ['./main.o']
        ]