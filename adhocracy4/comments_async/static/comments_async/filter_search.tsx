import React, { useState } from 'react'
import django from 'django'

const translated = {
  searchContrib: django.gettext('Search contributions'),
  clearSearch: django.gettext('Clear search')
}

interface FilterSearchProps {
  search: string
  onSearch: (query: string) => void
  translated?: any
}

export const FilterSearch = ({
  search,
  onSearch
}: FilterSearchProps) => {
  const [query, setQuery] = useState(search)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value)
  }

  const handleSubmit = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      onSearch(query)
    }
  }

  const handleClearQuery = (_e: React.MouseEvent) => {
    setQuery('')
    onSearch('')
  }

  return (
    <div className="a4-comments__filters__search" role="search">
      <input
        className="form-control a4-comments__filters__search-input mb-0"
        type="text"
        id="search-input"
        value={query}
        onChange={handleChange}
        onKeyPress={handleSubmit}
        placeholder={translated.searchContrib}
      />

      <button
        className={query !== '' ? 'a4-comments__filters__search-result text-muted' : 'd-none'}
        type="button"
        onClick={handleClearQuery}
      >
        <span className="fa-stack fa-2x">
          <i className="far fa-circle fa-stack-2x" />
          <i className="fas fa-times fa-stack-1x" aria-label={translated.clearSearch} />
        </span>
      </button>

      <button
        className="input-group-append a4-comments__filters__search-btn btn btn--transparent"
        type="button"
        onClick={() => onSearch(query)}
      >
        <i className="fas fa-search" aria-label={translated.searchContrib} />
      </button>
    </div>
  )
}
