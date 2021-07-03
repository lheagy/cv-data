from pybtex.database.input import bibtex
import json

parser = bibtex.Parser()
bib_data = parser.parse_file("heagy-publications.bib")

peer_reviewed = {}
non_peer_reviewed = {}
conference_proceedings = {}

non_peer_reviewed_journals = ["The Leading Edge"]

awards = {
    "Heagy2013": "Award of Merit (Best Student Paper, Annual Meeting)"
}

for key in bib_data.entries.keys():
    d = {
        "authors": [],
        "award": None,
        "booktitle": None,
        "title": None,
        "year": None,
        "journal": None,
        "doi": None,
        "arxivId": None,
        "url": None
    }
    entry = bib_data.entries[key]

    for k in d.keys():
        if k in entry.fields.keys():
            d[k] = entry.fields[k]
    for p in entry.persons["author"]:
        d["authors"].append(", ".join([" ".join(p.last_names), " ".join([f[0] + "." for f in p.bibtex_first_names])]))

    if entry.type == "article":
        if entry.fields["journal"] in non_peer_reviewed_journals:
            non_peer_reviewed[key] = d
        else:
            peer_reviewed[key] = d
    elif entry.type == "inproceedings":
        conference_proceedings[key] = d
    elif entry.type == "misc":
        non_peer_reviewed[key] = d
    else:
        print(key, entry.type)


for filename, data in zip(
    ["peer-reviewed.json", "non-peer-reviewed.json", "conference-proceedings.json"],
    [peer_reviewed, non_peer_reviewed, conference_proceedings]
):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
