import React from 'react'
import django from 'django'
import { PaginationButton } from './PaginationButton'

const pageNavigationStr = django.gettext('Page navigation')
const pageNextStr = django.gettext('next page')
const pagePrevStr = django.gettext('prev page')

export const Pagination = (props) => {
  const {
    currentPage,
    elidedRange,
    nextPage,
    onPaginate,
    prevPage
  } = props

  const getKeyStr = (num, idx) => {
    return `page-${typeof num !== 'number' ? `ellip-${idx}` : num}`
  }

  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination btn-group">
        <PaginationButton
          type="prev"
          key="page-prev"
          pageIndex={currentPage - 1}
          isDisabled={!prevPage}
          ariaLabel={pagePrevStr}
          onClick={onPaginate}
        />

        {elidedRange.map((num, idx) => (
          <PaginationButton
            type="num"
            key={getKeyStr(num, idx)}
            isActive={num === currentPage}
            pageIndex={num}
            onClick={onPaginate}
            isDisabled={num === '…'}
          />
        ))}

        <PaginationButton
          type="next"
          key="page-next"
          pageIndex={currentPage + 1}
          isDisabled={!nextPage}
          ariaLabel={pageNextStr}
          onClick={onPaginate}
        />
      </ul>
    </nav>
  )
}
