---
title: Building statically generated photo site
title_label: how-to
subtitle: And deploying it via GitHub Actions
lead: For years, I was mostly dissatisfied with a process of publishing content in the internet (well, among many other internet-related things).
slug: python-ssg
date: 2023-06-01
cover:
    bg_color: #333
    text_color: orange
    image: iso/rabbit.png
    filter: invert(1) grayscale(1) contrast(1.2)
    mix_blend_mode: screen
    gradient_angle: -45
footer:
    text: Cover image by <cite>Gerd Arntz</cite>
---

Basically you have two options to do this: to use some ready content platform (and to depend on its vendor) or to setup
your own (and to handle all infrastructure complexity).

## [#goals] Primary goals

- to build simple publishing platform,
- DX as internal priority,
- client performance as a "product" metric (aka "Green PageSpeed/Lightroom")

## [#engine] Chosing SSG engine

(some words about chosing Pelican and why)

## [#images] Handling images

OK, this is a tricky part. To deliver your images to your reader in a proper way, you need a bunch of stuff:

1. Obviously, some publically available media storage — a place where you can upload your image files and then deliver it efficently 
(so, it should also have CDN above);
2. The interface to transfer your local files into storage;
3. The image processing server to convert/resize/optimize source images automatically;
4. The code generator tool that prepares HTML markup for responsive images (yeah, embedding image into webpage nowadays is not just placing `<img>` tag).

Let's see, what to do with it step-by-step.

### [#images-storage] The storage

(NextCloud + CloudFlare stuff)

### [#images-processor] The processor server

(imgproxy setup)

### [#images-codegen] The code generator

(`[pic]` and MarkDown block parser)

## [#static] Handling static files

(CLI-only postcss + terser setup, hashsum manifest.json generation)

## [#deploy] Deployment

(Some words about GitHub Actions and deployment into Pages)

## [#results] Results

Full control over publishing process, high-speed "releases", most time for "creative" work (layout, build editorial).

And what about client-side performance?

[pic src="ssg/pagespeed-report.png" caption="PageSpeed results for random collection page" bordered]

Well, not so bad for a page full of high-resolution images.

<aside markdown=1>
You can check out results for your own via [this URL](https://pagespeed.web.dev/analysis/https-photos-arsgab-io-ege-2/4h3v293km1?form_factor=mobile)
</aside>

All source code for my personal sites is available in [GitHub repo](https://github.com/arsgab/).

*[DX]: Developer eXperiense
*[SSG]: Static Site Generator
*[CDN]: Content Delivery Network
*[HTML]: HyperText Markup Language
