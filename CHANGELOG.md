# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
This project (not yet) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## aplus-v2501.1

### Removed

- removed the deprecated django-ckeditor fields

### Added

- Added PollDetail/TextareaWithCounter.jsx and PollDetail/ChoiceRow.jsx
- `Voting Options` section to PollDashboard/EditPollManagement.jsx
- new setting `A4_EMAIL_ATTACHMENTS` if you need more than the `email_logo.png` attachement in your emails
  - this allows you to add custom attachments to the emails, even those set in a4

### Changed

- Renamed and refactored PollDetail/PollQuestion.jsx into PollDetail/PollChoice.jsx
- Refactored PollDetail/CharCounter.jsx
- refactored static/Alert.jsx

## mb-v2412.1

### Fixed

- prevent a new comment to be posted multiple times when repeatedly clicking
  submit by disabling the button after it's clicked for the first time (#1428)
- fix error alerts not showing correctly when adding/editing comments
- fix console warning / broken code when editing comments (#1491)
- fix child comment success alert shown again after hiding and then showing the
  replies again. (#1532)
- replace removed turf `inside` function with `booleanPointinPolygon`

### Added

- extent the api mock in adhocracy4/static/__mocks__/api.js to include some
  comment endpoints
- add various tests for comments
- add option to allow unregistered users to vote in a poll:
  - the feature is controlled via a new django setting `A4_POLL_ENABLE_UNREGISTERED_USERS` to enable or disable it
- add a new captcha react component to integrate the captcha in the poll
- add a poll_voted signal which is sent when a user has voted on a poll.
- RatingBox takes an optional render function to customize rendering
- added `jest-dom` to tests, allowing for nicer matchers like `toBeInTheDocument`
- added a rating_api file to allow for more modular api calls

### Changed

- Comment model now uses the RateableQuerySet class to get ratings for a comment (#284)
- image upload for projects organised by date
- redesign AI report to be readable
- only show AI report when there's a useful label (catnodecis and catneutral don't
count as labels)
- Modified the input type for text inputs PollOpenQuestion.jsx and PollQuestion.jsx to textarea.
- Changed PollQuestion.jest.jsx
- added a new div to `Alert.jsx` with the class name `a4-alert__content` to keep    semantic structure consistent with mein berlin
- added a new class called `a4-alert__container` to `Alert.jsx`- **Breaking Change** The react_comments_async templatetag no longer returns the
  comment categories as a data attribute. The categories are now included in the
  data returned from the comment api endpoint if called with `categories=true`.
  If the templatetag is called with `with_categories=True` and the react comments
  are used they automatically fetch the categories, so no changes are necessary.
- added new modifier classes to `PollResults.jsx`, `PollOpenQuestion.jsx` and `PollQuestion.jsx` for customized paddings
- replaced `<span></span>` with react fragment to keep consistency- Ratings are now functional components
- RatingBox has been split into RatingBox and RatingButton
- redirect when logged out now goes back to specific comment if the object was a comment
- fixed a bug where the GeoJsonMarker would not update if passing new props for `icon`
- migrate renovate config
- update babel monorepo
- update dependency @maplibre/maplibre-gl-leaflet to v0.0.22
- update dependency @testing-library/jest-dom to v6.6.3
- update dependency @testing-library/react to v16
- update dependency black to v24.10.0
- update dependency bleach to v6.2.0
- update dependency django to v4.2.16
- update dependency django-allauth to v65
- update dependency django-filter to v24.3
- update dependency djangorestframework to v3.15.2
- update dependency easy-thumbnails to v2.10
- update dependency eslint-plugin-promise to v6.4.0
- update dependency esquery to v1.6.0
- update dependency factory-boy to v3.3.1
- update dependency faker to v33.1.0
- update dependency flake8 to v7.1.1
- update dependency husky to v9.1.7
- update dependency lint-staged to v15.2.10
- update dependency psycopg to v3.2.3
- update dependency pytest to v8.3.4
- update dependency pytest-cov to v6
- update dependency pytest-django to v4.9.0
- update dependency rules to v3.5
- update eslint packages
- update dependency @turf/turf to v7.1.0
- update dependency shpjs to v6


## aplus-v2406.3

### Fixed

- add missing get_blueprint_type_display to module model
- comments_async: fix child comments not being editable by creator
- comments_async: hide "Join the discussion" headline when editing
  a comment

### Changed

- make wording for ai report toggle more specific

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
