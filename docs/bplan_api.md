# BPLAN Project API

mein.berlin provides an external REST API to create and manage BPLAN projects.

## Background

Bplans define binding regulations for urban planning, specifying land
use (e.g. housing, offices, green spaces) and building parameters like height
and footprint. Citizens can participate in the process and provide feedback
on the plans. As the central participation platform of the city of Berlin, we want
to show all Bplans which allow participation in our project overview. Up until the beginning of 2025
meinBerlin also provides the means for the digital participation. In the future this will be provided by
the Diplan platform. Bplans are mostly created via this api but they can also be added by initiators from the dashboard.

### Integration with Imperia (legacy)

Imperia is a CMS used by the public administration and is responsible for displaying Bplans and the participation form
on berlin.de. Imperia uses this API to publish and unpublish Bplans on meinBerlin depending on whether participation is
currently possible. When creating or publishing a Bplan, the meinBerlin API returns an embed code (iframe) which then is
embedded in the Bplan page on berlin.de to allow citizen to submit their feedback. Imperia only provides basic
information about the Bplan to meinBerlin, therefore meinBerlin will fetch the location and the district from the
Bplan map.

### Integration with Diplan

Diplan will replace Imperia for managing Bplans and also incorporate the participation feature currently done via the
embed
from meinBerlin. Therefore, the only remaining functionality in meinBerlin is to display them in the project overview
and link to Diplan.

#### Notable changes compared to the old system:

- The district can be calculated from the Bplan identifier, we no longer need to fetch it from the Bplan map
- The Bplan Location is provided by Diplan, we no longer need to fetch it from the Bplan map
- The statement form / embed code for the participation is no longer required as participation happens directly on
  Diplan
- Bplans will be shown unless unpublished via this api, previously they would automatically be archived once the
  participation phase ended

## Prerequisites

To use this API you need to have received an email and a password for the
API user and the `id` of your organisation.

The api currently supports both the legacy Imperia system and the new Diplan system. In the future
support for Imperia will be removed.

## Authentication

The API supports the HTTP Basic Authentication mechanism and requires a TLS connection to prevent
leaking the login credentials. You need the email and password combination from your user account as mentioned in the
Prerequisites above.

## Endpoints

