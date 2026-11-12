import React from 'react'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

let mockPollData = null
let mockSavedData = null
let mockChangeResponse = { questions: [] }
let mockChangeFails = false
let mockChangePending = false
let mockLastChangeDeferred = null

const mockMakeDeferred = (result, fails, failArg, pending = false) => {
  let doneCallback = null
  let failCallback = null
  return {
    done (cb) {
      doneCallback = cb
      if (!pending && !fails) cb(result)
      return this
    },
    fail (cb) {
      failCallback = cb
      if (!pending && fails) cb(failArg)
      return this
    },
    resolve (data) {
      if (doneCallback) doneCallback(data)
    },
    reject (arg) {
      if (failCallback) failCallback(arg)
    }
  }
}

jest.mock('../../../static/api', () => ({
  __esModule: true,
  default: {
    poll: {
      get: jest.fn(() => mockMakeDeferred(mockPollData, false)),
      change: jest.fn(() => {
        mockLastChangeDeferred = mockMakeDeferred(
          mockSavedData,
          mockChangeFails,
          { responseText: JSON.stringify(mockChangeResponse) },
          mockChangePending
        )
        return mockLastChangeDeferred
      })
    }
  }
}))

jest.mock('../../../../adhocracy4/dashboard/assets/dashboard', () => ({
  updateDashboard: jest.fn()
}))

import api from '../../../static/api'
import { PollManagement } from '../PollDashboard/PollManagement'
import { resetLocalKeys } from '../PollDashboard/utils'

const choiceQuestion = {
  id: 1,
  label: 'First question',
  help_text: '',
  multiple_choice: false,
  is_open: false,
  is_confidential: false,
  choices: [
    { id: 10, label: 'A', is_other_choice: false },
    { id: 11, label: 'B', is_other_choice: false }
  ],
  userChoices: [],
  answers: [],
  image_url: null,
  totalVoteCount: 0
}

const openQuestion = {
  id: 2,
  label: 'Second question',
  help_text: 'an explanation',
  multiple_choice: false,
  is_open: true,
  is_confidential: false,
  choices: [],
  userChoices: [],
  answers: [],
  image_url: null
}

