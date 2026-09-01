# Md Miadul Islam Nizzan — Portfolio

Personal portfolio built with Jekyll and GitHub Pages. Content lives in
YAML files under `_data/`, so updating projects, skills, research, or
experience never requires touching HTML.

**Live at:** https://miad979.github.io

## Structure

```
_config.yml     Site-wide settings, nav menu, contact/social links
_data/          YAML content: projects, skills, research, education, experience, awards, certifications
_layouts/       Page templates (default, projects, research, skills)
_sass/          Base stylesheet partials
style.scss      Main stylesheet (colors, fonts, layout)
index.html      Home page
*.md            About / Projects / Research / Skills / Resume / Contact page bodies
assets/         Resume PDF, JS
images/         Profile photo, project images
.github/workflows/deploy.yml   Auto-builds and deploys on every push
```

See **MAINTENANCE.md** for step-by-step instructions on updating content,
styling, and troubleshooting deploys.

## Local development

```bash
bundle install
bundle exec jekyll serve
# http://localhost:4000
```

## Deployment

Push to `master` — GitHub Actions builds the Jekyll site and publishes it
to GitHub Pages automatically. No manual steps required.

## Contact

- Email: nijjon12@gmail.com
- GitHub: [@miad979](https://github.com/miad979)
- LinkedIn: [Md Miadul Islam Nizzan](https://www.linkedin.com/in/md-miadul-islam-nizzan-450b70262/)
