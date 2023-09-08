from typing import List, Tuple

MAX_SUGGESTION_SIZE = 5


class TrieNode:
    def __init__(self, letter: str) -> None:
        self.letter = letter
        self.children = {}
        self.is_complete = False


class Trie:
    def __init__(self):
        self.root = TrieNode("")

    def add(self, word: str) -> None:
        node = self.root
        for letter in word:
            if letter in node.children:
                node = node.children[letter]
            else:
                tmp = TrieNode(letter)
                node.children[letter] = tmp
                node = tmp
        node.is_complete = True

    def search(self, word: str) -> List[Tuple[str, int]]:
        node = self.root
        for letter in word:
            if letter in node.children:
                node = node.children[letter]
            else:
                return []
        return self.dfs(node, word[:-1])

    def dfs(self, node: TrieNode, prefix: str) -> List[Tuple[str, int]]:
        res = []
        next_prefix = prefix + node.letter
        if node.is_complete:
            res.append(next_prefix)

        for child in node.children.values():
            res.extend(self.dfs(child, next_prefix))
        return res
