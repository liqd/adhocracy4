import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { FollowButton } from '../FollowButton'
import api from '../../../../static/api'

// mock api and config, as they rely on network and browser
jest.mock('../../../../static/config')
jest.mock('../../../../static/api')

afterEach(() => {
  jest.clearAllMocks()
})

test('Test render FollowButton not following', async () => {
  api.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" />)
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  const followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  expect(api.follow.get).toHaveBeenCalledTimes(1)
})

test('Test render FollowButton following', async () => {
  api.follow.setFollowing({ enabled: true })
  render(<FollowButton authenticatedAs project="test" />)
  const followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()
  const followButton = screen.queryByText('Follow')
  expect(followButton).toBeNull()
  expect(api.follow.get).toHaveBeenCalledTimes(1)
})

test('Test render FollowButton click follow', async () => {
  api.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" />)
  let followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  let followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  fireEvent.click(followButton)
  followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()
  followButton = screen.queryByText('Follow')
  expect(followButton).toBeNull()
  expect(api.follow.change).toHaveBeenCalledTimes(1)
  expect(api.follow.get).toHaveBeenCalledTimes(1)
})

test('Test FollowButton redirect', async () => {
  // testing the redirect doesn't work and will throw an exception
  // as we are not in a browser.
  // workaround: delete location and simply check if href is set
  // to "correct" url
  delete window.location
  window.location = {}
  api.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs={null} project="test" />)
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  const followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  fireEvent.click(followButton)
  expect(window.location.href).toBe('/mock-url')
  expect(api.follow.change).not.toHaveBeenCalled()
  expect(api.follow.get).not.toHaveBeenCalled()
})

test('Test AlertPortal with target that does not exist', async () => {
  api.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" alertTarget="non-existent-id" />)
  const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  fireEvent.click(followButton)
  expect(consoleErrorSpy).toHaveBeenCalledWith(
    'AlertPortal: Target element with ID "non-existent-id" not found in DOM'
  )
  consoleErrorSpy.mockRestore()
})

test('Test AlertPortal renders correctly with existing target', async () => {
  api.follow.setFollowing({ enabled: false })
  const alertContainer = document.createElement('div')
  alertContainer.id = 'alert-container'
  document.body.appendChild(alertContainer)
  render(<FollowButton authenticatedAs project="test" alertTarget="alert-container" />)
  const followButton = await screen.findByText('Follow')
  fireEvent.click(followButton)
  const alertElement = screen.getByText('You will be updated via email.')
  expect(alertElement).toBeInTheDocument()
  document.body.removeChild(alertContainer)
})
