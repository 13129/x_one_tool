def parse_pagination(pag=None):
    """
    自动解析翻页参数
    """

    def custom_decorator(func):
        def wrapper(skip, limit):
            # 在这里添加自定义逻辑
            skip, limit = pag.get("skip"), pag.get("limit")
            return skip, limit

        return wrapper

    return custom_decorator
