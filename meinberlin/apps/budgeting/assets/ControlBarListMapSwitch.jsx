import React from 'react'
import django from 'django'
import { SpacedSpan } from './SpacedSpan'

export const ControlBarListMapSwitch = ({ query }) => {
  // FIXME: to be changed, once Map is in React
  return (
    <div className="btn-group__container">
      <div className="btn-group">
        <div
          className="btn btn--light switch--btn active"
          aria-label={django.gettext('View as list')}
        >
          <i className="fa fa-list" aria-hidden="true" />
          <SpacedSpan>{django.gettext('List')}</SpacedSpan>
        </div>
        <a
          className="btn btn--light"
          href={'?mode=map' + query}
          aria-label={django.gettext('View as map')}
        >
          <i className="fa fa-map" aria-hidden="true" />
          <SpacedSpan>{django.gettext('Map')}</SpacedSpan>
        </a>
      </div>
    </div>
  )
}
