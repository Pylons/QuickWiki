# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html>
<head>
  <title>QuickWiki</title>
  ${h.stylesheet_link_tag('/quick.css')}
  ${h.javascript_include_tag('/javascripts/effects.js', builtins=True)}
</head>
<body>
  <div class="content">
    ${next.body()}\
    <p class="footer">
    ${footer(request.environ['pylons.routes_dict']['action'])}\
    </p>
  </div>
</body>
</html>

## Don't show links that are redundant for particular pages
<%def name="footer(action)">\
  Return to the ${h.link_to('FrontPage', h.url_for(action="index", title="FrontPage"))}
  % if action == "list":
    <% return '' %>
  % endif
  % if action != "edit":
    | ${h.link_to('Edit '+c.title, h.url_for(title=c.title, action='edit'))}
  % endif
  | ${h.link_to('Title List', h.url_for(action='list', title=None))}
</%def>