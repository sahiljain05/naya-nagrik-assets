# @krishna.speaks.truth: publishing through Buffer

All @krishna.speaks.truth posts are published through Buffer (vidIQ is no longer used for posting; vidIQ may still be used read-only for insights).
Content rules, rendering and captions stay as in the skills `gita-daily-carousel`, `gita-series-katha` and `krishna-se-baat`. Only their final "Publish" step is replaced by the steps below.

## Fixed IDs

| Thing | Value |
| --- | --- |
| Buffer organization | `6b028ae1c16256a90aecfb2f` |
| Buffer channel (Instagram krishna.speaks.truth) | `6b02d5ef8541f09ecb62b42f` |
| Image hosting | this repo, `krishna/<YYYY-MM-DD>-<slot>/slide_NN.jpg` |
| Raw URL | `https://raw.githubusercontent.com/sahiljain05/naya-nagrik-assets/main/krishna/<YYYY-MM-DD>-<slot>/slide_NN.jpg` |

Slots: `shlok` (06:00), `katha` (14:00), `series` (19:30), `baat` (19:30 Tue/Sat).

## Steps

1. **Duplicate check first.** Buffer `list_posts` for the channel above. If a post for today's slot is already scheduled or sent (same caption tag, e.g. `Day N ·`, `Katha #N ·`), stop and report it. Also check the latest Instagram captions to work out the next number (Buffer post texts are fine for this, or vidIQ `vidiq_social_post_list` / `vidiq_instagram_owner_insights` read-only).
2. Render the slides as the skill says (1080x1350 JPEG, 4:5). Look at every slide.
3. Copy them to `krishna/<YYYY-MM-DD>-<slot>/` in this repo, commit, and push to `main` (`git -c push.negotiate=true push origin main`; on rejection `git pull --rebase` once and push again). Confirm the raw URL of slide_01 returns HTTP 200 (`curl -s -o /dev/null -w "%{http_code}"`). Wait a few seconds and retry once if it is 404.
4. Buffer `create_post`:
   - `channelId` `6b02d5ef8541f09ecb62b42f`, `schedulingType` `automatic`, `mode` `customScheduled`, `dueAt` today's slot time in `+05:30` (e.g. `2026-11-23T06:00:00+05:30`). If that time has already passed, use `mode` `shareNow`.
   - `metadata.instagram`: `{ "type": "post", "shouldShareToFeed": true, "isAiGenerated": <true only when the post uses an OpenArt illustration> }`.
   - `assets`: every slide in order, `{ "image": { "url": <raw URL>, "metadata": { "altText": <one line describing the slide + topic keyword> } } }`.
   - `text`: the caption written per the skill (first line = tag, max 5 hashtags).
5. Check the response: `status` scheduled (or sent) and the asset count equals the number of slides. If Buffer returns an error, fix it and retry once; never create a second copy of the same post.
6. Report in one line: tag, topic, Buffer post id, scheduled time, status.

## Limits

Buffer free plan: 3 channels, 10 scheduled posts at a time across the organization (shared with @naya.nagrik). Each run schedules only the same day's post, so the queue stays small. If Buffer refuses because the queue is full, report it; do not delete other posts.
