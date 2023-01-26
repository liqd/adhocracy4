#!/bin/bash

VIRTUAL_ENV=venv
if [ ! -f $VIRTUAL_ENV/bin/python3 ]
then
    printf "no virtual env, did you run make install?";
else
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4administrative_districts > fixtures/administrative_districts.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4categories > fixtures/categories.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4labels > fixtures/labels.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4maps > fixtures/maps.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4modules > fixtures/modules.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4phases > fixtures/phases.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4polls > fixtures/polls.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata a4projects > fixtures/projects.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata account > fixtures/accounts.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_documents > fixtures/documents.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_livequestions > fixtures/live_questions.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_maps > fixtures/mb_maps.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_maptopicprio > fixtures/maptopicprop.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_moderationtasks > fixtures/moderationtasks.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_organisations > fixtures/organisations.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_topicprio > fixtures/topicprio.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_users > fixtures/users.json
    $VIRTUAL_ENV/bin/python3 manage.py dumpdata meinberlin_votes > fixtures/votes.json
fi
