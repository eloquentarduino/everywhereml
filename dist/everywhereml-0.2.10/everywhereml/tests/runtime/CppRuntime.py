from everywhereml.tests.runtime.BaseRuntime import BaseRuntime


class CppRuntime(BaseRuntime):
    """
    C++ runtime
    """
    @property
    def language(self):
        return 'cpp'

    @property
    def dialect(self):
        return None

    @property
    def main_file(self):
        return 'main.cpp'

    def get_cmd(self):
        """

        :return:
        """
        return [
            ['g++', '-w', 'main.cpp', '-o', 'main.o'],
            ['./main.o']
        ]