import React from 'react'
import django from 'django'
import { useSearchParams } from 'react-router'

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
          className="btn switch--btn btn--icon active"
          aria-label={django.gettext('View as list')}
        >
          <i className="fa fa-list" aria-hidden="true" />
          {django.gettext('List')}
        </div>
        <button
          className="btn btn--light btn--icon"
          onClick={handleClick}
          aria-label={django.gettext('View as map')}
        >
          <i className="fa fa-map" aria-hidden="true" />
          {django.gettext('Map')}
        </button>
      </div>
    </div>
  )
}
