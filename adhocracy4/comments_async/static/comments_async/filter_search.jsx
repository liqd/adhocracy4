import React from 'react'

export const FilterSearch = ({
  translated,
  search,
  onEnterSearch,
  onClickResult,
  onClickSearch
}) => {
  return (
    <div className="a4-comments__filters__search">
      <input
        className="form-control a4-comments__filters__search-input mb-0"
        type="search"
        id="search-input"
        onKeyPress={onEnterSearch}
        placeholder={translated.searchContrib}
      />

      <button
        className={search !== '' ? 'a4-comments__filters__search-result text-muted' : 'd-none'}
        type="button"
        onClick={onClickResult}
      >
        <span className="fa-stack fa-2x">
          <i className="far fa-circle fa-stack-2x" />
          <i className="fas fa-times fa-stack-1x" aria-label={translated.clearSearch} />
        </span>
      </button>

      <button
        className="input-group-append a4-comments__filters__search-btn btn btn--transparent"
        type="button"
        onClick={onClickSearch}
      >
        <i className="fas fa-search" aria-label={translated.searchContrib} />
      </button>
    </div>
  )
}
