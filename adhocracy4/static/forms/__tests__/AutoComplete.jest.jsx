import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { AutoComplete } from '../AutoComplete'
import useCombobox from '../useCombobox'

jest.mock('../useCombobox')

describe('AutoComplete', () => {
  const choices = [
    { name: 'Swedish', value: 'sv' },
    { name: 'English', value: 'en' },
    { name: 'German', value: 'de' }
  ]

  const defaultMockHookReturn = {
    opened: false,
    labelId: 'test-label-id',
    activeItems: [],
    listboxAttrs: {
      role: 'listbox',
      'aria-multiselectable': 'true'
    },
    comboboxAttrs: {
      role: 'combobox',
      'aria-haspopup': 'true',
      'aria-expanded': false,
      'aria-labelledby': 'test-label-id'
    },
    getChoicesAttr: (choice) => ({
      role: 'option',
      'aria-selected': false,
      active: false,
      focused: false
    })
  }

  beforeEach(() => {
    useCombobox.mockImplementation(() => defaultMockHookReturn)
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('renders with label and input', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        placeholder="Type to search"
      />
    )

    expect(screen.getByText('Search Languages')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Type to search')).toBeInTheDocument()
  })

  test('handles text input and filtering', () => {
    const onChangeInput = jest.fn()
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        onChangeInput={onChangeInput}
      />
    )

    const input = screen.getByRole('combobox')
    fireEvent.change(input, { target: { value: 'en' } })

    expect(input.value).toBe('en')
    expect(onChangeInput).toHaveBeenCalledWith('en')
    expect(screen.getByText('English')).toBeInTheDocument()
    expect(screen.queryByText('Swedish')).not.toBeInTheDocument()
  })

  test('applies custom filter function', () => {
    const customFilter = jest.fn((choice, text) => choice.value.includes(text))
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        filterFn={customFilter}
      />
    )

    const input = screen.getByRole('combobox')
    fireEvent.change(input, { target: { value: 'sv' } })

    expect(customFilter).toHaveBeenCalled()
  })

  test('hides label when hideLabel is true', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        hideLabel
      />
    )

    const label = screen.getByText('Search Languages')
    expect(label).toHaveClass('aural')
  })

  test('renders before and after elements', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        before={<div data-testid="before">Before</div>}
        after={<div data-testid="after">After</div>}
      />
    )

    expect(screen.getByTestId('before')).toBeInTheDocument()
    expect(screen.getByTestId('after')).toBeInTheDocument()
  })

  test('displays multiple selected items', () => {
    useCombobox.mockImplementation(() => ({
      ...defaultMockHookReturn,
      activeItems: [
        { name: 'English', value: 'en' },
        { name: 'German', value: 'de' }
      ]
    }))

    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        isMultiple
      />
    )

    expect(screen.getByText('English, German')).toBeInTheDocument()
  })

  test('applies custom class names', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
        className="custom-class"
        comboboxClassName="custom-combobox"
        liClassName="custom-li"
      />
    )

    expect(screen.getByRole('listbox')).toHaveClass('custom-class')
    expect(screen.getByRole('combobox')).toHaveClass('custom-combobox')
    const options = screen.getAllByRole('option')
    options.forEach(option => {
      expect(option).toHaveClass('custom-li')
    })
  })

  test('shows check icon for active items', () => {
    useCombobox.mockImplementation(() => ({
      ...defaultMockHookReturn,
      getChoicesAttr: (choice) => ({
        ...defaultMockHookReturn.getChoicesAttr(choice),
        active: choice.value === 'en'
      })
    }))

    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
      />
    )

    const checkIcon = screen.getByText('English').closest('li').querySelector('.fa-check')
    expect(checkIcon).toBeInTheDocument()
  })

  test('hides listbox when no filtered choices', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
      />
    )

    const input = screen.getByRole('combobox')
    fireEvent.change(input, { target: { value: 'xyz' } })

    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })

  test('passes isAutoComplete prop to useCombobox', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={choices}
      />
    )

    expect(useCombobox).toHaveBeenCalledWith(
      expect.objectContaining({
        isAutoComplete: true
      })
    )
  })

  test('handles empty choices array', () => {
    render(
      <AutoComplete
        label="Search Languages"
        choices={[]}
      />
    )

    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })
})
