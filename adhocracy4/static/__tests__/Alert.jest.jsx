import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Alert from '../Alert'

test('Alert is showing', () => {
  render(<Alert type="success" message="hello" />)
  const alert = screen.getByRole('alert')
  expect(alert).toBeTruthy()
})

test('Alert is not showing', () => {
  render(<Alert message="hello" />)
  const alert = screen.queryByRole('alert')
  expect(alert).toBeFalsy()
})

test('Invoke callback through click', () => {
  const onClickCallback = jest.fn()
  render(
    <Alert
      type="success"
      message="hello"
      onClick={onClickCallback}
    />
  )
  const clickButton = document.querySelector('.alert__close')
  fireEvent.click(clickButton)
  expect(onClickCallback).toHaveBeenCalled()
})

test('Invoke callback through timer', async () => {
  const onClickCallback = jest.fn()
  render(
    <Alert
      type="success"
      message="hello"
      onClick={onClickCallback}
      timeInMs={100}
    />
  )
  // second argument could be passed, e.g. { timeout: 4000 }
  await waitFor(() => expect(onClickCallback).toHaveBeenCalledTimes(1))
})

test('Invoke callback through click before timer ends', async () => {
  const onClickCallback = jest.fn()
  render(
    <Alert
      type="success"
      message="hello"
      onClick={onClickCallback}
      timeInMs={1000}
    />
  )
  const clickButton = document.querySelector('.alert__close')
  fireEvent.click(clickButton)
  expect(onClickCallback).toHaveBeenCalledTimes(1)
  await waitFor(() => expect(onClickCallback).not.toHaveBeenCalledTimes(2))
})
