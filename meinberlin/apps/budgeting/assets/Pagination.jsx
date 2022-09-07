import React from 'react'
import django from 'django'
import { PaginationButton } from './Paginationbutton'

const pageNavigationStr = django.gettext('Page navigation')
const pageNextStr = django.gettext('next page')
const pagePrevStr = django.gettext('prev page')

export const Pagination = (props) => {
  const {
    currentIndex,
    prevPage,
    nextPage,
    pageCount,
    onPaginate
  } = props

  // Creating an Array from single digit, example: 5 = [0,1,2,3,4]
  // and map to start by 1
  const pages = [...Array(pageCount).keys()].map(n => n + 1)

  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination btn-group">
        <PaginationButton
          type="prev"
          key="page-prev"
          pageIndex={currentIndex - 1}
          isDisabled={!prevPage}
          ariaLabel={pagePrevStr}
          onClick={onPaginate}
        />

        {pages.map(num => (
          <PaginationButton
            type="num"
            key={`page-${num}`}
            isActive={num === currentIndex}
            pageIndex={num}
            onClick={onPaginate}
          />
        ))}

        <PaginationButton
          type="next"
          key="page-next"
          pageIndex={currentIndex + 1}
          isDisabled={!nextPage}
          ariaLabel={pageNextStr}
          onClick={onPaginate}
        />
      </ul>
    </nav>
  )
}
