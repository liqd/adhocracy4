# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
This project (not yet) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## aplus-v2406.1

### Added

- react components for generating a leaflet map:
  - A basic map component that renders a polygon, tilelayer and zoom controls
  - MaplibreGL Tilelayer to implement `@maplibre/maplibre-gl-leaflet`
  - MarkerClusterLayer to implement `leaflet.markercluster`
  - MapPopup to provide basic html wrapping
  - AddMarkerControl to allow users to set a marker on a map within a
    constraining polygon
  - GeoJsonMarker to fetch the coords from GeoJson and render a jsx Marker
- added an utility in python to easily get all relevant map settings
- add/move ControlBarDropdown component from meinBerlin to a4
- add/move ControlBarSearch component from meinBerlin to a4. The placeholder
  text is now set via the `placeholder` prop.
- add/move Select compontent from meinBerlin to a4
- Add a new CommentControlBar component which uses ControlBarDropdown and
  ControlBarSearch for sorting and searching comments. There's no support for
  category filtering yet.
- **Breaking Change** Add a new subtitle "Discussion" above comment filters.
- comments_async/comment_form: add a span with class
  a4-comments_char-count-word which can be used to hide the trailing wording for the character count. The word will still be read by screenreaders.
- comments_async/comment_form: the cancel button is now wrapped in a div with class a4-comments__comment-form__actions__left.
- comments_async/comment_form: the action button is now wrapped in a div with class a4-comments__comment-form__actions__right.
- **Breaking Change** Added a heading to the comment_form when commenting is
  allowed. The heading can be controlled with the a4-comments__comment-form__heading-commenting-allowed" css class.

### Changed

- move the old comment search and filter into its own component
  CommentFilters
- **Breaking Change** Use the above mentioned CommentControlBar for sorting and
  filtering by default. You can pass `noControlBar` as props to comment_box to
  keep using the old filters.
- **Breaking Change** comments_async/comment_box: rename class visually-hidden to
  a4-sr-only as we want to move away from using bootstrap classes directly.
- **Breaking Change** comments_async/comment_form: the default height of the
  textarea has been increased from 46 to 75. We might have to add a way to set
  the initial height dynamically in the future.
- **Breaking Change** comments_async/comment_form: remove me-2 class from
  submitButton as we want to move away from using bootstrap classes directly.
  You can apply it to a4-comments__cancel-edit-input instead.
- **Breaking Change** comments_async/comment_form: rename general-form to
  a4-comments__comment-form__form to be more in line with BEM naming.
- **Breaking Change** comments_async/comment_form: wrap form elements in a form-group class according to
  mb styleguide. This might add an unwanted margin-bottom if used with
  Bootstrap.
- **Breaking Change** comments_async/comment_form: removed the placeholder from
  textarea.
- **Breaking Change** comments_async/comment_form: replace col with
  a4-comments__comment-form__actions on the div wrapping the cancel and action button. You
  can use @extend .d-flex, @extend .col-12 and @extend .col-sm-6 to retain
  bootstrap behavior.
- **Breaking Change** comments_async/comment_form: replace col with
  a4-comments__comment-form_terms-of-use on the the div wrapping the terms of
  use checkbox. You can use @extend .col-12 and @extend .col-sm-6 to retain
  bmotstrap behavior.
- update js and python dependencies

### Removed

- **Breaking Change** Removed the "Comments" headline in
  comment_box. This is replaced by the new "Discussion" subtitle above.
- removed peerDependencies from package.json to make updating js packages easier

### Fixed

- categories: make the icon form field optional, fixes category form not
  accepting a category without icon.


## mB-v2402.1

