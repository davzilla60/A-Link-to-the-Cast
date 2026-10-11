# A Link to the Cast

**Rad-Lad: The Fracture Quest.** This is an embeddable retro dungeon game for the Rad-Lad website. Players explore a torch-lit cave and sort real X-rays into **Fracture** or **No fracture**, guided by two bickering stone guardians.

## How it plays

1. **The Cave Gift.** The player walks into a cave, where an old man says *"It's dangerous to go alone! Take this PACS login."* Picking up the paper triggers the item-held pose, a glow, a jingle and the **PACS Access Acquired** banner. A passage then opens to the north.
2. **The Guardians' Chamber.** Two statues flank a sealed door and introduce themselves:
   - **Stable** (No fracture): intact, symmetrical, arms folded, calm and slightly smug.
   - **Splinter** (Fracture): cracked and chipped, with his chest plate shifted out of line. Cheeky and theatrical.
3. **The X-ray challenge.** Each film opens in a lightbox viewer, which can expand to full screen and supports zoom, pan, pinch and invert. Back in the chamber, the player stands on the pressure plate in front of a guardian and presses **A**, or taps one of the choice buttons. The guardians react and bicker. An answer card then explains the findings, with a **Look again** option.
4. **The door opens.** After the last film, the door behind the guardians slides open onto a lava glow. A review screen lists every film (each reopens with its answer), then **Through the door** leads on to Chamber II.
5. **Chamber II: Saria's Lava Gym.** A volcanic cavern with a central platform, a bench press, a dumbbell rack, weight plates and mats, all surrounded by lava. Saria (blonde, in gym gear) stops doing curls, congratulates the player, explains the rules, twirls on one leg and strikes a "bring it on" pose. Two punching bags then drop from the ceiling: **No fracture** on the left and **Fracture** on the right.
   - The player inspects each film, then punches a bag (stand under it and press **A**, or tap a choice button and the hero walks over and punches).
   - **Three health bubbles.** A wrong answer makes lava drip from the ceiling onto the player and pops one bubble. Saria then explains the film on an answer card. The round is untimed.
   - **Losing all three bubbles** ends the round, with **Restart Saria's trial** or the title screen. Restarting keeps Chamber I completed.
   - Finishing the round offers **Look around**. The barricaded door at the back is locked. Walking up to it makes Saria say the next chamber is still under construction.

- **Level select:** the title screen has **Begin quest** (cave → Chamber I → Chamber II) and direct buttons for **Chamber I** and **Chamber II**. Cleared chambers are ticked (saved in the browser).
- **Random order:** each chamber's films are reshuffled every time it starts, including replays and restarts.
- **Markers** (Rad-Lad "Marker Unlocked" stamp toast, plus the item-held pose and a guardian exchange). Progress counts total correct answers in a run, so a mistake does not reset it.
  - **A Crack-ing Start**: 5 correct. A bronze stone shield with a crack and five gems.
  - **The Legend of Align-da**: 10 correct. A gold crest with aligned stone sections and ten gems. With 10 cases, this needs a perfect run.
  - Chamber II: **Halfway to X-Ray Vision** (5 correct, half-lit X-ray goggles), **X-Ray Vision Unlocked** (10 correct, fully lit goggles) and **Missed the Mark** (lose all three bubbles, a target with a stray dart). The two correct-answer markers use the item-held pose; Missed the Mark shows a banner instead.
- **Controls:** arrows or WASD to move, Space/Enter/Z for A, `V` to view the film, `N`/`F` to choose directly, Esc to close the viewer. In the viewer, `+`/`-`/`0` zoom, `I` inverts and `E` expands. Clicking or tapping the floor walks there. On touch devices a D-pad and A/B buttons appear.
- Sound is synthesised chip audio with a toggle (no audio files). Unlocked markers and the sound setting are saved in the browser.

## Files

| File | Purpose |
|---|---|
| `index.html` / `cast.embed.html` | Built, self-contained game with all images inlined. Embed this. |
| `cast.html` | Source page. The build fills in its placeholders. |
| `build.py` | Case list (answers, labels, explanation text), image credits, and the build |
| `assets/src/` | Original radiographs |
| `assets/cNN.jpg` | Generated greyscale JPEGs (longest side 1400 px) |

## Adding or editing cases

1. Drop the radiograph in `assets/src/`.
2. Add an entry to `CASES` in `build.py` with `id`, `src`, `chamber` (1 or 2), `fracture` (True/False), `label` (shown when the film is presented), `title`, `findings`, and `source` (a key into `SOURCES`, or `None`).
3. Run `python build.py`. For local testing, `python build.py --preview` writes `_preview.html`, which loads the images from `assets/` instead of inlining them.

## Image credits

- Cases c05, c07, c08, c09, c11 and c16: Abedeen, I., Rahman, M. A., Zohra Prottyasha, F., Ahmed, T., Mohmud Chowdhury, T., & Shatabda, S. (2023). *FracAtlas: A Dataset for Fracture Classification, Localization and Segmentation of Musculoskeletal Radiographs.* figshare. Dataset. https://doi.org/10.6084/m9.figshare.22363012.v7 (CC BY 4.0). Converted to greyscale JPEG.
- Cases c01–c04, c06, c10, c12–c15 and c17–c20: source credit still to be added.

Educational use only; not for clinical decisions.
