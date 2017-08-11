# SoftwareListing

a simple tool for making static software listing websites

## About

SoftwareListing takes a directory of "item" metadata files
and generates a static website that includes a "listing" of
these items and pages for each item. The page generation is
based on HTML templates that can be customized as needed.

## Usage

Generate a static sample site with

`python ./src/swlisting.py ./listing ./dist`

By default, SoftwareListing is very barebones and you
will likely need to modify or even create your own template.
See the included sample template in `template/` for reference.

### Adding Templates

By default, SoftwareListing includes the following templates:

- `web` - Links to a webpage
- `desktop` - Provides downloads for Windows, macOS, and Linux

For example, to add a template for an AUR package,
create `template/items/aur.html` and put whatever
mustaches you need; for example, the `web` template looks like this:

```html
<h3>{{ name }}</h3>
<p>{{ desc }}</p>
<div>
  <a class="btn btn-default btn-small ripple" href="{{ page }}">View</a>
</div>
```
