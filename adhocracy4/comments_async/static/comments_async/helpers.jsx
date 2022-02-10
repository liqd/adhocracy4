export function localeDate (dateStr) {
  const options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' }
  return new Date(dateStr).toLocaleString(document.documentElement.lang, options)
}
