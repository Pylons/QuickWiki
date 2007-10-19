% for title in c.titles:
<li>
  <span id="page-${unicode(title)}">${title}</span>
  &nbsp;[${h.link_to('visit', h.url_for(title=title, action="index"))}]
  ${h.draggable_element("page-"+ unicode(title), revert=True)}
</li>
% endfor
