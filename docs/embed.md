# Embedding

Embedding allows to include parts of adhocracy on other websites. A common use
case would be the website of a municipal administration that embeds an idea
collection.  This allows users to access (and eventually contribute to) the
participation right where they are instead of going to a third party platform.

## TL;DR

You can embed any project with the following code:

    <iframe
        height="500"
        style="width: 100%; min-height: 300px; max-height: 100vh"
        src="http://example.com/projects/{slug}/"
        frameborder="0">
    </iframe>

## Terms

-   iframe: The HTML element that enables embedding. It is basically a virtual
    screen that is completely isolated from the embedding website for security
    reasons.
-   platform: The regular, non-embedded version of adhocracy. Some
    functionality is only available on the platform.

## Inspiration and Approaches

While working on this concept we looked at several existing embedding systems
and found three distinct categories:

-   *Widgets* with limited interaction (e.g. [twitter timeline](https://dev.twitter.com/web/embedded-timelines))
-   *Applications* (e.g. [soundcloud player](https://help.soundcloud.com/hc/en-us/articles/115003449627-The-HTML5-embedded-player))
-   Functionality that *integrates* into the website (e.g. [disqus](https://disqus.com/))

## Our chosen approach

It was hard to decide between application and integration, but we finally
landed on application.

We embed fully functional projects. Anything outside of a project (e.g.
managing projects, changing account settings) happens on the platform.

In the iframe, we load a JavaScript application called the *embed shell* that
loads the actual contents via ajax.  Whenever a link is clicked or a form is
submitted, the corresponding event is intercepted, the request is made via ajax
and the response is put back into the DOM.

The behavior of links and forms can be modified by adding a `data-embed-target`
attribute. Possible values are:

-   internal (default): use the mechanism described above
-   external: open in top frame
-   ignore: do not intercept the event (useful if other event handlers are
    registered for this element)
-   popup: open link in popup (useful for login)

## Restrictions on the overall application

The embed shell uses the regular views. This way, we do not need to duplicate
all views. However, this also means that you need to be aware of some general
restrictions:

-   Add `data-embed-target="external"` to all links and forms that should not
    open inside of the iframe.
-   Do not trigger navigation from JavaScript
-   Do not add submit handlers to forms that do not have
    `data-embed-target="ignore"`.
-   Do not use relative-path URLs:

        // works
        https://example.com/foo/bar
        /foo/bar
        ?ordering=created
        #top

        // does not work
        foo/bar
        ./foo/bar
        ../foo/bar

-   If you need to run JavaScript on page load, make sure that it also runs
    when navigating in the embed shell. There are several strategies:

    -   Take advantage of event propagation:

            $(document).on('click', '.my-special-selector', function () {…})

    -   Use the `a4.embed.ready` custom event whereever you use
        `$(function () {…})` (formerly `$(document).ready()`).

-   For cases where you cannot easily add data attributes to elements (e.g.
    links in user generated content), you can wrap it in a block with class
    `rich-text` instead. A simple way to do this is to use wagtail's `richtext`
    filter instead of `safe`.

-   The embed shell will only show content if it is returned with a 200 code.
    Any other code will produce an error alert. This works well with django's
    default views (e.g. for forms). But you need to be aware when writing your
    own views.

## Challenges

This is a more or less complete list of the challenges we found while working
on embedding. It is documented here so we do not make the same mistakes again.

### Size

Most HTML elements grow with their content, iframes do not. There are three
ways to handle this:

-   Have content in a fixed height. This conflicts with accessibility, most
    notably [WCAG 2.0 success criterion
    1.4.4](https://www.w3.org/TR/WCAG20/#visual-audio-contrast-scale).
-   Use JavaScript to mimic the behavior of other HTML elements. It is
    surprisingly hard get this right (e.g. without infinitly alternating
    between two sizes).
-   Make the contents adapt to the available size. This means that you will
    have additional scrollbars in the embed which can be annoying, especially
    on small screens.

### Viewport

The contents of the iframe do not know what is actually on the screen because
the iframe acts as a virtual screen. So anything that requires this information
does not work (e.g. modals, sticky navigation). Solutions:

-   Modals are displayed close to the position where they were triggered,
    because we can assume that this is on the screen.
-   If we choose a fixed-size and make it small enough, we can assume that the
    complete iframe is on the screen.

### State

If I reload a website, its general state remains the same (some detail may be
lost though). This is because the state is saved in the URL. The URL is updated
on each navigation. But navigation inside of an iframe does not update the URL
in the browser. So on reload the embed is reset to its initial state. The same
is true for any other use of the URL, e.g. bookmarking or social sharing.

This is not necessarily an issue. You can just live with it. It is also
possible to write some JavaScript to encode some additional state in the outer
URL. But it is very hard to do that without knowing something about the
embedding website.

### Phishing

Phishing is generally countered by checking the URL in the browser. The URL of
iframes is not visible by default, though. This means that any security related
actions (e.g. login) should not be done in the iframe, but in a pop-up or on
the platform.

### Social Share

When a user shares something on facebook or other social media, the information
that is actually shared is a URL. The social media site will also try to
extract some additional metadata (title, description, image) from that URL.

If we think about embedding, it is important to ask: Which URL do we want to
share (platform or embedded) and how can we provide the metadata? The answer to
the first question is: It depends.

If we share the platform URL, we can just add the metadata to that page. But if
the shared URL points to the page where our content is embedded, we have no
control over the metadata. If we want to have that control, we can provide an
additional service that just provides metadata and redirects for social media
and redirects humans to the embed.

### Third Party Cookies

Websites can set cookies in the browser to preserve some user-specific state,
most importantly their session. Without them, it would be impossible to log in.

There is a distinction between 1st-party-cookies (set by the page you are
currently visiting) and 3rd-party-cookies (set by other pages).
3rd-party-cookies are often used by advertisement companies to track users. So
it is a common privacy recommendation to disable them.

When embedded, we also are a 3rd party, so our cookies may get blocked. There
is no practical way around this other than requiring users to enable
3rd-party-cookies.

### Broken Visual Hierarchy

If the embed has its own header with a logo and login, it might look out of
place when embedded. You need to carefully craft the embed UI to make it work
in different contexts.

### Public API

Once people start embedding your page, the embedding API needs to be stable. In
most cases it is close to impossible to notify everyone to change their embed
codes.

### Account Integration

The whole point of embedding is lowering the entry barrier for new users. This
works even better if the account system is integrated with the embedding
website so that no additional login is required for participation.

## Possible extensions

-   Currently, it is only possible to embed full-functioning projects. Other
    options may be added under the `/embed/` prefix, optionally using the embed
    shell.
-   The embed shell sends an additional `X-Embed` header with every request.
    Views might react to that by generating HTML that is optimized for
    embedding.
