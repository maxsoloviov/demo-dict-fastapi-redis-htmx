import os.path
from typing import Dict, List, Optional, Tuple

from aioredis import Redis

from .helpers.trie import Trie


class DictionaryService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def clear(self) -> None:
        await self._redis.flushall()

    def load_dictionary(self) -> Dict[str, str]:
        location = os.path.dirname(__file__)
        with open(os.path.join(location, 'de-en.txt')) as f:
            return {
                k: v for k, v in filter(
                    lambda val: val is not None,
                    (
                        self.parse_record(line)
                        for line in f
                        if not line.startswith('#')
                    )
                )
            }

    def populate_trie(self, trie: Trie, words: List[str]) -> None:
        for word in words:
            trie.add(word)

    async def populate(self, dictionary: Dict[str, str]) -> None:
        await self._redis.mset(dictionary)

    def parse_record(self, line: str) -> Optional[Tuple[str, str]]:
        index = line.find('{')
        if index == -1:
            return

        word = line[:index].strip().lower()
        article = line[index:]
        return word, article

    async def get_article(self, word: str) -> Optional[str]:
        return await self._redis.get(word)
