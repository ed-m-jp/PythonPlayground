import math


def calculate_total_pages(total_items: int, page_size: int) -> int:
    if total_items == 0:
        return 1
    return math.ceil(total_items / page_size)