### Added
- add a changelog folder and readme with guideline for new changelog system
- add template tag for image alt text with test (!7481 a+)
- add CategoryAliasFactory and tests static get_category_alias()
- add LabelAliasFactory and tests static get_label_alias()
- tests for ImageMetadataMixin in ProjectBasicForm
- added initial_slide to context of module detail views
- adhocracy4/projects/mixins: extra context for insignts if insight model exists (#2492)
- gitignore: .python-version for pyenv
- retreival of image name to save as new image instance when project is duplicated
- custom migration for iframes to make them work with ckeditor5 (WARNING:
  backing up your database before running is recommended).
- added dependency beautifulsoup4
- added an ImageAltTextValidator to enforce alt text on img tags. The validator
  is used for project information and result.
- Add AiReport component to show the AiReport below user comments and in the
  dashboard
- Add SwitchButton component
- support for celery task queues
- template for github pull requests
- templatetag which disables iframes to stop them from loading if javascript is
  disabled

### Changed
- move CategoryFactory and LabelFactory to /test folder, so they can be used in other projects
- exports/mixins/items: show category and label alias in exports
- use CategoryAlias and LabelAlias in export if present
- apps/modules: change blueprint_type to char field (was creating migrations in forked projects after django upgrade to 4.x)
- apps/categories: change CategoryChoiceField for icons from moded field to simple field
  (was creating migrations in forked projects)
- apps/projects:
  add topics model/table
  make topics a m2m relation to projects
  stop making use of django-multiselectfield as it's not maintained
- apps/projects: topics should be first created and then added to project in migration
- replace django-ckeditor with django-ckeditor-5
- update helptext for project information and result with info about image alt
  text and move them from the model to the form
- reports: the serializer now also return the "username" and "created" fields
- refactor follow to be functional and add aria described by for when no alert shown and use a4 prefix for classes so external style liberies can be used (story !7618/7701)
- redirect to login page when follow button is pressed and user is not logged
  in
- **Breaking Change** Deprecated
  dashboard.mixins.DashboardComponentDeleteSignalMixin,
  for forms / POST requests use
  dashboard.mixins.DashboardComponentFormSignalMixin instead.
  DashboardComponentDeleteSignalMixin will be removed in the next version.
- make django translation mock return the original text
- psycopg to 3.1.12
- Django from 3.2.20 to 4.0
  - added migrations for max_length
- Django-allauth from 0.54.0 to 0.55.0 to be compatible with django 4.2
  unique email is now only a constrain if it is already verified.
  This takes place if ACCOUNT_UNIQUE_EMAIL is enabled in the settings
- Django from 4.0 to 4.1
  Reverse relations need to be saved before being called from the object they relate
- Django from 4.1 to 4.2
  any fields modified in the custom save() methods should be added to the update_fields keyword argument before calling super()
  retrieve referer in requests from headers instead of META

### Fixed
- fixed comment infinite scrolling not working
- fixed anchor links and scrollTo not working when comment was not on the first
  pagination page
- fix comment count not including child comments on module tiles, lists, map
  pins and detail view
- apps/projects: project's topics_name property should iterate through m2m relation
- delete logic moved to form_valid method after django upgrade in dashboard component mixin
- duplicated image path when a project gets duplicated in the dashboard
- follow templatetag is setting the project slug instead of the name
- fix map attribution not being set for vector tile maps if loaded from settings
- fix comment count plurals not updating properly
- fix an error when opening a module which is marked as draft in a multimodule
  project

### Removed
- removed RichTextCollapsibleField
- removed RichtTextCollapsibleMixin
- django-background-tasks from settings and requirements
- requirements: django-multiselectfield.
  Project.topics are now m2m with Topic, as the django-multiselectfield lib has not been supported.
  see the [docs](https://github.com/liqd/adhocracy4/blob/main/docs/topic_enums.md) for more info.

## mB-v2307

### Added

- image alt-text field to project model and form. (!1425)
- image mixin to ensure all images added in projects and related models require meta data in form of alt-text and copyright. (!1425)
- add CategoryAliasFilter and LabelAliasFilter for category and label filters with custom label (#1436)
- add markdown rules to editorconfig

### Changed

- actions: only create actions for phases and projects if the project is not
  a draft (!1437)
- reformat CHANGELOG.md
