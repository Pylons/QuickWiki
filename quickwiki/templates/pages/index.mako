<%inherit file="/base.mako"/>\

<%def name="header()">Title List</%def>

<ul id="titles">
  % for title in c.titles:
  <li>
    ${title} [${h.link_to('visit', url('show_page', title=title))} - ${h.link_to('delete', url('delete_page', title=title))}]
  </li>
  % endfor
</ul>
