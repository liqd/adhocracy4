import React from 'react'
import { createRoot } from 'react-dom/client'
import RatingBox from './RatingBox'

export const renderRatings = function (el: HTMLElement) {
  const props = JSON.parse(el.getAttribute('data-attributes') as string)

  const root = createRoot(el)
  root.render(<RatingBox {...props} />)
}

export default {
  renderRatings
}
