
# sqlite-notebook

An un-inventively named quick script to process markdown documents with inline
SQL queries.

You write a markdown file with code blocks tagged `sql`, then run this script
against it, along with a local sqlite3 database file, and you get HTML output
with the query results in table form. Sort of like a crude/simple jupyter
notebook.

Requires the python package `mistune` to parse markdown. Try something like:

    # debian/ubuntu
    sudo apt install python3-mistune

    # elsewhere
    sudo pip3 install mistune
