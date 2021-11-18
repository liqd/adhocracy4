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

export const toDate = (isodate) => {
  const d = new Date(isodate)
  return `${d.getDate()}. ${months[d.getMonth()]} ${d.getFullYear()}`
}

export const intComma = (number) => {
  return Number(number).toLocaleString()
}
