import React from 'react'

export const FilterCategory = ({
  translated,
  filter,
  filterDisplay,
  onClickFilter,
  commentCategoryChoices
}) => {
  return (
    <div className="a4-comments__filters__dropdown me-sm-2">
      <div className="dropdown">
        <button
          className="btn btn--select dropdown-toggle a4-comments__filters__btn"
          type="button"
          id="categoryDropdownBtn"
          data-bs-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <span className={filter === 'all' ? 'a4-comments__filters__btn-text' : 'd-none'}>{translated.display}{filterDisplay}</span>
          <span className={filter !== 'all' ? 'a4-comments__filters__btn-text small-screen' : 'd-none'}>{filterDisplay}</span>

          <i className={filter === 'all' ? 'fa fa-caret-down' : 'fas fa-check'} aria-hidden="true" />
        </button>
        <div className="dropdown-menu dropend" aria-labelledby="categoryDropdownBtn">
          {filter !== 'all' &&
            <button className="dropdown-item" onClick={onClickFilter} id="all" key="all" href="#">
              {translated.all}
            </button>}
          {Object.keys(commentCategoryChoices).map(objectKey => {
            const name = commentCategoryChoices[objectKey]
            return (objectKey !== filter) &&
              <button className="dropdown-item" onClick={onClickFilter} id={objectKey} key={objectKey} href="#">{name}</button>
          })}
        </div>
      </div>
    </div> // eslint-disable-line react/jsx-closing-tag-location
  )
}
