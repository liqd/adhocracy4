// Helper functions, used in apps/budgeting/assets

// toLocaleDate returns a formatted and internationalized
// date string. Fallback formatting is the German variant.
// input: 2021-11-11T15:37:19.490201+01:00
// output: 11. November 2021 (depending on locale)
export const toLocaleDate = (isodate, locale = 'de-DE') => {
  const date = new Date(isodate)
  const formatStyle = { dateStyle: 'long' }
  return new Intl.DateTimeFormat(locale, formatStyle).format(date)
}

// wrapSpaces returns the given value
// wrapped by a space before and after
// input: "0"
// output: " 0 "
export const wrapSpaces = (value) => {
  return ` ${value} `
}
