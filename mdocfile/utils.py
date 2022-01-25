import re

camel_to_snake_regex = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(word: str) -> str:
    return camel_to_snake_regex.sub('_', word).lower()
