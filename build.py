"""Build index.html / cast.embed.html from cast.html + assets/.

For every case in CASES:
  assets/src/<src>       the original radiograph (any size, any JPEG/PNG)
The build makes, per case:
  - assets/<id>.jpg      greyscale JPEG, longest side <= MAX_SIDE
  - a small thumbnail for the end-of-quest review list
then base64-inlines everything so the output is one self-contained file.

Usage:  python build.py            -> index.html + cast.embed.html (self-contained)
        python build.py --preview  -> _preview.html (references assets/ files; for local testing)
"""
import base64, io, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
A = ROOT / "assets"
MAX_SIDE = 1400

# "fracture" is the verified answer (labelled by the user, 2026-10-11).
# "source" is a key into SOURCES. Text is shown on the answer card.
CASES = [
    {
        "id": "c01", "src": "01.jpg", "fracture": False, "source": None,
        "label": "Right knee, AP",
        "title": "No fracture: right knee",
        "findings": [
            "The cortex of the distal femur, proximal tibia and fibular head is smooth and unbroken.",
            "The joint spaces are preserved and the bones are aligned.",
            "The bones at the top left are the patient's fingers resting on the thigh. Check the edges of every film.",
        ],
    },
    {
        "id": "c02", "src": "02.jpg", "fracture": False, "source": None,
        "label": "Ankle and hindfoot, lateral",
        "title": "No fracture: lateral ankle",
        "findings": [
            "The distal tibia, talus and calcaneus all have smooth, continuous outlines.",
            "The ankle and subtalar joints line up normally.",
            "The faint line across the distal tibia is a physeal scar (the old growth plate). It is smooth and runs right across the bone, so it is not a fracture.",
        ],
    },
    {
        "id": "c03", "src": "03.jpg", "fracture": False, "source": None,
        "label": "Left ankle, AP",
        "title": "No fracture: left ankle",
        "findings": [
            "Both malleoli are intact and the ankle mortise is congruent.",
            "The foot is rotated, so the tarsal bones overlap. Overlapping edges make lines that are not fractures.",
            "The small curved shadows at mid-shin are skin or clothing folds.",
        ],
    },
    {
        "id": "c04", "src": "04.jpg", "fracture": False, "source": None,
        "label": "Child's forearm and elbow",
        "title": "No fracture: child's forearm",
        "findings": [
            "The radius and ulna are straight, with smooth cortices from elbow to wrist.",
            "Growth plates and separate ossification centres are normal in a child. They are smooth-edged and sit where you expect them.",
            "If in doubt, compare with the other side or a normal reference for the child's age.",
        ],
    },
    {
        "id": "c05", "src": "05.jpg", "fracture": False, "source": "fracatlas",
        "label": "Elbow, AP and lateral",
        "title": "No fracture: elbow",
        "findings": [
            "The humeral condyles, radial head and olecranon have smooth outlines on both views.",
            "On the lateral view the radial head points at the capitellum.",
            "Always check the lateral view for a raised posterior fat pad: it can be the only clue to a hidden fracture.",
        ],
    },
    {
        "id": "c06", "src": "06.jpg", "fracture": True, "source": None,
        "label": "Left knee, AP",
        "title": "Fracture: proximal tibia",
        "findings": [
            "An oblique fracture line crosses the proximal tibial metaphysis, below the plateau.",
            "There is a small step in the medial cortex (image left), where the line exits the bone.",
            "Trace each cortex all the way round. A step or gap in the outline gives the fracture away.",
        ],
    },
    {
        "id": "c07", "src": "07.jpg", "fracture": True, "source": "fracatlas",
        "label": "Pelvis and hips, AP",
        "title": "Fracture: right proximal femur",
        "findings": [
            "The right trochanteric region (image left) is irregular and fragmented. The normal smooth neck-shaft outline is lost.",
            "Compare it with the normal left hip: the outlines should mirror each other.",
            "In an older patient with a fall and hip pain, look closely at the neck and trochanters on every pelvis film.",
        ],
    },
    {
        "id": "c08", "src": "08.jpg", "fracture": True, "source": "fracatlas",
        "label": "Infant forearm, held for the film",
        "title": "Fracture: infant forearm",
        "findings": [
            "The forearm bones lose their smooth, straight outline towards the wrist end, with a break in the cortex.",
            "Children's bones often bend or buckle instead of snapping cleanly, so look for subtle kinks and bulges.",
            "The adult hand holding the child is in the beam. If someone must hold a patient, shield them and keep their hands out of the field.",
        ],
    },
    {
        "id": "c09", "src": "09.jpg", "fracture": True, "source": "fracatlas",
        "label": "Wrist and hand, PA",
        "title": "Fracture: distal radius",
        "findings": [
            "There is a dense, irregular band across the distal radial metaphysis, with loss of the smooth cortical outline: an impacted fracture.",
            "The carpal bones and small joints also show arthritic change. That is a separate finding.",
            "Impaction shows up as a white band, not a dark line, because the fragments are driven into each other.",
        ],
    },
    {
        "id": "c10", "src": "10.jpg", "fracture": True, "source": None,
        "label": "Infant arm, held for the film",
        "title": "Fracture: around the infant elbow",
        "findings": [
            "Look at the proximal radius and ulna next to the elbow. The metaphyseal outline is irregular, not the smooth flare it should be.",
            "Much of an infant's elbow is unossified cartilage, so the gaps between the bones are normal. The fracture is in the bone you can see.",
            "The carer's hands are in the beam: shield anyone who has to hold a patient still.",
        ],
    },
]

