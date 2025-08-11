import React, { useState } from 'react';
import classNames from '../classNames';
import useCombobox from './useCombobox';
import Choice from '../../types/choice';

interface AutoCompleteProps<T = any> {
  label: string;
  className?: string;
  liClassName?: string;
  comboboxClassName?: string;
  choices: Choice<T>[];
  hideLabel?: boolean;
  onChangeInput?: (text: string) => void;
  filterFn?: (choice: Choice<T>, text: string) => boolean;
  placeholder?: string;
  before?: React.ReactNode;
  after?: React.ReactNode;
  isMultiple?: boolean;
  values?: T[];
  defaultValue?: T | T[];
  onChange?: (newValues: T[]) => void;
}

const defaultFilterFn = <T,>(choice: Choice<T>, text: string): boolean =>
  choice.name.toLowerCase().includes(text.toLowerCase());

export const AutoComplete = <T,>({
  label,
  className,
  liClassName,
  comboboxClassName,
  choices,
  hideLabel = false,
  onChangeInput,
  filterFn,
  placeholder,
  before,
  after,
  ...comboboxProps
}: AutoCompleteProps<T>) => {
  const {
    opened,
    labelId,
    activeItems,
    listboxAttrs,
    comboboxAttrs,
    getChoicesAttr,
  } = useCombobox({
    choices,
    ...comboboxProps,
    isAutoComplete: true,
  });

  const [text, setText] = useState('');

  const classes = classNames(
    'form-control a4-combo-box__container',
    opened && 'a4-combo-box__container--opened',
    className
  );

  const comboboxClasses = classNames(
    'form-control a4-combo-box__combobox',
    comboboxClassName
  );

  const actualFilterFn = filterFn || defaultFilterFn;
  const filteredChoices = text !== '' ? choices.filter(choice => actualFilterFn(choice, text)) : choices;

  const onChangeHandler = (e: React.ChangeEvent<HTMLInputElement | HTMLLIElement>) => {
    setText(e.target.value.toString());
    onChangeInput?.(e.target.value.toString());
  };

  return (
    <div className="form-group a4-combo-box a4-combo-box--autocomplete">
      <p id={labelId} className={classNames('label', hideLabel && 'aural')}>
        {label}
      </p>
      <div className="a4-combo-box__input-wrapper form-control">
        {before && <div className="a4-combo-box__before">{before}</div>}
        {comboboxProps.isMultiple && (
          <div className="a4-combo-box__selected">
            {activeItems.map((choice) => choice.name).join(', ')}
          </div>
        )}
        <input
          type="text"
          value={text}
          onChange={onChangeHandler}
          placeholder={placeholder}
          className={comboboxClasses}
          {...comboboxAttrs}
        />
        {after && <div className="a4-combo-box__after">{after}</div>}
      </div>
      {filteredChoices.length > 0 && (
        <ul className={classes} {...listboxAttrs}>
          {filteredChoices.map((choice) => {
            const { active, focused, ...attrs } = getChoicesAttr(choice);
            const liClasses = classNames(
              liClassName,
              'a4-combo-box__option',
              active && 'a4-combo-box__option--active',
              focused && 'a4-combo-box__option--focus'
            );

            return (
              <li
                key={String(choice.value)}
                className={liClasses}
                {...attrs}
              >
                <span>{choice.name}</span>
                {active && <i className="fa fa-check" aria-hidden="true" />}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default AutoComplete;