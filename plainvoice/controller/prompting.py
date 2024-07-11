from prompt_toolkit import prompt as ptk_prompt


def prompt_yes_no(message: str) -> tuple[bool, str]:
    """
    Prompting the user for a simple yes/no question.

    Args:
        message (str): \
            The message to display on asking. It gets
            appended by " [(y)es/(n)o]" by default.

    Returns:
        tuple: \
            bool: True, if "yes" or "y" was answered.
            str: The prompting process.
    """
    answer = ptk_prompt(message + " [yes/no] ")
    return answer.lower() in ['yes', 'y']