# Image source attribution. Cases with "source": None have no credit yet.
SOURCES = {
    "fracatlas": {
        "citation": "Abedeen, I., Rahman, M. A., Zohra Prottyasha, F., Ahmed, T., Mohmud Chowdhury, T., & Shatabda, S. (2023). "
                    "FracAtlas: A Dataset for Fracture Classification, Localization and Segmentation of Musculoskeletal Radiographs. "
                    "figshare. Dataset.",
        "url": "https://doi.org/10.6084/m9.figshare.22363012.v7",
        "licence": "CC BY 4.0",
        "licence_url": "https://creativecommons.org/licenses/by/4.0/",
        "changes": "converted to greyscale JPEG",
    },
}


def prep(c):
    im = Image.open(A / "src" / c["src"]).convert("L")
    if max(im.size) > MAX_SIDE:
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    out = A / f"{c['id']}.jpg"
    im.save(out, "JPEG", quality=84, optimize=True)
    t = im.copy()
    t.thumbnail((96, 96))
    buf = io.BytesIO()
    t.save(buf, "JPEG", quality=70)
    return out, im.size, "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def data_uri(p):
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def main():
    preview = "--preview" in sys.argv
    cases = []
    for c in CASES:
        p, size, thumb = prep(c)
        e = {k: v for k, v in c.items() if k != "src"}
        e.update(img=(f"assets/{p.name}" if preview else data_uri(p)), thumb=thumb, w=size[0], h=size[1])
        cases.append(e)
    used = {c["source"] for c in CASES if c["source"]}
    sources = {k: v for k, v in SOURCES.items() if k in used}
    assets = {k: data_uri(A / f"{k}.png") for k in ("logo_mark",)}
    src = (ROOT / "cast.html").read_text(encoding="utf-8")
    out = (src.replace("/*__CASES__*/[]", json.dumps(cases))
              .replace("/*__SOURCES__*/{}", json.dumps(sources))
              .replace("/*__ASSETS__*/{}", json.dumps(assets)))
    names = ["_preview.html"] if preview else ["index.html", "cast.embed.html"]
    for n in names:
        (ROOT / n).write_text(out, encoding="utf-8")
    nf = sum(c["fracture"] for c in CASES)
    print(f"built {len(cases)} case(s) ({nf} fracture, {len(cases)-nf} no fracture) -> {', '.join(names)}, {len(out)/1e6:.2f} MB")


if __name__ == "__main__":
    main()
