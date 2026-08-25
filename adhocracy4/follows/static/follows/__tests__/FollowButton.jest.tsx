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

const mockedApi = api as unknown as {
  follow: {
    get: jest.Mock
    change: jest.Mock
    setFollowing: (value: { enabled: boolean } | null) => void
  }
}

test('Test render FollowButton not following', async () => {
  mockedApi.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" />)
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  const followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  expect(mockedApi.follow.get).toHaveBeenCalledTimes(1)
})

test('Test render FollowButton following', async () => {
  mockedApi.follow.setFollowing({ enabled: true })
  render(<FollowButton authenticatedAs project="test" />)
  const followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()
  const followButton = screen.queryByText('Follow')
  expect(followButton).toBeNull()
  expect(mockedApi.follow.get).toHaveBeenCalledTimes(1)
})

test('Test render FollowButton click follow', async () => {
  mockedApi.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" />)
  let followButton: HTMLElement | null = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  let followingButton: HTMLElement | null = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  fireEvent.click(followButton as HTMLElement)
  followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()
  followButton = screen.queryByText('Follow')
  expect(followButton).toBeNull()
  expect(mockedApi.follow.change).toHaveBeenCalledTimes(1)
  expect(mockedApi.follow.get).toHaveBeenCalledTimes(1)
})

test('Test FollowButton redirect', async () => {
  // testing the redirect doesn't work and will throw an exception
  // as we are not in a browser.
  // workaround: delete location and simply check if href is set
  // to "correct" url
  // @ts-expect-error jsdom's window.location is not configurable
  delete window.location
  // @ts-expect-error override location with a plain object for the redirect test
  window.location = { href: '' } as Location
  mockedApi.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs={null} project="test" />)
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  const followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  fireEvent.click(followButton)
  expect(window.location.href).toBe('/mock-url')
  expect(mockedApi.follow.change).not.toHaveBeenCalled()
  expect(mockedApi.follow.get).not.toHaveBeenCalled()
})

test('Test AlertPortal with target that does not exist', async () => {
  mockedApi.follow.setFollowing({ enabled: false })
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
  mockedApi.follow.setFollowing({ enabled: false })
  const alertContainer = document.createElement('div')
  alertContainer.id = 'alert-container'
  document.body.appendChild(alertContainer)
  render(<FollowButton authenticatedAs project="test" alertTarget="alert-container" />)
  const followButton = await screen.findByText('Follow')
  fireEvent.click(followButton)
  const alertElement = screen.getByText((content, _element) => {
    return content.includes('From now on, we\'ll keep you updated on all changes') &&
           content.includes('Make sure email notifications are enabled in your') &&
           content.includes('notification settings')
  })
  expect(alertElement).toBeInTheDocument()
  document.body.removeChild(alertContainer)
})
