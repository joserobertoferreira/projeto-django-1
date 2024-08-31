import math


def pagination_range(page_range, view_pages, current_page):
    middle_page = math.ceil(view_pages / 2)
    from_page = current_page - middle_page
    to_page = current_page + middle_page
    total_pages = len(page_range)

    offset_page = abs(from_page) if from_page < 0 else 0

    if from_page < 0:
        from_page = 0
        to_page += offset_page

    if to_page >= total_pages:
        from_page -= abs(total_pages - to_page)

    pagination = page_range[from_page:to_page]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'current_page': current_page,
        'total_pages': total_pages,
        'from_page': from_page,
        'to_page': to_page,
        'offset_page': offset_page,
        'has_previous': from_page > 0,
        'has_next': to_page < total_pages,
    }
