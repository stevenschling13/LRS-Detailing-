# Photos folder

This folder holds before/after detail photos for the gallery section.

## Naming convention

Use sequential filenames:

- `01.jpg`
- `02.jpg`
- ...
- `08.jpg`

## Recommended image specs

- Up to 1600×1200
- JPG or WebP
- Under 300KB each

## After adding photos

Edit `/index.html`, search for `class="ph"`, and replace each placeholder `div` with:

```html
<img src="/photos/01.jpg" alt="Before and after detail of a 2019 Honda CR-V interior" width="800" height="600" loading="lazy" decoding="async" />
```

Always include explicit `width` and `height` so the browser can reserve layout space (prevents cumulative layout shift). Match the aspect ratio of the file. Write a real `alt` description for each photo — what's in it, not just "before and after".
