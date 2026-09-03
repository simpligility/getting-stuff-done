---
name: trinodb-website
description: Work on the Trino project website in the trinodb/trino.io repository. Covers the Jekyll and Netlify setup, the local build, blog post conventions and front matter, the data files behind the ecosystem, users, and sponsors pages, the Trino Community Broadcast episode collection, the custom Liquid tags, and the linking traps. Child skill of the trinodb family. Load it before adding or editing any content on trino.io.
---

# Trino website

Use this skill when working in a clone of
[trinodb/trino.io](https://github.com/trinodb/trino.io), the source of the
[Trino website](https://trino.io). It builds on the shared context in the
`trinodb` skill, which covers the organization, the contribution workflow,
and the documentation style guide that applies to website content as well.

Writing style for all site content follows the
[Google developer documentation style guide](https://developers.google.com/style),
as described in the `trinodb` skill. When writing for Manfred, the
conventions in `manfred-writing` apply on top of it.

## The stack

The site is built with [Jekyll](https://jekyllrb.com) 4.4 and hosted on
[Netlify](https://www.netlify.com). Content is Markdown and HTML with Liquid
templating. Netlify builds with `bundle exec jekyll build` and publishes
`_site`, using the Ruby version declared in `netlify.toml`. Plugins in use are
`jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-compose`, and `jekyll-paginate`.

## Repository layout

| Path | Contents |
|---|---|
| `_posts` | Blog posts, one Markdown file per post |
| `_episodes` | Trino Community Broadcast episodes, one file per episode |
| `_data` | `tools.yml`, `users.yml`, and `sponsors.yml` drive the generated pages |
| `_layouts` | `default`, `page`, `blog`, `post`, and `episode` |
| `_includes` | Header, footer, hero, table of contents, and the tool and user list renderers |
| `_plugins` | Custom Liquid tags in `youtube.rb` and `download.rb` |
| `assets/blog` | Blog post images, either a single file or a per-post directory |
| `assets/images/logos` | Tool, user, and sponsor logos |
| `ecosystem` | The ecosystem pages that render `tools.yml` |
| `development` | Contribution process, roles, and vision pages |
| `blog`, `broadcast` | Index, archive, and feed pages for the two collections |
| `_config.yml` | Site configuration and custom variables |
| `netlify.toml` | Build settings and every redirect |

## Build and preview locally

The README documents the setup. The essentials:

```bash
PATH=`brew --prefix`/opt/ruby/bin:$PATH
gem install bundler -v '=2.6.9'
bundle install
./jekyllRun.sh
```

The site then runs on `http://localhost:4000`.

Install the bundler version recorded at the end of `Gemfile.lock` rather than
whatever is current. A mismatch fails with a `cannot load such file` error
pointing at a missing `bundler-<version>/exe/bundle`, which reads like a broken
Ruby install but is only a missing gem version. Reinstall the pinned version and
run `bundle install` again.

Posts and episodes with a future date do not render by default. Pass `--future`
to see them:

```bash
./jekyllRun.sh --future
netlify dev -c 'bundle exec jekyll serve --future'
```

Use `netlify dev` instead of the helper script to exercise the redirects in
`netlify.toml`, which plain Jekyll does not apply. Verify anything that depends
on a redirect that way. Use `netlify dev --live` for a public tunnel when
checking rendering on a phone.

A plain `bundle exec jekyll build --future` is the quickest way to confirm that
new content compiles and that Liquid tags such as `post_url` resolve. It writes
to `_site`, which is ignored by git.

## Blog posts

Create a file in `_posts` named `YYYY-MM-DD-slug.md`. The date in the file name
sets the publication date and the permalink, which `_config.yml` defines as
`/blog/:year/:month/:day/:title.html`.

Front matter:

```yaml
---
layout: post
title: "Trino JavaScript packages are back on npm"
author: "Manfred Moser"
excerpt_separator: <!--more-->
image: /assets/blog/some-image.png
---
```

- `title` uses sentence case.
- `author` is a plain string of names only, with several authors separated by
  commas, such as `"Manfred Moser, Mateusz Gajewski"`. Never add a company or
  any other affiliation to an author name. The Trino blog credits people, not
  their employers. Around eighteen posts carry a company name against this
  convention, almost all of them from 2019 to 2021, and they are candidates for
  cleanup rather than a precedent to follow.
- `excerpt_separator` with a `<!--more-->` marker in the body controls what the
  blog index shows as the preview. Put the marker after the opening one or two
  paragraphs.
- `image` is optional. When present, the post layout renders it at the top of
  the post, above the body, so there is no need to repeat it in the content.

Images go in `assets/blog`, either as a single file named after the post or in a
per-post directory for a post with several images. Reuse an existing logo from
`assets/images/logos` when a post continues an earlier topic, which keeps the
visual connection between related posts.

Commit messages for post additions follow the pattern used in the repository,
such as `Add blog post about Java 24 upgrade`.

## Linking conventions

Internal links are relative to `site.baseurl` and point at the built `.html`
path:

```markdown
[Trino Slack]({{ site.baseurl }}/slack.html)
[Trino Web UI]({{ site.baseurl }}/docs/current/admin/web-interface.html)
```

Link to another post with `post_url` and the file name without the extension,
which fails the build if the target does not exist:

```markdown
[the earlier post]({{ site.baseurl }}{% post_url 2024-11-18-javascript %})
```

Older posts use `{{site.baseurl}}` without spaces. Both forms work.

Two traps:

- **Ecosystem anchors.** `/ecosystem/client` and `/ecosystem/client.html` are
  redirects to the ecosystem index, and a redirect drops the fragment. A link
  such as `/ecosystem/client#vscode` therefore lands on the index rather than on
  the entry. Link to the real page instead, such as
  `/ecosystem/client-application.html#vscode` or
  `/ecosystem/client-driver.html#javascript`. The fragment is the `anchor` value
  from `_data/tools.yml`, which is not always the obvious name. Some old posts
  still carry the broken form.
- **Documentation links.** `/docs/*` proxies to the hosted documentation, so a
  documentation page that was renamed or removed in a later Trino release breaks
  a `docs/current` link silently. Confirm the URL before using it.

## Data-driven pages

Three data files generate large parts of the site. Editing an entry is the
normal way to update the ecosystem, users, and sponsors pages, and there is no
page to edit alongside it.

`_data/tools.yml` drives the [ecosystem pages]({{ site.baseurl }}/ecosystem/).
Every entry has `name`, `anchor`, `category`, `owner`, `logo`, `logosmall`,
`description`, and `links`:

```yaml
- name: Alluxio
  anchor: alluxio
  category: data-lake
  owner: trinodb
  logo: /assets/images/logos/alluxio.png
  logosmall: /assets/images/logos/alluxio-small.png
  description: |
    Multi-paragraph Markdown description.
  links:
    - urltext: Alluxio
      url: https://www.alluxio.io/
```

The `category` value must be one of `client-driver`, `client-application`,
`data-lake`, `data-source`, or `add-on`, which selects the page the entry
appears on. The `owner` value is `trinodb` for anything the Trino community
maintains and `other` for everything else, which splits each page into an
official and a third-party section. The `anchor` value is the URL fragment, so
keep it stable once published.

`_data/users.yml` drives the home page and the users page, and adds `highlight`
and `testimonial` fields. `_data/sponsors.yml` drives the sponsor display and
adds `highlight`, `position`, and `logobalanced`.

Logos live in `assets/images/logos` as a matched pair, a full size image at
500 by 400 pixels and a `-small` variant at 250 by 200 pixels, both PNG.

## Trino Community Broadcast episodes

Episodes are a Jekyll collection in `_episodes`, one file per episode, named
after the episode number, such as `69.md`. The `episode` layout reads `title`,
`date`, `image`, `introduction`, `lang`, `youtube_id`, `wistia_id`, and
`sections`. The `sections` list is a sequence of `time` and `title` pairs that
renders the chapter list.

To turn a recording into the topic list and summary that these fields need, use
the `trinodb-contributor-call-processing` skill.

## Custom Liquid tags

Three tags are defined in `_plugins` and available in any page:

- `{% youtube VIDEO_ID %}` embeds a responsive YouTube player.
- `{% downloadGH trino-server .tar.gz %}` renders a download button for a GitHub
  release asset of the current Trino version.
- `{% downloadMC trino-jdbc .jar %}` renders the same for a Maven Central
  artifact. Note the constraint recorded in the `trinodb` skill, that
  server tarballs and plugin archives are no longer published to Maven Central
  as of Trino 477, so new download buttons for those belong on `downloadGH`.

Both download tags read `site.trino_version`, so they never need a hardcoded
version.

## Trino release bumps

A new Trino release needs a single change, the `trino_version` value in
`_config.yml`. Every download button and version reference derives from it. The
commit convention is `Update to Trino 483`.

## Redirects

Every redirect lives in `netlify.toml` rather than in front matter. Add one when
a page moves or when an old URL is still linked from elsewhere. Remember that a
redirect discards the fragment, so a redirect is not a substitute for an
anchored link.

The `/blog/assets/*` redirect maps to `/assets/blog/:splat`, which is why some
older posts reference images under a `/blog/assets` path.

## Contributing

The website follows the same process as the rest of the project, described on
the [development process page](https://trino.io/development/process.html) and in
the `trinodb` skill. Fork the repository, keep `upstream` pointing at
`trinodb/trino.io`, work on a branch, and open a pull request.

Commit messages follow the Chris Beams conventions. The process page explicitly
prohibits AI attribution footers such as `Co-authored-by:` or `Assisted-by:` on
Trino commits, and that applies to this repository too, including when preparing
work for Manfred.

Before opening a pull request:

1. Build with `bundle exec jekyll build --future` and confirm there are no
   errors.
2. Preview the changed pages in a running server.
3. Check every new link, especially documentation and ecosystem links.
4. Confirm that new Markdown is hard wrapped at 80 characters, apart from long
   URLs that cannot be broken.
