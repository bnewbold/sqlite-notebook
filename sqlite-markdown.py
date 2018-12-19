#!/usr/bin/env python3

import sys
import sqlite3
import mistune
import argparse

class SqliteMarkdownRenderer(mistune.Renderer):

    def __init__(self, conn):
        super(SqliteMarkdownRenderer, self).__init__()
        self.conn = conn

    def block_code(self, code, lang):
        if lang.strip().lower() == 'sql':
            # remove comment lines
            core = code.strip()
            code = '\n'.join(
                [line.strip() for line in code.split('\n') if not (line.strip().startswith('#') or not line.strip())])
            core = code.strip()
            sys.stderr.write("executing: {}\n".format(code.strip()))
            cursor = self.conn.cursor()
            result = cursor.execute(code)
            ret = ""
            if cursor.description is None:
                ret = "(empty result)"
            else:
                ret += "<table>\n  <thead><tr>\n"
                for k in cursor.description:
                    ret += "  <th>{}</th>\n".format(k[0])
                ret += "</tr></thead>\n"
                if not result.rowcount:
                    ret += "<tr><td>(no rows returned)</td></tr>"
                for row in result:
                    ret += "<tr>\n"
                    for v in row:
                        if v is None:
                            v = ''
                        if type(v) == str and (v.startswith("https://") or v.startswith("http://")):
                            ret += '  <td><a href="{}">{}</a></td>\n'.format(v, v)
                        elif type(v) == str and v.startswith("10."):
                            ret += '  <td><a href="https://doi.org/{}">{}</a></td>\n'.format(v, v)
                        else:
                            ret += '  <td>{}</td>\n'.format(v)
                    ret += "</tr>\n"
                ret += "</table>"
            ret += "<pre><b>QUERY:</b> {}</pre>\n<br>".format(code)
            return '<div style="margin: 1em 3em 1em 3em; "><code>' + ret + "</code></div>"
        else:
            return "\n<code>" + code + "</code>\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file",
        default=sys.stdin, type=argparse.FileType('rt'))
    parser.add_argument("sqlite_db_path",
        type=str)
    args = parser.parse_args()

    conn = sqlite3.connect(args.sqlite_db_path)
    renderer = SqliteMarkdownRenderer(conn)
    markdown = mistune.Markdown(renderer=renderer)
    print(markdown(args.markdown_file.read()))

if __name__ == '__main__':
    main()
