import React from 'react'
import django from 'django'

const translated = {
  characters: django.gettext('characters')
}

export const CharCounter = ({ value, max, id }) => {
  const current = value.length

  return (
    <span className="a4-char-counter" id={id}>
      {current}/{max} {translated.characters}
    </span>
  )
}
