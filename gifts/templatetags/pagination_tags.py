from urllib.parse import parse_qs, urlencode

from django import template

register = template.Library()


@register.filter
def remove_query_param(query_string, param):
    """
    Remove a query parameter from a query string
    """
    query_dict = parse_qs(query_string)
    query_dict.pop(param, None)
    return urlencode(query_dict, doseq=True)


@register.simple_tag
def paginator_range(page_obj, paginator, spread=2):
    """
    Generate a range of page numbers for pagination with optional spread around the current page.

    Args:
        page_obj (Page): The current page object.
        paginator (Paginator): The paginator object containing all pages.
        spread (int, optional): The number of pages to include around the current page. Defaults 2.

    Returns:
        list: A list of page numbers and "..." where ranges are skipped.
    """

    current_page = page_obj.number
    total_pages = paginator.num_pages
    spread = int(spread)

    pages = {1, total_pages}

    for i in range(current_page - spread, current_page + spread + 1):
        if 1 <= i <= total_pages:
            pages.add(i)

    pages_list = sorted(list(pages))

    final_list = []
    prev_page = None
    for p in pages_list:
        if prev_page is not None and p - prev_page > 1:
            final_list.append("...")
        final_list.append(p)
        prev_page = p

    return final_list
