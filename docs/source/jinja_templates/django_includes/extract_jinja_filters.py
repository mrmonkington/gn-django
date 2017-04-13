import re
import itertools

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
    if "templatetag" in tag_match:
        templatetag_docs[tag_name] = builtins_rst[start_index:end_index]
    if "templatefilter" in tag_match:
        templatefilter_docs[tag_name] = builtins_rst[start_index:end_index]


for tag_name, tag_doc in templatefilter_docs.items():
    with open("filters/" + tag_name + ".rst", "w") as f:
        f.write(tag_doc)

for tag_name, tag_doc in templatetag_docs.items():
    with open("tags/" + tag_name + ".rst", "w") as f:
        f.write(tag_doc)


