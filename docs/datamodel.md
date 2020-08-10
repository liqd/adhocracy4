adhocracy4 data model
=====================

Adhocracy4 is a library to implement online participation software. It
heavily relies on the Django webframework.

Examples of using adhocracy4 are [a+](https://github.com/liqd/adhocracy-plus),
[meinBerlin](https://github.com/liqd/a4-meinberlin) and
[Civic Europe](https://github.com/liqd/a4-civic-europe). The first two being
online participation platforms implementing different processes like idea
collections or debates, and the latter using adhocracy4 as the basis for a
transparent idea challenge.

This document describes some important constraints concerning the data models
of the software using adhocracy4. It also shows the available options
to extend the data model.

The adhocracy4 data model is composed of various django apps. The `a4projects`,
`a4modules` and `a4phases` provide the basic infrastructure to model
participation processes. In order to write a well adapted participation
software, additional apps can be created that base on the functionality on
adhocracy4 and provide more features.

participation process model
---------------------------

The adhocracy4 process model always replicates the following data model: A set
of organisations on the platform each run their own participation projects.
A project can have different modules concerning the same topic. Most commonly
only one module per project is used, though.
Each module shares its data and will be structured into a consecutive number of
steps (called phases). In a phase (or step) objects in the data collection can be
created, updated or enhanced with more information and feedback. Phases can
share their dataset among each other, and are likely to do so if they are
defined in the same django app. Phases from different django apps should not
share a module. Each phase has a type which provides the possibility to alter
its implementation. Each django app can register a phase type on startup.

entity relation model
---------------------

    organisations <1--n> projects <1--n> modules <1--n> items
                                                          |
                                                          |- ideas
                                                          |- documents

                                                 <1--n> phases

### organisation

-   container of projects
-   can be overridden easily (pluggable)
-   must expose initiators (via `has_initiator` method)

### projects

-   map a participation project / process in the real world
-   allow to specify local moderators and participants (user roles)
-   contains containers of participation content (modules)
-   exposes moderators / members (via `has_member` or `has_moderator` method)
-   provides an `is_archived` flag, allowing to distinguish projects with
    finished participation phases that may still be active in other ways from
    truly archived projects

### modules

-   follows automatically a given timeline (phases)
-   container of items produced by a specific django app in the context of a
    project

### phases

-   a period in which participation is possible (has start and end date)
-   limits which and how items can be created, or altered via rules and permissions
-   has a phase type set

### phase types (also called phase content)

-   not stored in database, registered at setup
-   each django app can define new phase types
-   describes possible actions in current phase
    -   used for permissions
    -   used to enable / disable call-to-actions
-   sets content of the participation tab in project detail view

user generated content
----------------------

In a participation project users are expected to create, update, enhance or
evaluate content. There are two basic options in Adhocracy4 to model user
generated content:

-   extend item model
-   use generic foreign keys

For both options it is useful to extend `adhocracy4.models.base.UserGeneratedContentModel`.
This ensures that all user generated items have some basic fields.

All user generated content has a `project` property, which links it to a
project. This is required for permissions to work. If a user wants to moderate
a comment, the system must check if she is a moderator of the project that the
comment belongs to.

### extending item model

Extending the item model (part of `a4modules`) will create a new model that
belongs to a module and therefore to a specific project. This is usually the
best option if the user should create new content within a project. Examples are
ideas, documents.

Advantages:

-   possible to query all items of a project or module
-   normal foreign key relation (easier to query and database tracks
    constraints)

An item might be composed of various smaller parts. An example is the document
which consists of paragraphs. In that case only a container for the parts
should be an item (eg. document containing paragraphs), but all parts should
still implement the `project` property.

Open questions:

-   Do we need the item class at all? Wouldn't a foreign key to a module
    be enough for all use cases?

    -   benefit: one table less
    -   down side: mixed list of different item types are harder

-   Should we change the implementation so that all user-generated content is
    an item?

    -   parts of bigger items could have `is_part_of` reference (eg. paragraph)
    -   attachments of items could have `related_to` reference (eg. rating,
        comment)
    -   benefit: no generic foreign keys, project context is always given
    -   down sides: giant item table

### using generic foreign keys

A model can have a generic key, which allows it to attach to every django
model. This is usually the best option when a user does something in relation
to existing user generated content. An example is rating of existing ideas.

Advantages:

-   reusable for many different apps

Disadvantages:

-   no relation to a module
    -   requires more work to get phase dependent permissions
    -   usually permissions handled via special permissions of the target item
-   no relation to a project, but implicit through membership of the target
    item
    -   list views/APIs still require this to be explicit for private projects
-   needs signals to be deleted if target is deleted

Open questions:

-   Should we require an additional foreign key to the project, so it can be
    used for list views and permissions?
