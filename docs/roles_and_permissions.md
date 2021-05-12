# Roles and permissions

To handle the complexity of having different permissions for
different roles in our participation projects, we use the
[django-rules package](https://github.com/dfunckt/django-rules).

## Roles
We make use of the follwing roles in adhocracy4. The different
projects make use of these, but might have defined more roles.

#### Admin
The admin or superuser role comes with the django's authentification
system.
#### Initiator
Initiators are added to organisations and can add and change projects.
#### Moderator
Moderators are addde to the project and can only view and moderate these. In some projects, they are also allowed to change existing projects, but to achieve this, the rules defined in a4 are overwritten in the project.
#### Members
Organisation members can take part in any project of an organisation, even when the project is private (not public). The members are added as extra model, which connects a user to an organisation. Currently these are only used in [adhocracy-plus](https://github.com/liqd/adhocracy-plus).
#### Participants
If a project is private (not public), only participants (and organisation members) can take part. The participants are added to the project.
#### User
Any logged-in user.
#### Anonymous
This isn't a real role, but the logged-out user.
#### Permisions table
|  Role | public projects <br /> read/write | semi-public projects <br /> read/write  | private projects <br /> read/write  |
| :------------: | :------------: | :------------: | :------------: |
| **Admin**  | y/y  | y/y  | y/y  |
|  **Initiator** <br />  (organisation)  | y/y  | y/y  | y/y  |
|  **Member** *  <br />  (organisation)| y/y  | y/y  | y/y  |
| **Moderator**  <br />  (project) | y/y  | y/y  | y/y  |
| **Contributor** <br />  (organisation) | y/y  | y/n  | n/n  |
| **Group Member** \** <br />  (organisation/project) | y/y  | y/y  | y/y  |
|  **Participant** * | y/y  | y/y  | y/y  |
|  **User** | y/y | y/n  | n/n  |

\* must also be a contributor to be allowed to take part <br />
\** only on mB: subgroup of initiators, only allowed to add projects and to work on projects belonging to the same group, not allwed to work on all projects of organisation


## Permissions
The apps that define the roles normally also define permissions.

As described in [phases and modules](./phases_and_modules.md), the rules define what the user (or participant) can do before, during and after the phases.
