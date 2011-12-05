<div xmlns="http://www.w3.org/1999/xhtml"
    xmlns:py="http://purl.org/kid/ns#"
    py:strip="True"
    py:def="PControls(tg, params=[])">

    <?python
        """Displays the pagination controls.

        Sometimes the function receives parameters in this form (1):
            /object/1
        where `object` is the method and `1` is the id parameter. In this case
        the paginate decorator makes a bad request:
            /object/1?tg_paginate_limit=1&tg...&id=1&...
        so the id parameter is provided twice. To fix this, provide params (list
        of parameter names) to erase from the url.
        """

        from idileslib.turbogears.presentation import fix_paginate_url as fix

        pag = tg.paginate
    ?>
    <p style="text-align: center" py:if="pag.page_count > 1" class="paginate-pages">
        <a py:if="pag.current_page > 1" href="${fix(pag.href_first, params)}">&laquo;</a>
        <a py:if="pag.current_page > 1" href="${fix(pag.href_prev, params)}">&lsaquo;</a>
        <span py:for="page in pag.pages">
            <a py:if="page != pag.current_page"
                href="${fix(pag.get_href(page), params)}">${page}</a>
            <b py:if="page == pag.current_page">${page}</b>
        </span>
        <a py:if="pag.current_page &lt; pag.page_count"
            href="${fix(pag.href_next, params)}">&rsaquo;</a>
        <a py:if="pag.current_page &lt; pag.page_count"
            href="${fix(pag.href_last, params)}">&raquo;</a>
    </p>
</div>
