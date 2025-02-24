# Common Errors

## Javascript

### Error when writing tests for components in a project importing adhocracy4

When writing tests with Jest (and/or testing-libray) in a project which uses adhocracy4 and the component being
tested imports a newly developed component from adhocracy4 you might encounter the following
issue:

```
Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: undefined.
```

One possible cause is that you used `npm link` to link to your local a4.
If you get the above error try deleting your `node_modules`
folder (e.g. by running `make clean`) and then properly install a4 via `npm
install liqd/adhocracy4#<name of your branch or tag>` (assuming you already
pushed your changes in a4, otherwise create a branch).
It doesn't seem to be enough to install it from a local folder via `npm install <path to a4>` for some reason.
