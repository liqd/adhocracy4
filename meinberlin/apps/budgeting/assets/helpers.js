import django from 'django'

const months = [
  django.gettext('January'),
  django.gettext('February'),
  django.gettext('March'),
  django.gettext('April'),
  django.gettext('May'),
  django.gettext('June'),
  django.gettext('July'),
  django.gettext('August'),
  django.gettext('September'),
  django.gettext('October'),
  django.gettext('November'),
  django.gettext('December')
]

// toDate returns a formatted date string
// input: 2021-11-11T15:37:19.490201+01:00
// output: 11. November 2021
export const toDate = (isodate) => {
  const d = new Date(isodate)
  return `${d.getDate()}. ${months[d.getMonth()]} ${d.getFullYear()}`
}

// intComma returns a number separated by
// a comma or period depending on the locale
// input: 20000
// output: 20.000 or 20,000
export const intComma = (number) => {
  return Number(number).toLocaleString()
}

// wrapSpaces returns the given value
// wrapped by a space before and after
// input: "0"
// output: " 0 "
export const wrapSpaces = (value) => {
  return ` ${value} `
}
