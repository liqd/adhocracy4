# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
This project (not yet) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- image alt-text field to project model and form. (!1425)
- image mixin to ensure all images added in projects and related models require meta data in form of alt-text and copyright. (!1425)
- add CategoryAliasFilter and LabelAliasFilter for category and label filters with custom label (#1436)
- add markdown rules to editorconfig

### Changed

- actions: only create actions for phases and projects if the project is not
  a draft (!1437)
- reformat CHANGELOG.md
