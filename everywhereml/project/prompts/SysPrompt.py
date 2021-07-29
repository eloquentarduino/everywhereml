from everywhereml.project.prompts.Prompt import Prompt


class SysPrompt(Prompt):
    """
    Prompt to sys input/output
    """
    def print(self, *args, **kwargs):
        """
        Print to sys output
        :param args:
        :param kwargs:
        :return:
        """
        print(*args, **kwargs)

    def input(self, prompt):
        """
        Get input from sys input
        :param prompt: str message prompt
        :return:
        """
        return input(prompt)
