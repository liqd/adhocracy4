import React from 'react'

export const CharCounter = (props) => {
  const current = props.value.length

  return (
    <span>{current}/{props.max}</span>
  )
}
