import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import { Pagination } from '../Pagination'

test('clicking on page 2 returns value of 2', () => {
  const onPageChangedFn = jest.fn()
  render(
    <Pagination
      currPageIndex={1}
      pageCount={3}
      onPaginate={selPage => onPageChangedFn(selPage)}
    />
  )
  const pageButton2 = screen.getByText('2')
  fireEvent.click(pageButton2)
  expect(onPageChangedFn).toHaveBeenCalledWith(2)
})
