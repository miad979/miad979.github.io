# Maintenance Guide

This site is data-driven: almost everything you'll want to update lives in
plain YAML files under `_data/`, not in HTML. Edit a file, commit, push —
GitHub Actions rebuilds and redeploys automatically in 1–2 minutes.

## Where things live

```
_config.yml            → Site-wide info: name, email, phone, location, social links, nav menu
_data/
  education.yml         → Degrees, GPA/CGPA, institutions
  experience.yml         → Jobs, leadership roles, mentorship
  projects.yml           → Every project card (set featured: true to show it on the home page)
  research.yml            → Thesis, manuscripts, research-in-progress
  skills.yml               → Skill categories and items
  awards.yml                → Awards and honors
  certifications.yml         → Certifications (empty until you add one)
about.md, resume.md, contact.md, ...  → Page intros/body copy (short, mostly static)
index.html               → Home page (pulls featured projects from _data/projects.yml automatically)
style.scss                → All styling — colors are SCSS variables at the top
assets/resume.pdf          → Downloadable CV (replace this file to update the PDF)
images/profile.jpg          → Your headshot
```

## Common tasks

### Add a project
Edit `_data/projects.yml` and add an entry at the top:
```yaml
- title: "Project Name"
  description: "One or two sentences on what it does."
  tags: ["Python", "TensorFlow"]
  github: "https://github.com/miad979/repo-name"
  demo: "https://optional-live-demo.com"
  featured: true   # shows on the home page too
  highlights:
    - "Key feature or result"
```
It shows up on `/projects/` immediately, no other file needs to change.

### Link a project to its real GitHub repo
Right now every project's `github:` field points at your general profile
(`https://github.com/miad979`) because the individual repo names weren't
confirmed. Once you know the repo, replace that line with the exact URL,
e.g. `https://github.com/miad979/ai-research-assistant-agent`.

### Add research or a publication
Edit `_data/research.yml`. Anything with `type: "Manuscript"` automatically
appears on `/publications/` as well as `/research/` — you don't need to
touch `publications.md`.

### Add a skill or category
Edit `_data/skills.yml` — add a skill to an existing category's list, or add
a whole new category block.

### Add an award, a degree, or a role
Edit `_data/awards.yml`, `_data/education.yml`, or `_data/experience.yml`
respectively. These also feed the timelines on `/about/` and the table on
`/resume/`, so one edit updates both pages.

### Add a certification
Edit `_data/certifications.yml` (currently empty — see the commented example
inside it). The `/certifications/` page will stop showing the "none yet"
message as soon as one entry exists.

### Update contact info, social links, or the nav menu
Edit `_config.yml`. Everything else references these values, so this is the
one place to change an email, phone number, or social URL.

### Replace the downloadable resume PDF
Overwrite `assets/resume.pdf` with a new export. The "Download PDF" button
on `/resume/` always points at this exact path.

### Change colors or fonts
Edit the variables at the top of `style.scss`:
```scss
$ink: #17201d;    // main text
$muted: #626a66;  // secondary text
$paper: #f4f1ea;  // page background
$white: #fffdf8;  // card background
$lime: #c9f27b;   // accent highlight
$green: #1d493c;  // primary accent
```
Fonts (Manrope for headings, DM Sans for body) are loaded via the
`@import` at the top of the same file.

## Local preview (optional)

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

## Deployment

Deployment is automatic via `.github/workflows/deploy.yml`: every push to
`master` builds the site with Jekyll and publishes it to GitHub Pages.
Check the **Actions** tab on GitHub if a change doesn't show up after a
couple of minutes — that's where build errors (e.g. a YAML typo) will show.

## Troubleshooting

| Issue | Likely cause / fix |
|---|---|
| Site didn't update | Check the Actions tab for a failed build; wait ~2 min; hard-refresh the browser |
| A page looks empty or breaks | Usually a YAML indentation error in `_data/` — validate with a YAML linter |
| Image doesn't show | Path is case-sensitive on GitHub Pages — `Profile.jpg` ≠ `profile.jpg` |
| New page not in the nav | Add it to `navigation:` in `_config.yml` |

## Notes on this rebuild

A few things from the previous version of this repo were intentionally
**left out** because they weren't in the CV supplied for this rebuild, and
couldn't be confirmed against GitHub or LinkedIn:

- An "Industrial Trainee — Networking & Cybersecurity" role at a named
  employer (previously in `resume.md` / `certifications.md`)
- A specific IEEE membership ID number
- A third academic reference

If any of these are accurate, they're easy to add back — the IEEE ID and
the training role belong in `_data/awards.yml` / `_data/experience.yml`,
and the reference belongs in the "Academic references" section of
`resume.md`.

Also removed: two projects that appeared on the old home page and
`/projects/` page ("AI-Driven Self-Healing Networks" and "MEDeLIFE EHR")
had no basis in the CV, GitHub, or LinkedIn — they were dropped rather
than published under your name. A stray, unrelated auto-commit GitHub
Action (`auto-notebook.yml`, which rewrote and pushed to the repo on every
notebook upload) was also removed as an unnecessary source of fragility;
say the word if you'd like a safer version of that automation back.
