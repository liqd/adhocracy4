### Changelogs

Temporary folder to add new changes. Each change should go into a separate file
(unless it makes sense to group some changes into one file, e.g. a story).
During release the changes will be moved to CHANGELOG.md.

Each file should follow one of the below naming patterns:

- \<issue number>.md
  or
- \<story number>.md
  or
- \<pr number>.md
  or
- \<random number>.md if none of other apply

The content of the file should look like this:

```
### <type of change>

- description of the change in one or max two sentences (#<issue> or !<pr>)
```

< type of change > can be one of:

- **Added** for new features.
- **Changed**: for changes in existing functionality.
- **Deprecated**: for soon-to-be removed features.
- **Removed**: for now removed features.
- **Fixed**: for any bug fixes.
- **Security**: in case of vulnerabilities.


## Example

```
### Fixed

- improve userdashboard filter performance (#2449)
```

