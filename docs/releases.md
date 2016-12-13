Performing releases on A4
=========================

Basic properties of our release cycle:

- version numbers follow semantic versioning
- current development version is on branch `master`
- releases can only be on release branches named `releas<major>.<minor>`
- patch releases are tags on the minor branch

How to perform a release
------------------------

    OLD_VERSION=0.1.0
    NEW_VRSION=0.2.0

    # ensure last release branch is included
    git checkout master
    git merge release0.1

    # create release branch
    git checkout -b release0.2

    # update version number
    sed -i 's/"version": "0.1.0"/"version": "0.2.0"/' package.json
    sed -i "s/version='0.1.0'/version='0.2.0'/" setup.py
    sed -i "s/Development/Release 0.2.0/" CHANGES

    # perform release
    git commit -m "Release version 0.2.0"
    git tag --sign r0.2.0
