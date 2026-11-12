import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

jest.mock('django', () => ({
  gettext: (text) => text,
  pgettext: (context, text) => text,
  ngettext: (singular, plural, count) => count === 1 ? singular : plural,
  interpolate: (fmt, data, named) => {
    if (named) {
      return fmt.replace(/%\((\w+)\)s/g, (match, key) => data[key])
    }
    return fmt
  }
}))

import PollLongform from '../PollDetail/PollLongform'

describe('PollLongform', () => {
  const choiceQuestion = {
    id: 1,
    label: 'Favorite color',
    is_open: false,
    multiple_choice: false,
    is_confidential: false,
    authenticated: true,
    choices: [
      { id: 10, label: 'Red', is_other_choice: false },
      { id: 11, label: 'Blue', is_other_choice: false }
    ]
  }

  const openQuestion = {
    id: 2,
    label: 'Your thoughts',
    is_open: true,
    authenticated: true,
    multiple_choice: false,
    choices: [],
    answers: [],
    userAnswer: null
  }

  const baseProps = {
    questions: [choiceQuestion, openQuestion],
    answers: {},
    allowUnregisteredUsers: false,
    questionImagesEnabled: false,
    errors: {},
    useTermsOfUse: false,
    agreedTermsOfUse: false,
    orgTermsUrl: '',
    checkedTermsOfUse: false,
    showCaptcha: false,
    captcha: '',
    onSetCheckedTerms: jest.fn(),
    onAnswerChange: jest.fn(),
    onSubmit: jest.fn(),
    isLoading: false
  }

  it('renders all questions without a progress bar', () => {
    render(<PollLongform {...baseProps} />)

    expect(screen.getByText('Favorite color')).toBeInTheDocument()
    expect(screen.getByText('Your thoughts')).toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
  })

  it('forwards the answer of every question', () => {
    const onAnswerChange = jest.fn()
    render(<PollLongform {...baseProps} onAnswerChange={onAnswerChange} />)

    fireEvent.click(screen.getByLabelText('Red'))
    expect(onAnswerChange).toHaveBeenCalledWith(1, { choices: [10] })

    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'My answer' } })
    expect(onAnswerChange).toHaveBeenCalledWith(2, { open_answer: 'My answer' })
  })

  it('submits all answers at once', () => {
    const onSubmit = jest.fn()
    render(<PollLongform {...baseProps} onSubmit={onSubmit} />)

    fireEvent.click(screen.getByRole('button', { name: 'Submit All' }))
    expect(onSubmit).toHaveBeenCalledTimes(1)
  })

  it('disables submitting until the terms of use are accepted', () => {
    render(<PollLongform {...baseProps} useTermsOfUse />)

    const submit = screen.getByRole('button', { name: 'Submit All' })
    expect(submit).toBeDisabled()
    expect(screen.getByRole('checkbox')).toBeInTheDocument()
  })

  it('disables submitting until the captcha is solved', () => {
    render(<PollLongform {...baseProps} showCaptcha />)

    expect(screen.getByRole('button', { name: 'Submit All' })).toBeDisabled()
  })

  it('keeps the inputs read-only while submitting', () => {
    render(<PollLongform {...baseProps} isLoading />)

    expect(screen.getByLabelText('Red')).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Submitting...' })).toBeDisabled()
  })
})
