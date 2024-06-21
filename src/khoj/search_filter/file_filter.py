import fnmatch
import logging
import re
from collections import defaultdict
from typing import List

from khoj.search_filter.base_filter import BaseFilter
from khoj.utils.helpers import LRU, timer

logger = logging.getLogger(__name__)


class FileFilter(BaseFilter):
    # file_filter_regex = r'file:"(.+?)" ?'

    # We will make two regex for adding a file and removing a file from the query
    # Similar to word_filter.py
    required_regex = r'\+file:"(.+?)" ?'
    blocked_regex = r'\-file:"(.+?)" ?'

    def __init__(self, entry_key="file"):
        self.entry_key = entry_key
        self.file_to_entry_map = defaultdict(set)
        self.cache = LRU()

    def get_filter_terms(self, query: str) -> List[str]:
        "Get all filter terms in query"
        # return [f"{self.convert_to_regex(term)}" for term in re.findall(self.file_filter_regex, query)]

        # We will create two variable required_terms and blocked_terms to keep the files that the user wants and doesn't want in the query
        # Similar to word_filter.py

        required_terms = [f"{self.convert_to_regex(term)}" for term in re.findall(self.required_regex, query)]
        blocked_terms = [f"{self.convert_to_regex(term)}" for term in re.findall(self.blocked_regex, query)]
        
        # We just return the sum of the two terms

        return required_terms + blocked_terms

    def convert_to_regex(self, file_filter: str) -> str:
        "Convert file filter to regex"
        return file_filter.replace(".", r"\.").replace("*", r".*")

    def defilter(self, query: str) -> str:
        return re.sub(self.file_filter_regex, "", query).strip()
