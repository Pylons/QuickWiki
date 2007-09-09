<%inherit file="base.mako"/>  

<h1 class="main">${c.title}</h1>
<p>This page doesn't exist yet.
  <a href="${h.url_for(action='edit', title=c.title)}">Create the page</a>.
</p>
