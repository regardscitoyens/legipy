# coding: utf-8

from . import law_parser
from . import legislature_list_parser
from . import pending_law_list_parser
from . import published_law_list_parser
from . import common_law_list_parser

parse_law = law_parser.parse_law
parse_legislature_list = legislature_list_parser.parse_legislature_list
parse_pending_law_list = pending_law_list_parser.parse_pending_law_list
parse_published_law_list = published_law_list_parser.parse_published_law_list
parse_common_law_list = common_law_list_parser.parse_common_law_list
