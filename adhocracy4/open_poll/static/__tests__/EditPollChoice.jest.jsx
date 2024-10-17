// tools needed for testing
import React from 'react'
import { render, fireEvent } from '@testing-library/react'

// component and related data to be tested
import { EditPollChoice } from '../PollDashboard/EditPollChoice.jsx'

const CHOICE_OBJECT = {
  id: 1,
  label: 'cool1',
  count: 0,
  is_other_choice: false
}

describe('<EditPollChoice> with...', () => {
  test('label', () => {
    const tree = render(
      <EditPollChoice
        id={CHOICE_OBJECT.id}
        index={CHOICE_OBJECT.id}
        label={CHOICE_OBJECT.label}
        choice={CHOICE_OBJECT}
        choiceId={CHOICE_OBJECT.id}
        undeletable
      />
    )
    const choiceTextInput = tree.container.querySelector('#id_choices-1-name')
    expect(choiceTextInput.value).toBe(CHOICE_OBJECT.label)
  })

  test('on label change', () => {
    const onLabelChangedFn = jest.fn()
    const tree = render(
      <EditPollChoice
        id={CHOICE_OBJECT.id}
        index={CHOICE_OBJECT.id}
        label={CHOICE_OBJECT.label}
        choice={CHOICE_OBJECT}
        choiceId={CHOICE_OBJECT.id}
        onLabelChange={(label) => { onLabelChangedFn() }}
        undeletable
      />
    )
    const choiceTextInput = tree.container.querySelector('#id_choices-1-name')
    fireEvent.change(choiceTextInput, { target: { value: 'change text' } })
    expect(onLabelChangedFn).toHaveBeenCalled()
  })
})
