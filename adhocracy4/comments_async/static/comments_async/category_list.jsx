import React from 'react'
import django from 'django'

const translated = {
  chooseCategories: django.gettext('Choose categories for your comment')
}

const CategoryList = (props) => (
  <fieldset>
    <legend className="sr-only">{translated.chooseCategories}</legend>
    {Object.keys(props.categoryChoices).map(objectKey => {
      const categoryCheck = props.categoryChoices[objectKey]
      const inputId = props.idPrefix + '_' + objectKey
      const categoryClass = 'badge a4-comments__category__text a4-comments__category__' + objectKey
      return (
        <div className="a4-comments__category" key={objectKey}>
          <label className="a4-comments__category__row" htmlFor={inputId}>
            <input
              className="a4-comments__category__input"
              type="checkbox"
              checked={props.categoriesChecked.indexOf(objectKey) > -1}
              onChange={props.handleControlFunc}
              id={inputId}
              value={categoryCheck}
            />
            <span className={categoryClass}> {categoryCheck}</span>
          </label>
        </div>
      )
    })}
  </fieldset>
)

export default CategoryList
