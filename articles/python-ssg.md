---
title: Building static generated photo site with Python
title_label: how-to
subtitle: And deploying it via GitHub Actions
lead: For years, I was mostly dissatisfied with a process of publishing any content in the internet (well, along with many other internet-related things).
slug: python-ssg
date: 2023-06-01
comments: on
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

You have, mostly, two options if you want to publish something to the Web: to use some established content platform — and fully depend on its vendor, or to setup
your own — and, consequently, to maintain all infrastructural complexity.

So, as a proof of concept, I wanted to find some kind of compromise, to create personal publishing micro-platform, where I could have full control over my content, but without need to manually spin up virtual machines or to fix issues after next minor Kubernetes updates or to handle with deployment environment in any other way.

Long story short: after month of cycling in Türkiye, I had a lot of photos that I liked and wanted to be presented not only in Instagram (at least, because many of it were in landscape orientation :-). As a result, I've made **[photos.arsgab.io](https://photos.arsgab.io)** — and actively filling it up for several months with pictures from my last travels. I can definitely say now that I am satisfied with a "platform" I've built, and in this article I would like to cover some technical decisions and solutions that were made during the development.

[aside]
It's also needed to say that I was inspired by [this awesome website](https://photos.cherenkevich.com){: target="_blank" rel="noopener"} made by Aleksey Cherenkevich and adopted a lot of ideas from it
[/aside]

## {#concepts} Key concepts

- to build simple publishing platform,
- DX as internal priority,
- client performance as a "product" metric (aka "Green PageSpeed/Lighthouse")

## {#engine} Chosing SSG engine

(some words about chosing Pelican and why)

## {#images} Handling images

OK, this is a tricky part. To deliver your images to your reader in a proper way, you need a bunch of stuff:

1. Obviously, some publically available media storage — a place where you can upload your image files and then deliver it efficently 
(so, it should also have CDN above);
2. The interface to transfer your local files into storage;
3. The image processing server to convert/resize/optimize source images automatically;
4. The code generator tool that prepares HTML markup for responsive images (yeah, embedding image into webpage nowadays is not just placing `<img>` tag).

Let's see, what to do with it step-by-step.

### {#images-storage} The storage

(NextCloud + CloudFlare stuff)

### {#images-processor} The processor server

(imgproxy setup)

### {#images-codegen} The code generator

(`[pic]` and MarkDown block parser)

## {#static} Handling static files

(CLI-only postcss + terser setup, hashsum manifest.json generation)

## {#details} Last details

## {#deploy} Deployment

(Some words about GitHub Actions and deployment into Pages)

## {#results} Results

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
