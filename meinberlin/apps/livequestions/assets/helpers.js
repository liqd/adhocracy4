import cookie from 'js-cookie'

export function updateItem (data, url, method) {
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'X-CSRFToken': cookie.get('csrftoken')
    },
    method: method,
    body: JSON.stringify(data)
  }
  )
}
