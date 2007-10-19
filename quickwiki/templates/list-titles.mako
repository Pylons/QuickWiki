% for title in c.titles:
<li>
  <span id="${unicode(title)}">${title}</span>
  &nbsp;[${h.link_to('visit', h.url_for(title=title, action="index"))}]
  ${h.draggable_element(unicode(title), revert=True)}
</li>
% endfor
