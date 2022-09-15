import React, { useEffect, useState } from 'react'
import django from 'django'

export const ControlBarSearch = (props) => {
  const translated = {
    startSearch: django.gettext('Start search'),
    searchFor: django.gettext('Search for Proposals')
  }

  const [value, setValue] = useState(props.term)

  const handleSubmit = (e) => {
    e.preventDefault()
    props.onSearch(value)
  }

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  useEffect(() => {
    setValue(props.term)
  }, [props.term])

  return (
    <form
      onSubmit={handleSubmit}
      className="input-group"
    >
      <label
        htmlFor="id-filter-search"
        className="visually-hidden"
      >
        {translated.searchFor}
      </label>
      <input
        className="form-control"
        type="search"
        id="id-filter-search"
        placeholder={translated.searchFor}
        onChange={handleChange}
        value={value}
      />
      <div className="input-group-append">
        <button
          className="btn btn--light btn--attached-right"
          type="submit"
        >
          <i className="fa fa-search" aria-hidden="true" />
          <span className="visually-hidden">
            {translated.startSearch}
          </span>
        </button>
      </div>
    </form>
  )
}
