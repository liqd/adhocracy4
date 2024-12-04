import React from 'react'
import django from 'django'
import { PaginationButton } from './PaginationButton'
import { useSearchParams } from 'react-router'

const pageNavigationStr = django.gettext('Page navigation')
const pageNextStr = django.gettext('next page')
const pagePrevStr = django.gettext('prev page')

export const Pagination = (props) => {
  const {
    elidedRange,
    nextPage,
    prevPage
  } = props
  const [queryParams, setQueryParams] = useSearchParams()
  const currPage = parseInt(queryParams.get('page')) || 1

  const onPaginate = (pageIndex) => {
    queryParams.set('page', pageIndex)
    setQueryParams(queryParams)
  }

  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination btn-group">
        <PaginationButton
          type="prev"
          key="pagination-item-prev"
          pageIndex={currPage - 1}
          isDisabled={!prevPage}
          ariaLabel={pagePrevStr}
          onClick={onPaginate}
        />

        {elidedRange.map((num, idx) => (
          <PaginationButton
            type="num"
            key={'pagination-item-' + idx}
            isActive={num === currPage}
            pageIndex={num}
            onClick={onPaginate}
            isNoButton={num === '…'}
          />
        ))}

        <PaginationButton
          type="next"
          key="pagination-item-next"
          pageIndex={currPage + 1}
          isDisabled={!nextPage}
          ariaLabel={pageNextStr}
          onClick={onPaginate}
        />
      </ul>
    </nav>
  )
}
