<%inherit file="base.mako"/>

<h1 class="main">${c.title}</h1>
% if c.message:
<p><div id="message">${c.message}</div></p>
% endif
${c.content}
