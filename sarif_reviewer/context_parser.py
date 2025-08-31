from importlib import import_module
from pathlib import Path
from typing import Dict

from tree_sitter import Language, Parser
from .logging import get_logger

logger = get_logger(__name__)


class GenericLanguageManager:
    """
    Dynamically load parsers for installed tree-sitter language wheels.
    Assumes you already installed e.g.:
        pip install tree-sitter-python tree-sitter-javascript
    """

    def __init__(self):
        self._languages: Dict[str, Language] = {}

    def load_language(self, lang: str) -> Language:
        """
        Load a Language object from a prebuilt wheel.
        lang: "python", "javascript", "go", etc.
        """
        if lang in self._languages:
            return self._languages[lang]

        pkg_name = f"tree_sitter_{lang.replace('-', '_').replace(' ', '_')}"
        try:
            module = import_module(pkg_name)
        except ModuleNotFoundError:
            raise ValueError(
                f"Tree-sitter package for '{lang}' not found. "
                f"Did you install `{pkg_name}`?"
            )

        # Common convention: each package exposes a `language()` function
        if hasattr(module, "LANGUAGE"):
            lang_obj = module.LANGUAGE
        elif hasattr(module, "language"):
            lang_obj = module.language()
        else:
            raise RuntimeError(f"Could not find a Language in {pkg_name}")
        lang_obj = Language(lang_obj)
        self._languages[lang] = lang_obj
        return lang_obj


class ContextParser:
    pm = GenericLanguageManager()

    def __init__(
        self,
        language_name: str,
    ):
        self.language = ContextParser.pm.load_language(language_name)
        self.parser = Parser(self.language)
        self.tree = None

    def parse(self, file_path: str, base_dir: str = None):
        try:
            if base_dir:
                path = Path(base_dir) / Path(file_path)
            else:
                path = Path(file_path)

            with open(path, "r", encoding="utf-8") as f:
                code = f.read()

                tree = self.parser.parse(code.encode())
                self.tree = tree
                logger.info(f"Successfully parsed file {file_path}")
                return self.tree.root_node

        except Exception:
            logger.error(f"Error parsing file {file_path}", exc_info=True)
            return None

    def get_tree(self):
        return self.tree

    def get_contextual_code_for_point(
        self, starting_point: tuple, ending_point: tuple = None, encoding: str = "utf-8"
    ) -> str:
        if not self.tree:
            return ""
        
        if starting_point and ending_point:
            logger.debug(f"Getting contextual code from {starting_point} to {ending_point}")
            node = self.tree.root_node.descendant_for_point_range(starting_point, ending_point)
            return node.text.decode(encoding)
        elif starting_point:
            logger.debug(f"Getting contextual code from Starting point: {starting_point}")
            cursor = self.tree.walk()
            cursor.goto_first_child_for_point(starting_point)
            return cursor.node.text.decode(encoding)
        
        return ""


if __name__ == "__main__":
    example = """
def foo(x):
    return x + 1
"""
    parser = ContextParser("python")
    root_node = parser.parse(example)

    # for child in root_node.children:
    #     print(child.type, child.start_point, child.end_point, child.text)

    def print_cursor(cursor):
        print(
            cursor.node.type,
            cursor.node.start_point,
            cursor.node.end_point,
            cursor.node.text,
        )

    cursor = root_node.walk()

    # cursor.goto_first_child()
    # print_cursor(cursor)

    # cursor.goto_next_sibling()
    # print_cursor(cursor)

    # cursor.goto_next_sibling()
    # print_cursor(cursor)

    cursor.goto_first_child_for_point((36, 0))
    print_cursor(cursor)
    print(cursor.node.text.decode("utf-8"))
