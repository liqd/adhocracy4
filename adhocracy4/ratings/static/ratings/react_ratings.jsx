import React from 'react'
import { createRoot } from 'react-dom/client'
import RatingBox from './RatingBox'

module.exports.renderRatings = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))

  const root = createRoot(el)
  root.render(<RatingBox {...props} />)
}
