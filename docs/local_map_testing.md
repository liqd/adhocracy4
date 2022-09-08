# Testing maps locally
To have access to the maps from berlinonline.de we need to send a header with the origin set to meinberlin-dev.liqd.net.

To do that in firefox, install https://addons.mozilla.org/en-US/firefox/addon/simple-modify-header/ and create new header:

    Url Patterns: https://maps.berlinonline.de/*
    Action: Modify
    Header Field Name: origin
    Header Field Value: https://meinberlin-dev.liqd.net/
    Apply on: Request

P.S.: keep in mind to disable the policy when you're visiting mein.berlin.de where this will break the maps :)
