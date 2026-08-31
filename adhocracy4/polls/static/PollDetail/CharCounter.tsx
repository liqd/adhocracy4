import React from 'react'
import django from 'django'

const translated = {
  characters: django.gettext('characters')
}

interface CharCounterProps {
  value: string
  max: number
  id?: string
}

export const CharCounter = ({ value, max, id }: CharCounterProps) => {
  const current = value.length

  return (
    <span className="a4-char-counter" id={id}>
      {current}/{max} {translated.characters}
    </span>
  )
}
