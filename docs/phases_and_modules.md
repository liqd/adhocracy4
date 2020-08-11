# Modules and Phases

## Phases

### Definition

A phase is a fixed time interval inside the linear time line of
a participation module. It enables participants to interact in a certain
way with the participation module's content.

### Details

-   each app defines phases (eg ideas/phases.py)
-   each phase belongs to a module (and indirectly to a project)
-   each module only has phases from one app
-   each phase has an initiator-configurable start and end date
    -   phases are active if start date <= now < end date
    -   only one phase in a module can be active at any point
-   if a phase is active:
    -   it provides a view for all content in that module phase
    -   it sets permissions for creation/modification of content
-   all phases from an app have a developer-defined order
    -   eg ideas app => "create ideas" before "rate ideas" before "rate and
        comment ideas"
-   phases provide an initiator-configurable name and description

### Use cases

-   an initiator can choose a module with a preconfigured set of phases and has
    to set the times of the phases
    -   only have to obey some rules (dates and order given)

### Current Implementation

-   abstract concept "phase" is split into "phase type" and "phase"
-   phase type is sometimes called phase content or phase identifier
-   phase type (or content) defines:
    -   permissions
    -   view to use
-   phase contains:
    -   start and end dates
    -   description and title
    -   module reference
    -   phase-type reference
    -   weight
-   phases are ordered by weight
    -   weights are usually initialised from the position of the phase type in
        the blueprint.
-   no checking of start and end dates between phases (if overlap)
-   view of phase displayed from start date to start date of next phase / or
    indefinitely?
-   view of phase displayed from start date to end date
-   permissions are only set for participants
    - moderators and initiators can always do everything on item-level

### Current Implementation of Active, Past and Future Phases

The states of the phases are implemented a bit differently in the different places (in the PhasesQuerySet and as properties of the Module and the Project model).

#### PhasesQuerySet
-   active_phases:
    -   start date <= now < end date
    -   ordered by weight (default from model)
-   finished_phases:
    -   end date <= now
    -   ordered by weight (default from model)
-   past_phases:
    -   end date <= now
    -   ordered by start
-   future_phases:
    -   start date > now or start date == None
    -   ordered by start
-   past_and_active_phases:
    -   start date <= now < end date
    -   ordered by start
-   finish_next:
    -   start date <= now < end date
    -   end date within next 24 hours
-   start_last:
    -   start date < now
    -   started within last hour

#### Phase (model) properties
-   is_over
    -   returns True when no end_date is set (contrary to future_phases with also contains the phases without end_date)
    -   returns True is end date is past
-   is_first_of_project (function, not a property)
    -   is meant to return if it is the first phase of the project
    -   as the order is not defined when multiple modules exist, this shouldn't be used

#### Module (model) properties
-   future_phases and past_phases use PhasesQuerySet
    -   both ordered by start date
-   active_phase
    - active_phases.first()
    - ordered by weight
    - there should only be one active phase in the module though
-   last_active_phase
    - either active_phase or past_phases.last (the past phase the started last)

#### Project (model) properties
-   future_phases and past_phases use PhasesQuerySet
    -   both ordered by start date
-   last_active_phase
    -   past_and_active_phases.last
    -   the phase that started last
-   active phase
    -   last_active_phase if end date <= now
-   active_phase_ends_next
    -   active_phases.order_by('end_date').first
    -   phase that ends next
-   days_left are days left of active phase
-   time_left is time left of active_phase_ends_next
-   active_phase_progress id percent over of active_phase_ends_next
-   has_started is True if past_and_active_phase exists
-   has_finished is True if neither active_phases nor future_phases exist

#### Things to keep in mind or fix
-   finished_phases and past_phases are different by their order
-   phases without dates are future phases, but is_over returns True if no end_date is set
-   past_and_active_phases are ordered by start date (while active_phases are ordered by weight)
-   finish_next has all phases ending within 24 hours, not the next one to finish
-   start_last has all phases that started in the last hour, not the last one to start
-   is_first_of_project will only work for single modules
-   active_phase from module and project are taken from QS with different orderings (weight for module, start date for project)

## Modules

### Definition

A module is a container of multiple phases of a single app. A module is called
active when one of its phases is active. Within a project context multiple
modules may overlap or run simultaneously this is called a multi module project.

### Details

-   each module belongs to a project
-   each module only has phases from one app
-   modules are ordered by weight per default
-   if a project has more than one module, the modules are either clustered if they are overlapping or ordered by module start
-   a project defines a "last active" module as
    -   the module of the last active phase
    -   the last active phase is defined as the last starting phase out of all past
        and currently active phases

### Use cases

-   an initiator can select a blueprint in the dashboard
    -   blueprints define which module and phase combinations are possible
-   an initiator can add multiple offline events

## (Upcoming) challenges

Below this line only opinions no facts:

-   jump to content of previous phase
    -   needed because offline phases (OPIN only) hide the module content
    -   transition generic offline phases to events
        -   events still visible in timeline
    -   only module specific offline phases?

-   ~~introduce a new dynamic way for initiators to combine phases~~
    -   ~~possibility to create custom blueprints~~
    -   ~~two step process~~
    -   ~~should support multiple modules, if implemented (see below)~~
