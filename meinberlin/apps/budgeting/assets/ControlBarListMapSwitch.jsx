import React from 'react'
import django from 'django'
import { SpacedSpan } from './SpacedSpan'
import { useSearchParams } from 'react-router-dom'

export const ControlBarListMapSwitch = () => {
  // FIXME: to be changed, once Map is in React

  const [queryParams, setQueryParams] = useSearchParams()

  const handleClick = () => {
    queryParams.set('mode', 'map')
    setQueryParams(queryParams)
    location.reload()
  }

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
        <button
          className="btn btn--light"
          onClick={handleClick}
          aria-label={django.gettext('View as map')}
        >
          <i className="fa fa-map" aria-hidden="true" />
          <SpacedSpan>{django.gettext('Map')}</SpacedSpan>
        </button>
      </div>
    </div>
  )
}
