import React from 'react'
import django from 'django'

const pageNavigationStr = django.gettext('Page navigation')

export const Pagination = (props) => {
  const {
    currPageIndex,
    pageCount
  } = props

  // Creating an Array from single digit, example: 5 = [0,1,2,3,4]
  // and map to start by 1
  const pages = [...Array(pageCount).keys()].map(n => n + 1)

  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination">
        {pages.map(num => (
          <li
            key={`page-${num}`}
            className={
              num === currPageIndex
                ? 'pagination-item active'
                : 'pagination-item'
              }
          >
            <button onClick={() => props.onPaginate(num)}>
              {num}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  )
}
