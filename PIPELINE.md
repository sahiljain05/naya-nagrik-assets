# Naya Nagrik daily carousel pipeline

Instagram: **@naya.nagrik**. Civic sense for Indian youth, told as stories with two recurring characters.
Owner's full blueprint: the Claude doc "Civic Sense Instagram Channel — Blueprint".

## Fixed IDs

| Thing | Value |
| --- | --- |
| OpenArt project | `1vSDFa0BsrDm349OVAz3` (Personal Project) |
| OpenArt folder | `55bXlNbNEX4sg3TVrNWV` (Naya Nagrik) |
| Character sheet reference | `resource:Atkgr4qUAeDp0nDpccNJ` |
| Image model | `gpt-image-2-5-flare`, mode `image2image`, aspectRatio `3:4` (about 19 credits each) |
| Buffer organization | `6b028ae1c16256a90aecfb2f` |
| Buffer channel (Instagram naya.nagrik) | `6b028f808541f09ecb5fe90a` |
| Image hosting | this repo, `posts/nnXX/`, served from `https://raw.githubusercontent.com/sahiljain05/naya-nagrik-assets/main/posts/nnXX/<file>` |

## Characters (keep exactly as the reference sheet)

- **Bunty** (22): messy black hair, light stubble, mustard-yellow hoodie, blue jeans, white sneakers with green stripes, black backpack, phone in hand. Lovable, lazy, "chalta hai". Usually makes the mistake and changes by the end.
- **Pinky** (21): high black ponytail, light-blue denim jacket over pink kurti, black jeans, brown sling bag, white sneakers with green stripes. Witty, never preachy. About once a month she slips up and Bunty corrects her.
- Any other person (parent, elder, sweeper, cop) must be described explicitly in the prompt with different clothes, and the prompt must say "do not draw the characters from the reference sheet" for that person, otherwise the model turns them into Bunty.

## Daily run

1. `content/plan.json`: take the first entry with `status: "todo"`.
2. Write the story in Hinglish (Roman script) using the 10-slide arc: hook → setup → mistake → ripple → twist → why → Indian mirror → rule → character changes → CTA. Max 25 words per slide.
3. **Only 5 illustrated panels** (slides 1, 3, 4, 5, 9 by default). Slides 2, 6, 7, 8 are `type: text` slides (`kind`: `plain`, `fact`, `mirror`, `rule`); slide 10 is `type: cta`. This keeps cost near 95 credits per post.
4. Panel prompts: start with the character description above, then "Flat 2D comic illustration, clean bold outlines, soft cel shading, warm palette", the scene, and end with "Vertical composition, top 25% plain empty space for text. No text, no letters, no speech bubbles, no signage words." OpenArt runs at most 4 images at a time: submit 4, wait, then the 5th.
5. Download panels, write `spec.json` (see `tools/compose.py` for fields; faces are `assets/face_bunty.png` and `assets/face_pinky.png`), run `python3 tools/compose.py spec.json`. Fonts: Poppins Bold/Medium under `/usr/share/fonts/truetype/google-fonts/`.
6. Look at a contact sheet of all 10 slides. Check: characters correct, no stray text in panels, no other person drawn as Bunty/Pinky, text readable. Regenerate a bad panel once.
7. Commit slides to `posts/nnXX/` and push to `main`. Confirm the raw URL of slide 1 returns 200.
8. Buffer `create_post`: channel above, `schedulingType: automatic`, `mode: customScheduled`, `dueAt` = today 19:00 +05:30, Instagram metadata `{type: post, shouldShareToFeed: true, isAiGenerated: true}`, 10 image assets with alt text.
9. Caption: punch line, 2–3 lines of why, one question for comments, then **exactly 5 hashtags**: `#CivicSense #NayaNagrik #IndianYouth` + 2 pillar tags.
10. Update `plan.json` (status `scheduled`, buffer_post_id), commit, push.

## Red lines (skip the idea and take the next one if a post would break these)

- No shaming real identifiable people, no political party content.
- No religious, caste or regional stereotypes, even as a joke.
- No "India dirty, West clean" framing: every global example is paired with an Indian place or person already doing it right.
- Facts and fines only if you are sure; put the source in small print on the fact slide.
