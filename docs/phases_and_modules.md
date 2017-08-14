# Modules and Phases

## Phases

### Definition

A phase is a fixed time interval inside the linear time line of
a participation project. It enables participants to interact in a certain
way with the participation project's content.

### Details

-   each app defines phases (eg ideas/phases.py)
-   each phase belongs to a module (indirectly to a project)
-   each module only has phases from one app
-   each phase has an initiator-configurable start and end date
    -   phases are active if start date <= now < end date
    -   only one phase in a module can be active at any point
    -   optional as long as project is in draft
-   if a phase is active:
    -   it provides a view for (all?) module content
    -   it sets permissions for creation/modification of content
-   all phases from an app have a developer-defined order
    -   eg ideas app => "create ideas" before "rate ideas" before "rate and
        comment ideas"
-   phases provide an initiator-configurable name and description

### Use cases

-   an initiator can create a project by combining any arbitrary phases
    -   only have to obey some rules (dates and order given)

### Current Implementation

-   abstract concept "phase" is split into "phase type" and "phase"
-   phase type is inconsistently called phase content or phase identifier sometimes
    -   it's yves' fault
-   phase type defines:
    -   permissions
    -   view to use
-   phase contains:
    -   start and end dates
    -   description and title
    -   module reference
    -   phase-type reference
    -   weight
-   phases are ordered by weight
    -   given by blueprint
    -   developer defined phase order doesn't really exist anymore
-   no checking of start and end dates between phases (if set or overlap)
-   view of phase displayed from start date to start date of next phase / or indefinitely
-   permissions are only set for participants
    -   moderators and initiators can always do everything


## Modules

### Definition

A module is a container of multiple phases of a single app. A module is called
active when one of its phases is active. Within a project context multiple
modules may overlap.

### Details

-   each module belongs to a project
-   each module only has phases from one app
-   modules have a developer-defined order called weight
-   a project defines a "last active" module as
    -   the module of the last active phase
    -   the last active phase is defined as the last starting phase out of all past
        and currently active phases

### Use cases

-   an initiator can select a blueprint
    -   blueprints define which module and phase combinations are possible
-   an initiator can add an offline phase before/after each phase (only OPIN)


## (Upcoming) challenges

Below this line only opinions no facts:

-   jump to content of previous phase
    -   needed because offline phases (OPIN only) hide the module content
    -   transition generic offline phases to events
        -   events still visible in timeline
    -   only module specific offline phases

-   introduce a new dynamic way for initiators to combine phases
    -   possibility to create custom blueprints
    -   two step process
    -   should support multiple modules, if implemented (see below)
