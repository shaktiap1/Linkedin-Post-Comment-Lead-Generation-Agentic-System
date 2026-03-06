async def safe_query_selector(container, selector):

    try:
        element = await container.query_selector(selector)
        return element

    except Exception:
        return None