* [Create Bplan](#Creating-a-Bplan) : `POST https://mein.berlin.de/api/organisations/<organisation-id>/bplan/`
* [Update Bplan](#Updating-a-Bplan) : `PATCH /https://mein.berlin.de/api/organisations/<organisation-id>/bplan/<bplan-id>/`

## Creating a Bplan

Create a new Bplan within the organisation designated by `organisation-id`.

**URL** : `https://mein.berlin.de/api/organisations/<organisation-id>/bplan/`

**Method** : `POST`

**Parameters** : `organisation-id`: Integer - id of the organisation the bplan will be added to

**Auth required** : YES

**Permissions required** : User account must be initiator for the specified organisation

**Data constraints**

The following fields need to be provided:

- *name*: string
  - Name of the BPLAN (e.g. used as the title of the project tile)
  - Maximum length of 120 chars
- *(imperia only) identifier*: string
  - Identifier that clearly identifies the BPLAN, needs to be the same as in the FIS Broker (e.g. `VIII - 329`)
  - Maximum length of 120 chars
- *(diplan only) bplan_id*: string
  - Id that clearly identifies the BPLAN, needs to be the same as in the FIS Broker (e.g. `VIII - 329`)
  - Maximum length of 120 chars
- *description*: string
  - Description of the BPLAN shown in the project tile
  - Maximum length of 250 chars
- *url*: string
  - URL of the external site the BPLAN is embedded on
- *office_worker_email*: string
  - Email of the office worker to receive notifications about changes
  - Imperia only: email the statements are sent to
- *is_draft*: bool
  - Whether the plan is still a draft or should be published
- *start_date*: string
  - Start date of the participation
  - [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)
    (if no time zone is defined, german time zones UTC+01 and UTC+02 are used)
- *end_date*: string
  - End date of the participation in
  - [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)
    (if no time zone is defined, german time zones UTC+01 and UTC+02 are used)
- *point*: string
  - string containing coordinates separated by a comma, e.g. "1492195.544958444,6895923.461738203"
  - Location of the bplan
  - Projection: WGS84 / EPSG:3857
- *image_url*: string
  - URL of the image that is used in the project tile
  - Minimal resolution 500x300 px (width x height)
  - Maximum file size 10MB
- *image_copyright*: string
  - Copyright shown for the image
  - Maximum length of 120 chars

#### Data example

```json
{
  "name": "Luisenblock Ost - Bebauungsplan 1-70",
  "bplan_id": "VI - 123c",
  "description": "Der Luisenblock Ost soll städtebaulich neu geordnet werden. Nutzungen des Deutschen Bundestages sollen in einem Sondergebiet als Auftakt des 'Band des Bundes' zusammengefasst werden.",
  "url": "https://berlin.de/ba-marzahn-hellersdorf/.../bebauungsplan.649020.php",
  "is_draft": false,
  "start_date": "2017-01-01T00:00",
  "end_date": "2018-01-01T00:00",
  "point": "1492195.544958444,6895923.461738203",
  "image_url": "http://berlin.de/images/.../bebauungsplan.649020.png",
  "image_copyright": "BA Marzahn-Hellersdorf"
}
```

### Success Response

**Condition** : If all data is valid

**Code** : `201 CREATED`

**Response**

- id: Integer
  - The id of the newly created bplan. Required to make modifications to this bplan.
- (imperia only): embed: string
  - Returns the embed code (iframe) for the statement form

**Content example**

```json
{
  "id": 1
}
```

### Error Responses

**Condition** : Invalid data (e.g. missing field).

**Code** : `400 Bad Request`

**Content example**

```json
{
  "name": [
    "This field is required."
  ]
}
```

## Testing

### Example for `curl`

```bash
curl \
 -X POST https://mein.berlin.de/api/organisations/5/bplan/ \
 --user 'test@example.com':'password' \
 -H "Content-Type: application/json" \
 -d \
 '
 {
   "name":"Luisenblock Ost - Bebauungsplan 1-70",
   "bplan_id": "VI - 96a",
   "description": "Test",
   "url": "https://mein.berlin.de",
   "office_worker_email": "test@example.com",
   "start_date": "2019-01-01T00:00",
   "end_date": "2022-01-01T00:00",
   "point": "1492195.544958444,6895923.461738203"
 }
'
```

### Example for `curl` and local testing

```bash
curl  -X POST http://127.0.0.1:8003/api/organisations/1/bplan/ \
 --user 'admin@liqd.net':'password' \
 -H "Content-Type: application/json" \
 -d \
 '
 {
   "name":"Luisenblock Ost - Bebauungsplan 1-70",
   "bplan_id": "VI - 96a",
   "description": "Test",
   "url": "https://mein.berlin.de",
   "office_worker_email": "test@example.com",
   "start_date": "2019-01-01T00:00",
   "end_date": "2022-01-01T00:00",
   "point": "1492195.544958444,6895923.461738203"
 }
'
```

## Updating a Bplan

Update an existing Bplan with the id `bplan-id` (attention: `bplan-id` here refers to the id which is returned from
the api after creating a new bplan, not the `bplan_id` field which is used to designate the fis-broker identifier)
within the organisation designated by`organisation-id`.

**URL** : `https://mein.berlin.de/api/organisations/<organisation-id>/bplan/<bplan-id>/`

**Method** : `PATCH`

**Parameters** :

- `organisation-id`: Integer
  - id of the organisation the bplan will be added to
- `bplan-id`: Integer
  - id of the bplan to update

**Auth required** : YES

**Permissions required** : User account must be initiator for the specified organisation

**Data constraints**

See [data example](#data-example) above

### Success Response

**Condition** : If all data is valid

**Code** : `200 OK`

**Response**

- id: Integer
  - The id of the newly created bplan. Required to make modifications to this bplan.
- (imperia only): embed: string
  - Returns the embed code (iframe) for the statement form

**Content example**

```json
{
  "id": 1
}
```

### Error Responses

**Condition** : Invalid data (e.g. missing field).

**Code** : `400 Bad Request`

**Content example**

```json
{
  "name": [
    "Not a valid string"
  ]
}
```

## Testing

### Example for `curl`

```bash
curl \
 -X PATCH https://mein.berlin.de/api/organisations/5/bplan/1 \
 --user 'test@example.com':'password' \
 -H "Content-Type: application/json" \
 -d \
'
 {
   "is_draft": true
 }
'
```

### Example for `curl` and local testing

```bash
curl  -X PATCH http://127.0.0.1:8003/api/organisations/1/bplan/16/ \
 --user 'admin@liqd.net':'password' \
 -H "Content-Type: application/json" \
 -d \
'
 {
   "is_draft": true
 }
'
```
