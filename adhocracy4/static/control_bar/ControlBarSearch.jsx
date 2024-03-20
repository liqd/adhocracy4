import React, { useEffect, useState } from 'react'
import django from 'django'

const translated = {
  search: django.gettext('Search'),
  startSearch: django.gettext('Start search')
}

export const ControlBarSearch = ({ onSearch, term, placeholder }) => {
  const [value, setValue] = useState(term)
  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(value)
  }

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  useEffect(() => {
    setValue(term)
  }, [term])

  return (
    <form onSubmit={handleSubmit} className="a4-control-bar__search__form">
      <div className="form-group">
        <label htmlFor="searchterm" className="form-label">
          {translated.search}
        </label>
        <div className="a4-control-bar__search__term">
          <div className="input-wrapper">
            <i className="a4-control-bar__search__logo-start" aria-hidden="true" />
            <input
              type="search"
              className="form-control a4-control-bar__search__input"
              placeholder={placeholder || ''}
              value={value}
              id="searchterm"
              onChange={handleChange}
            />
          </div>
          <button className="a4-control-bar__search__input-submit" type="submit" title={translated.startSearch}>
            <span className="a4-sr-only">{translated.startSearch}</span>
            <i className="a4-control-bar__search__logo-end" aria-hidden="true" />
          </button>
        </div>
      </div>
    </form>
  )
}