describe('PollManagement', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    resetLocalKeys()
    mockChangeFails = false
    mockChangePending = false
    mockLastChangeDeferred = null
    mockPollData = {
      allow_unregistered_users: false,
      hide_results_until_finished: false,
      presentation_mode: 'multistep',
      questions: [choiceQuestion, openQuestion]
    }
    mockSavedData = {
      allow_unregistered_users: false,
      hide_results_until_finished: false,
      presentation_mode: 'multistep',
      questions: [choiceQuestion, openQuestion]
    }
    mockChangeResponse = { questions: [{ label: ['Please provide a question.'] }, {}] }
  })

  const renderManagement = (props = {}) => render(
    <PollManagement
      pollId={1}
      enableUnregisteredUsers
      questionImagesEnabled={false}
      {...props}
    />
  )

  it('renders the questions as a collapsed list', async () => {
    renderManagement()
    expect(await screen.findByText('First question')).toBeInTheDocument()
    expect(screen.getByText('Second question')).toBeInTheDocument()
    expect(screen.getByText('01')).toBeInTheDocument()
    expect(screen.getByText('02')).toBeInTheDocument()
    // collapsed: no editor fields visible
    expect(screen.queryByLabelText('Move question up')).not.toBeInTheDocument()
  })

  it('expands a question when clicked and collapses on a second click', async () => {
    const { container } = renderManagement()
    fireEvent.click(await screen.findByText('First question'))
    expect(screen.getByLabelText('Move question up')).toBeInTheDocument()

    const textarea = screen.getByRole('textbox', { name: /Question/ })
    fireEvent.change(textarea, { target: { value: 'Edited' } })

    fireEvent.click(container.querySelector('.poll-management__summary'))
    expect(screen.queryByLabelText('Move question up')).not.toBeInTheDocument()
    // edits are kept in the local state
    expect(screen.getByText('Edited')).toBeInTheDocument()
  })

  it('warns about unsaved changes when leaving the page', async () => {
    renderManagement()
    fireEvent.click(await screen.findByText('First question'))

    const cleanUnload = new Event('beforeunload', { cancelable: true })
    window.dispatchEvent(cleanUnload)
    expect(cleanUnload.defaultPrevented).toBe(false)

    fireEvent.change(screen.getByRole('textbox', { name: /Question/ }), { target: { value: 'Edited' } })

    const dirtyUnload = new Event('beforeunload', { cancelable: true })
    window.dispatchEvent(dirtyUnload)
    expect(dirtyUnload.defaultPrevented).toBe(true)
  })

  it('keeps edits local until the poll is saved', async () => {
    renderManagement()
    fireEvent.click(await screen.findByText('First question'))
    fireEvent.change(screen.getByRole('textbox', { name: /Question/ }), { target: { value: 'Edited' } })

    expect(api.poll.change).not.toHaveBeenCalled()
  })

  it('moves the question within the survey with the arrow controls', async () => {
    const { container } = renderManagement()
    fireEvent.click(await screen.findByText('First question'))
    fireEvent.click(screen.getByLabelText('Move question down'))

    const labels = Array.from(container.querySelectorAll('.poll-management__label')).map((el) => el.textContent)
    expect(labels[0]).toBe('Second question')
    expect(labels[1]).toBe('First question')
  })

  it('switches a choice question to an open question and back', async () => {
    renderManagement()
    fireEvent.click(await screen.findByText('First question'))

    // switch to open text: choices are removed
    fireEvent.click(screen.getByRole('button', { name: 'Open Text' }))
    expect(screen.queryByText('Answer option')).not.toBeInTheDocument()

    // switch back to single choice: two empty answers are seeded
    fireEvent.click(screen.getByRole('button', { name: 'Single choice' }))
    expect(screen.getByText('Answer option')).toBeInTheDocument()
    expect(screen.getAllByText(/^Answer #/)).toHaveLength(2)

    // switching to multiple choice keeps the answers
    fireEvent.click(screen.getAllByRole('button', { name: 'Multiple choice' })
      .find((button) => button.classList.contains('poll-management__answer-type-btn')))
    expect(screen.getByText('Answer option')).toBeInTheDocument()
    expect(screen.getAllByText(/^Answer #/)).toHaveLength(2)
  })

  it('adds a new open question and expands it', async () => {
    const { container } = renderManagement()
    await screen.findByText('First question')
    // the "New question" button is rendered above the list and in the footer
    fireEvent.click(screen.getAllByText('New question')[0])
    fireEvent.click(screen.getAllByText('Open question')[0])

    expect(screen.getByLabelText('Move question up')).toBeInTheDocument()
    expect(container.querySelectorAll('.poll-management__list-item')).toHaveLength(3)
  })

  it('adds a new multiple choice question and marks it as multiple choice', async () => {
    const { container } = renderManagement()
    await screen.findByText('First question')
    fireEvent.click(screen.getAllByText('New question')[0])
    fireEvent.click(screen.getAllByRole('button', { name: 'Multiple choice' })[0])

    const types = Array.from(container.querySelectorAll('.poll-management__type')).map((el) => el.textContent)
    expect(types[types.length - 1]).toBe('Multiple choice')
    expect(container.querySelectorAll('.poll-management__list-item')).toHaveLength(3)
  })

  it('deletes a question after confirming', async () => {
    renderManagement()
    await screen.findByText('First question')
    fireEvent.click(screen.getAllByLabelText('Delete question')[0])
    // first click only asks for confirmation
    expect(screen.getByText('First question')).toBeInTheDocument()
    fireEvent.click(screen.getByLabelText('Confirm delete'))

    expect(screen.queryByText('First question')).not.toBeInTheDocument()
    expect(screen.getByText('01')).toBeInTheDocument()
    expect(screen.getByText('Second question')).toBeInTheDocument()
  })

  it('sends the full payload on save and strips read-only fields', async () => {
    renderManagement()
    await screen.findByText('First question')
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(api.poll.change).toHaveBeenCalledTimes(1)
    const [payload, pollId] = api.poll.change.mock.calls[0]
    expect(pollId).toBe(1)
    expect(payload.allow_unregistered_users).toBe(false)
    expect(payload.hide_results_until_finished).toBe(false)
    expect(payload.presentation_mode).toBe('multistep')
    expect(payload.questions).toHaveLength(2)
    expect(payload.questions[0]).toEqual({
      id: 1,
      label: 'First question',
      help_text: '',
      multiple_choice: false,
      is_open: false,
      is_confidential: false,
      choices: [
        { id: 10, label: 'A', is_other_choice: false },
        { id: 11, label: 'B', is_other_choice: false }
      ],
      image_alt_text: ''
    })
    expect(payload.questions[0].userChoices).toBeUndefined()
    expect(payload.questions[0].answers).toBeUndefined()
    expect(payload.questions[0].image_url).toBeUndefined()
  })

  it('shows an alert and expands the question with errors on failed save', async () => {
    mockChangeFails = true
    renderManagement()
    await screen.findByText('First question')
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => {
      expect(document.querySelector('#alert')).toHaveTextContent('Please provide a question.')
    })
    expect(screen.getByLabelText('Move question up')).toBeInTheDocument()
  })

  it('clears only the edited field error, keeping the others visible', async () => {
    mockChangeFails = true
    mockChangeResponse = {
      questions: [{ label: ['Please provide a question.'], help_text: ['Please explain.'] }, {}]
    }
    renderManagement()
    await screen.findByText('First question')
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))
    await screen.findByText('Please provide a question.')

    // reveal and edit the explanation field only
    fireEvent.click(screen.getByText('Explanation'))
    fireEvent.change(screen.getByRole('textbox', { name: /Explanation/ }), {
      target: { value: 'Because' }
    })

    expect(screen.queryByText('Please explain.')).not.toBeInTheDocument()
    expect(screen.getByText('Please provide a question.')).toBeInTheDocument()
  })

  it('toggles the unregistered users option', async () => {
    renderManagement()
    const checkbox = await screen.findByLabelText('Allow unregistered users to vote')
    fireEvent.click(checkbox)
    expect(checkbox).toBeChecked()
  })

  it('saves the chosen presentation mode', async () => {
    renderManagement()
    await screen.findByText('First question')

    const multistep = screen.getByLabelText('Answer in multiple steps')
    expect(multistep).toBeChecked()

    fireEvent.click(multistep)
    expect(multistep).not.toBeChecked()

    fireEvent.click(screen.getByRole('button', { name: 'Save' }))
    const [payload] = api.poll.change.mock.calls[0]
    expect(payload.presentation_mode).toBe('longform')
  })

  it('collapses an expanded question when its row is clicked again', async () => {
    const { container } = renderManagement()
    fireEvent.click(await screen.findByText('First question'))
    expect(screen.getByLabelText('Move question up')).toBeInTheDocument()

    fireEvent.click(container.querySelector('.poll-management__summary'))
    expect(screen.queryByLabelText('Move question up')).not.toBeInTheDocument()
  })

  it('reorders questions via drag and drop', async () => {
    const { container } = renderManagement()
    await screen.findByText('First question')

    const items = container.querySelectorAll('.poll-management__item')
    expect(items).toHaveLength(2)

    fireEvent.dragStart(items[0])
    fireEvent.dragEnter(items[1])
    fireEvent.dragOver(items[1])
    fireEvent.drop(items[1])
    fireEvent.dragEnd(items[0])

    expect(screen.getByText('01')).toBeInTheDocument()
    // after the drop the second question is first in the list
    const labels = Array.from(container.querySelectorAll('.poll-management__label')).map((el) => el.textContent)
    expect(labels[0]).toBe('Second question')
  })

  it('reorders questions via the drag handle on touch devices', async () => {
    // jsdom does not implement PointerEvent; testing-library needs one that
    // carries clientX/clientY and pointerType for React's pointer handlers.
    class PointerEventPolyfill extends MouseEvent {
      constructor (type, params = {}) {
        super(type, params)
        this.pointerType = params.pointerType || ''
        this.pointerId = params.pointerId ?? 0
      }
    }
    window.PointerEvent = PointerEventPolyfill

    const { container } = renderManagement()
    await screen.findByText('First question')

    const listItems = container.querySelectorAll('.poll-management__list-item')
    const first = listItems[0]
    const second = listItems[1]
    const handle = first.querySelector('.poll-management__drag-handle')
    const list = container.querySelector('.poll-management__list')

    // jsdom lacks pointer capture and hit testing
    Element.prototype.setPointerCapture = jest.fn()
    Element.prototype.releasePointerCapture = jest.fn()
    Element.prototype.hasPointerCapture = jest.fn(() => true)
    document.elementFromPoint = jest.fn((_x, y) => (
      y < 50 ? first : second
    ))

    fireEvent.pointerDown(handle, { pointerType: 'touch', clientX: 10, clientY: 10 })
    fireEvent.pointerMove(list, { pointerId: 1, clientX: 10, clientY: 60 })
    fireEvent.pointerUp(list, { pointerId: 1, clientX: 10, clientY: 60 })

    const labels = Array.from(container.querySelectorAll('.poll-management__label')).map((el) => el.textContent)
    expect(labels[0]).toBe('Second question')
    expect(labels[1]).toBe('First question')
  })

  it('does not reorder when the touch gesture is canceled', async () => {
    class PointerEventPolyfill extends MouseEvent {
      constructor (type, params = {}) {
        super(type, params)
        this.pointerType = params.pointerType || ''
        this.pointerId = params.pointerId ?? 0
      }
    }
    window.PointerEvent = PointerEventPolyfill

    const { container } = renderManagement()
    await screen.findByText('First question')

    const listItems = container.querySelectorAll('.poll-management__list-item')
    const first = listItems[0]
    const second = listItems[1]
    const handle = first.querySelector('.poll-management__drag-handle')
    const list = container.querySelector('.poll-management__list')

    Element.prototype.setPointerCapture = jest.fn()
    Element.prototype.releasePointerCapture = jest.fn()
    Element.prototype.hasPointerCapture = jest.fn(() => true)
    document.elementFromPoint = jest.fn((_x, y) => (
      y < 50 ? first : second
    ))

    fireEvent.pointerDown(handle, { pointerType: 'touch', clientX: 10, clientY: 10 })
    fireEvent.pointerMove(list, { pointerId: 1, clientX: 10, clientY: 60 })
    fireEvent.pointerCancel(list, { pointerId: 1, clientX: 10, clientY: 60 })

    const labels = Array.from(container.querySelectorAll('.poll-management__label')).map((el) => el.textContent)
    expect(labels[0]).toBe('First question')
    expect(labels[1]).toBe('Second question')
  })

  it('does not delete the last remaining question', async () => {
    mockPollData = {
      allow_unregistered_users: false,
      hide_results_until_finished: false,
      questions: [choiceQuestion]
    }
    const { container } = renderManagement()
    await screen.findByText('First question')

    fireEvent.click(screen.getByLabelText('Delete question'))
    fireEvent.click(screen.getByLabelText('Confirm delete'))

    expect(container.querySelectorAll('.poll-management__list-item')).toHaveLength(1)
    expect(screen.getByText('First question')).toBeInTheDocument()
  })

  it('hides the editor and offers a retry when loading fails', async () => {
    api.poll.get.mockImplementationOnce(() => mockMakeDeferred(null, true, null))
    renderManagement()

    expect(await screen.findByText('The poll could not be loaded. Please try again.')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Save' })).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Retry' }))

    expect(await screen.findByText('First question')).toBeInTheDocument()
    expect(api.poll.get).toHaveBeenCalledTimes(2)
  })

  it('keeps edits made while a save is pending', async () => {
    mockChangePending = true
    renderManagement()
    fireEvent.click(await screen.findByText('First question'))

    const textarea = screen.getByRole('textbox', { name: /Question/ })
    fireEvent.change(textarea, { target: { value: 'Before save' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))
    expect(api.poll.change).toHaveBeenCalledTimes(1)

    fireEvent.change(textarea, { target: { value: 'Edited while saving' } })
    await act(async () => {
      mockLastChangeDeferred.resolve(mockSavedData)
    })

    expect(screen.getByRole('textbox', { name: /Question/ })).toHaveValue('Edited while saving')

    const unload = new Event('beforeunload', { cancelable: true })
    window.dispatchEvent(unload)
    expect(unload.defaultPrevented).toBe(true)
  })
})
