import React from 'react'
import { createRoot } from 'react-dom/client'
import LandingPageMapTeaser from './LandingPageMapTeaser'

module.exports.renderFilter = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(
    <React.StrictMode>
      <LandingPageMapTeaser {...props} />
    </React.StrictMode>)
}
