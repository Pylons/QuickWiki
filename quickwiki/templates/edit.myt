<h1 class="main">Editing <% c.title %></h1>

<% h.start_form(h.url_for(action='save', title=c.title),method="post") %>
    <% h.text_area(name='content', rows=7, cols=40, content=c.content)%> <br /> 
    <% h.submit(value="Save changes", name='commit') %>
<% h.end_form() %>