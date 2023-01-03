import cookie from 'js-cookie'

export function updateItem (data, url, method) {
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'X-CSRFToken': cookie.get('csrftoken')
    },
    method,
    body: JSON.stringify(data)
  }
  )
}

// toLocaleDate returns a formatted and internationalized
// date string. Fallback formatting is the German variant.
// input: 2021-11-11T15:37:19.490201+01:00
// output: 11. November 2021 (depending on locale)
export const toLocaleDate = (
  isodate,
  locale = 'de-DE',
  formatStyle = { dateStyle: 'long' }
) => {
  const date = new Date(isodate)
  return new Intl.DateTimeFormat(locale, formatStyle).format(date)
}
