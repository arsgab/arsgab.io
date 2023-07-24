---
title: Building static generated photo site with Python
title_label: how-to
subtitle: And deploying it via GitHub Actions
lead: For years, I was mostly frustrated with a process of publishing any content in the internet (well, along with many other internet-related things).
slug: python-ssg
date: 2023-07-01
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

You mostly have two options to publish something into the Web: to use some established content platform (and fully depend on its vendor), or to setup
your own (and, therefore, to maintain all related infrastructural complexity).

So, as a proof of concept, I wanted to find some kind of compromise, to create personal publishing micro-platform, where I could have full control over my content, but without need to manually spin up virtual machines or to fix issues after next minor Kubernetes updates or to handle with deployment environment in any other way.

Long story short: after month of cycling in Türkiye, I had a lot of photos that I liked and wanted to be presented not only in Instagram (at least, because many of it were in landscape orientation :-). As a result, I've made **[photos.arsgab.io](https://photos.arsgab.io)** — and actively filling it up for several months with pictures from my last travels. I can definitely say now that I am pleased with a "platform" I've built, and in this article I would like to cover some technical decisions and solutions that were made during the development.

[aside]
It's needed to say that I was inspired by [this beautiful website](https://photos.cherenkevich.com){: newtab } made by Aleksey Cherenkevich and I adopted a lot of ideas from it
[/aside]

## {#concepts} Primary concepts

So, there was set of core assumptions upon this "project":

[aside]
I will reference Markdown as M↓, just for fun
[/aside]

- I want a static generated site without running any backend or database behind it. On one side I have batch of text (Markdown) files, on another — batch of well-done HTML files;
- as a developer, I don't need any CMS or visual editor to work with content. Plain text editor and `git` are pretty enough for me;
- on the other hand, as a developer, I want first-class developer experience with content preparing and publishing — here I mean fast HTML/frontend artifacts building process and deployment;
- client-side performance (a.k.a. "Green PageSpeed/Lighthouse" metrics) is a priority, of course.

And in order to build static generated photos site, you need to make some choices for, well, the tool or library which will generate static content, the way you will store and serve your photos and at least how styles for images collections will be built and delivered. In next sections I will try to cover these points.

## {#engine} Chosing SSG engine

I've heard a lot about static site generation technics for years, but I've had no real experience with it prior to this project. I chose <cite>[Pelican](https://getpelican.com/)</cite> as SSG engine — mostly because it's writen in Python (and Python is my primary language; the vast majority of other SSG libraries written in JavaScript, and I didn't want to mess with JavaScript at any way). Pelican also uses <cite>Jinja</cite> as rendering engine, which is very familiar for me too.

[aside]
Jinja is a Python general-purpose templating engine, which is used, e.g. in Ansible
[/aside]

Well, there are some details in Pelican that I am not very happy with: *a)* its configuration system (which is rather complex and not thoroughly documented, so it took time to set up things in a way that I wanted) and *b)* the Jinja environment object hidden inside (you can add custom filters/functions by registering it in `sys.path`, but it's inappropriate for me, and furthermore, I needed this object to render my custom templates, so I ended up with passing environment reference via `contextvars`), but it does what it should do rather well — transforming M↓ sources into HTML in acceptable time — and has nice overall design, so I would definetly recommend it to use.


## {#images} Handling images

OK, this is a tricky part. To deliver your local images to browser in a proper way, you need a bunch of things to be done:

1. Some publically available media storage, obviously — a place where you can upload your image files and then deliver it in effective way (so, it might have some CDN above);
2. The interface to transfer local files to your storage of choice;
3. The image processing server to convert/resize/optimize source images automatically;
4. The code generator tool that prepares HTML markup for responsive images. Yeah, embedding image into webpage nowadays is not just placing it into the `<img>` tag.

Let's see, what we can do with it, step-by-step.

### {#images-storage} The storage

Just before this project I've tried self-hosted <cite>[NextCloud](https://nextcloud.com/)</cite> as the alternative for Dropbox/Google Drive/iCloud Documents, and it worked good for me — so I've decided to use this installation to store my photos as well. To do it, I simply opened one of directories in my private "cloud" in `nginx` location and then proxied it with <cite>Cloudflare</cite>.

So, the store is my VPS, and I upload pictures to it just by copying into local folder on my computer, and the folder is synced with remote source via NextCloud client.

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

<aside Markdown=1>
You can check out results for your own via [this URL](https://pagespeed.web.dev/analysis/https-photos-arsgab-io-ege-2/4h3v293km1?form_factor=mobile)
</aside>

All source code for my personal sites is available in [GitHub repo](https://github.com/arsgab/).

*[DX]: Developer eXperiense
*[SSG]: Static Site Generator
*[CDN]: Content Delivery Network
*[HTML]: HyperText Markup Language
*[CMS]: Content Management System
*[VPS]: Virtual Private Server
