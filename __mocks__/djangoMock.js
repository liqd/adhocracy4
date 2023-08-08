module.exports = {
  gettext: (text) => text,
  pgettext: (context, text) => text,
  ngettext: (number, text) => text + number,
  interpolate: (fmt, data) => fmt
}
