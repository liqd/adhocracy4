
const shortFormat = { day: '2-digit', month: '2-digit', year: 'numeric', hour: 'numeric', minute: 'numeric' }
const longFormat = { day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric' }

// localeDate returns a formatted and internationalized
// date string.
//
// input: 2021-11-11T15:37:19.490201+01:00
// output: 11. November 2021, 10:37 (depending on locale)
// output (if not valid locale): 11.11.2021
export const localeDate = (isodate, locale = 'de-DE') => {
  const date = new Date(isodate)
  const formatStyle = _validateLocaleSupport(locale).length > 0
    ? longFormat
    : shortFormat
  return new Intl.DateTimeFormat(locale, formatStyle).format(date)
}

const _validateLocaleSupport = (locale) => {
  const options = { localeMatcher: 'lookup' }
  return Intl.DateTimeFormat.supportedLocalesOf(locale, options)
}
