import React from 'react'

export const FilterSort = ({
  translated,
  sort,
  sorts,
  onClickSorted
}) => {
  return (
    <div className="a4-comments__filters__dropdown">
      <div className="dropdown">
        <button
          className="btn btn--select dropdown-toggle a4-comments__filters__btn"
          type="button"
          id="sortDropdownBtn"
          data-bs-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <span className={sort === 'new' ? 'a4-comments__filters__btn-text' : 'd-none'}>{translated.sortedBy}{sorts[sort]}</span>
          <span className={sort !== 'new' ? 'a4-comments__filters__btn-text small-screen' : 'd-none'}>{sorts[sort]}</span>
          <i className={sort === 'new' ? 'fa fa-caret-down' : 'fas fa-check'} aria-hidden="true" />
        </button>
        <div className="dropdown-menu dropdown-menu-end" aria-labelledby="sortDropdownBtn">
          {Object.keys(sorts).map(objectKey => {
            const name = sorts[objectKey]
            return (objectKey !== sort) &&
              <button
                className="dropdown-item" onClick={onClickSorted} id={objectKey}
                key={objectKey} href="#"
              >{name}
              </button>
          })}
        </div>
      </div>
    </div>
  )
}
