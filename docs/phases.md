# Phases #

## Original design ##

  **Definition:** A phase is fixed time interval inside the linear time line of
  a particpation project. It enables participants to interact in certain
  way with the participation projects content.

  **Details:**
  - each app defines phases (eg ideas/phases.py)
  - each phase belongs to a module (indirectly to a project)
  - each module only has phases from one app
  - each phase has a initiator configruable start and end date
      - phases are active if start date <= now < end date
      - never two phases active in the same project
      - optional as long as project is in draft
  - if active is phases:
    - provides a view for (all?) module content
    - sets permissions for creation/modification of content
  - all phases from an app have a developer defined order
    - eg ideas app =>  "create ideas" before "rate ideas" before "rate and comment ideas"
  - phase provide a initiator configruable name and description

  **Use cases:**
    - an initiator can create a project by combining any arbitrary phases
       - only have to obey some rules (dates and order given)

  **Left for later**:
    - deal with multiple modules inside the same project

## Current implementation ##

Below are listed the differences of what is currently implemented in a4 and opin:

  **Details:**
  - abstract concept phase is split into phase type and phase
  - phase type is inconsitently called phase content or phase identifier sometimes
    - its yves` fault
  - phase type defines:
      - permissions
      - view to use
  - phase contains:
      - start and end dates
      - description and title
      - module refrence
      - phase-type refrence
      - weight
  - phase are ordered by weight
      - given by blueprint
      - developer defined phase order doesn't really exist anymore
  - no checking of start and end dates between phases (if set or overlap)
  - view of phase displayed from start date to start_date of next phase / or indefnitly
  - permissions are only set for participants
    - moderators and intiators can always do everything

  **Use cases**:
     - an initiator can select a blueprint
        - blueprints define which phase combinations are possible
     - an initiator can add an offline phase before/after each phase (only OPIN)

## (Upcomming) challenges ##

Below this line only opinions no facts:

  - result phase for all modules/projects
    - should be mandatory
    - ideas from product vision worshop
       - implement not as phase
       - use result tab
       - extend project to store release date of results
       - integration into timeline

  - jump to content of previous phase
    - needed because offline phases (OPIN only) hide the module content
    - transition generic offline phases to events
      - events still visible in timeline
    - only module specific offline phases

  - hide features if not usable in a module
    - eg project doesn't has rate phase => no rate buttons
    - possible for comments and rate
       - because phases contain information wether this is allowed
       - implementation started by Alexej

  - introduce a new dynamic way for initators to combine phases
    - possibility to create custom blueprints
    - two step process
    - should support multiple modules, if implemented (see below)

  - unclear concept for multiple modules
    - all modules need accessiable from project detail view
    - modules should be integrated in the timeline
    - probably multiple active modules at the same time
    - very complex ui/ux issue
