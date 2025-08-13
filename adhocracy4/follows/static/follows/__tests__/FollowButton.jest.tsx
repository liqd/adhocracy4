import React from 'react'
import { render, fireEvent, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { vi, Mock } from 'vitest'
import { FollowButton } from '../FollowButton'
import api from '../../../../static/api'

// mock api and config, as they rely on network and browser
vi.mock('../../../../static/config')

const mockJQueryDeferred = () => {
  const deferred = {
    done: vi.fn().mockReturnThis(),
    fail: vi.fn().mockReturnThis(),
    always: vi.fn().mockReturnThis(),
    then: vi.fn().mockReturnThis(),
    promise: vi.fn().mockReturnThis(),
    state: vi.fn(),
    pipe: vi.fn().mockReturnThis()
  }
  return deferred
}

vi.mock('../../../../static/api', () => ({
  __esModule: true,
  default: {
    comments: {
      get: vi.fn(() => mockJQueryDeferred()),
      add: vi.fn(() => mockJQueryDeferred()),
      change: vi.fn(() => mockJQueryDeferred()),
      delete: vi.fn(() => mockJQueryDeferred())
    },
    follow: {
      get: vi.fn(() => mockJQueryDeferred()),
      change: vi.fn(() => mockJQueryDeferred()),
      setFollowing: vi.fn() // Add this mock
    }
  }
}))

afterEach(() => {
  vi.clearAllMocks()
})

test('Test render FollowButton not following', async () => {
  api.follow.setFollowing({ enabled: false })
  render(<FollowButton authenticatedAs project="test" alertTarget="alert-container" />)
  const followButton = await screen.findByText('Follow')
  expect(followButton).toBeTruthy()
  const followingButton = screen.queryByText('Following')
  expect(followingButton).toBeNull()
  expect(api.follow.get).toHaveBeenCalledTimes(1)
})

test('Test render FollowButton following', async () => {
  // Create a mock deferred object
  const deferred = mockJQueryDeferred();

  // Mock the follow.get method to return our deferred object
  (api.follow.get as Mock).mockReturnValueOnce(deferred);

  // Mock setFollowing if needed (though it may not be necessary for this test)
  (api.follow.setFollowing as Mock).mockImplementation(() => {})

  render(<FollowButton authenticatedAs project="test" />)

  // Simulate a successful API response with enabled: true
  deferred.done.mock.calls[0][0]({
    enabled: true
  })

  // Wait for and assert the Following button appears
  const followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()

  // Assert the Follow button is not present
  const followButton = screen.queryByText('Follow')
  expect(followButton).toBeNull()

  // Verify the API was called
  expect(api.follow.get).toHaveBeenCalledTimes(1)
  expect(api.follow.get).toHaveBeenCalledWith('test')
})

test('Test render FollowButton click follow', async () => {
  // Mock get to return not following initially
  (api.follow.get as Mock).mockImplementationOnce(() => ({
    done: (callback: (arg0: { enabled: boolean }) => void) => {
      callback({ enabled: false })
      return { fail: vi.fn() }
    }
  }));

  // Mock change to return following after click
  (api.follow.change as Mock).mockImplementationOnce(() => ({
    done: (callback: (arg0: { enabled: boolean }) => void) => {
      callback({ enabled: true })
      return { fail: vi.fn() }
    }
  }))

  render(<FollowButton authenticatedAs project="test" />)

  // Initial state
  const followButton = await screen.findByText('Follow')
  fireEvent.click(followButton)

  // Updated state
  const followingButton = await screen.findByText('Following')
  expect(followingButton).toBeTruthy()

  // Verify calls
  expect(api.follow.change).toHaveBeenCalledWith({ enabled: true }, 'test')
})

test.skip('Test FollowButton redirect', async () => {
  // testing the redirect doesn't work and will throw an exception
  // as we are not in a browser.
  // workaround: delete location and simply check if href is set
  // to "correct" url
  delete window.location
  window.location = {} as Location
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
  // Mock API responses
  const getDeferred = mockJQueryDeferred()
  const changeDeferred = mockJQueryDeferred();

  (api.follow.get as Mock).mockReturnValueOnce(getDeferred);
  (api.follow.change as Mock).mockReturnValueOnce(changeDeferred);
  (api.follow.setFollowing as Mock).mockImplementation(() => {})

  render(
    <FollowButton
      authenticatedAs
      project="test"
      alertTarget="non-existent-id"
    />
  )

  // Set up console error spy
  const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

  // Resolve initial load
  getDeferred.done.mock.calls[0][0]({ enabled: false })

  const followButton = await screen.findByText('Follow')
  fireEvent.click(followButton)

  // Resolve change call
  changeDeferred.done.mock.calls[0][0]({ enabled: true })

  await waitFor(() => {
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      'AlertPortal: Target element with ID "non-existent-id" not found in DOM'
    )
  })

  consoleErrorSpy.mockRestore()
})

test('Test AlertPortal renders correctly with existing target', async () => {
  // Mock API responses
  const getDeferred = mockJQueryDeferred()
  const changeDeferred = mockJQueryDeferred();

  (api.follow.get as Mock).mockReturnValueOnce(getDeferred);
  (api.follow.change as Mock).mockReturnValueOnce(changeDeferred);
  (api.follow.setFollowing as Mock).mockImplementation(() => {})

  // Create target container
  const alertContainer = document.createElement('div')
  alertContainer.id = 'alert-container'
  document.body.appendChild(alertContainer)

  render(
    <FollowButton
      authenticatedAs
      project="test"
      alertTarget="alert-container"
    />
  )

  // Resolve initial load
  getDeferred.done.mock.calls[0][0]({ enabled: false })

  const followButton = await screen.findByText('Follow')
  fireEvent.click(followButton)

  // Resolve change call with success
  changeDeferred.done.mock.calls[0][0]({ enabled: true })

  await waitFor(() => {
    const alertElement = screen.getByText('You will be updated via email.')
    expect(alertElement).toBeInTheDocument()
  })

  // Cleanup
  document.body.removeChild(alertContainer)
})
