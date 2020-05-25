# Testing maps locally
To have access to the maps from berlinonline.de we need to send a header with the origin set to meinberlin-dev.liqd.net.

To do that in firefox, install https://addons.mozilla.org/en-US/firefox/addon/modify-header-value/ and create new header:

    url: https://maps.berlinonline.de/
    header name: origin
    header value: https://meinberlin-dev.liqd.net/
    after adding the policy, enable the modify checkbox

P.S.: keep in mind to disable the policy when you're visiting mein.berlin.de where this will break the maps :)
