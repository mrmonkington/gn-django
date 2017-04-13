import re
import itertools

all_filters = [
    "addslashes",
    "capfirst",
    "escapejs",
    "floatformat",
    "iriencode",
    "linenumbers",
    "make_list",
    "slugify",
    "stringformat",
    "truncatechars",
    "truncatechars_html",
    "truncatewords",
    "truncatewords_html",
    "urlizetrunc",
    "ljust",
    "cut",
    "linebreaksbr",
    "linebreaks",
    "striptags",
    "add",
    "date",
    "time",
    "timesince",
    "timeuntil",
    "default_if_none",
    "divisibleby",
    "yesno",
    "pluralize",
    "localtime",
    "utc",
    "timezone",
]
all_filters_regex = "(?:" + "|".join(all_filters) + ")"


def process_yesno(docs):
    cut_at = "Internationalization tags and filters"
    cut_at_index = docs.index(cut_at)
    docs = docs[:cut_at_index]
    return docs
    
custom_processors = {'yesno': process_yesno}

def process_docs_text(tag_name, docs):
    # Replace the titles with function definitions
    title_regex = "``" + tag_name + "``\n(?:---+|~~~+)\n"
    replacement = ".. function:: " + tag_name + "\n"
    docs = re.sub(title_regex, replacement, docs)
    # Indent the subsequent body
    body_start_index = docs.index(replacement) + len(replacement)
    body = docs[body_start_index:-1]
    body = body.replace("\n", "\n    ")
    docs = docs[:body_start_index] + body
    # transpose django syntax filters in to jinja syntax
    docs = re.sub(r"({{ (?:[^:|]*)|" + all_filters_regex + ")(:)([^}}]*)( }}?)", r"\1(\3)\4", docs)
    # Finally run a custom processor for this tag, if it exists
    if custom_processors.get(tag_name):
        docs = custom_processors[tag_name](docs)
    return docs

builtins_rst = ""
with open("_django_builtins.rst", "r") as f:
    builtins_rst = f.read()

tag_matches = re.findall("\.\. (?:templatetag|templatefilter)\:\: .*\n", builtins_rst)
filter_docs = {}
templatetag_docs = {}
templatefilter_docs = {}
tag_pairs = zip(tag_matches, tag_matches[1:] + [-1])
for tag_match, next_tag_match in tag_pairs:
    tag_name = tag_match.split('::')[1].strip()
    start_index = builtins_rst.index(tag_match)
    if next_tag_match == -1:
        end_index = -1
    else:
        end_index = builtins_rst.index(next_tag_match)
    docs_text = builtins_rst[start_index:end_index]
    docs_text = process_docs_text(tag_name, docs_text)
    if "templatetag" in tag_match:
        templatetag_docs[tag_name] = docs_text
    if "templatefilter" in tag_match:
        templatefilter_docs[tag_name] = docs_text

for tag_name, tag_doc in templatefilter_docs.items():
    with open("filters/" + tag_name + ".rst", "w") as f:
        f.write(tag_doc)

for tag_name, tag_doc in templatetag_docs.items():
    with open("tags/" + tag_name + ".rst", "w") as f:
        f.write(tag_doc)


