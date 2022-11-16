window.addEventListener('load', function () {
  const formsets = document.querySelectorAll('.js-formset')
  const PLACEHOLDER = /__prefix__/g
  const dynamicFormSets = []
  const selectDropdownSettings = {
    style: 'category-icon-select__btn',
    styleDropdown: 'category-icon-select'
  }

  // empty formset created on page load
  // used in: module_label_forms, module_category_forms {include inline_form}
  const DynamicFormSet = function (formset) {
    this.formset = formset
    this.formTemplate = this.formset.querySelector('.js-form-template')
    // prefix from django form modal
    this.prefix = this.formset.dataset.prefix
    this.totalInput = this.formset.querySelector(
      '#id_' + this.prefix + '-TOTAL_FORMS'
    )
    this.total = parseInt(this.totalInput.value)
    // maxNum from django form modal
    this.maxNum = parseInt(
      this.formset.querySelector('#id_' + this.prefix + '-MAX_NUM_FORMS').value
    )

    this.formset
      .querySelector('.js-add-form')
      .addEventListener('click', addForm.bind(this))
  }

  // checks if max forms reached and inserts field before hidden template element
  const addForm = function () {
    if (this.total < this.maxNum) {
      this.total += 1
      this.totalInput.value = this.total
      const newForm = getNewForm(this.formTemplate, this.total - 1)
      this.formTemplate.insertAdjacentHTML('beforebegin', newForm)

      // take new field and add event listener to delete btn
      this.formTemplate.previousElementSibling
        .querySelector('.js-remove-form')
        .addEventListener('click', removeForm.bind(this))
      // only calling jquery for select dropdown (used for icon select for map modules)
      if (window.jQuery.fn.selectdropdown) {
        window
          .jQuery(
            this.formTemplate.previousElementSibling.querySelector(
              '.category-icon-select'
            )
          )
          .selectdropdown(selectDropdownSettings)
      }
    }
  }

  // list all fields and remove field before save
  const removeForm = function (event) {
    const _this = this
    this.total -= 1
    this.totalInput.value = this.total
    const form = event.currentTarget.closest('.js-form')
    const id = Array.from(this.formset.querySelectorAll('.js-form')).indexOf(
      form
    )

    // update index prefix of all elements in fields after removed field
    const updateAttr = function (element, key, i) {
      // boolean to check attribute
      if (element.hasAttribute(key)) {
        const _old = _this.prefix + '-' + (id + i + 1)
        const _new = _this.prefix + '-' + (id + i)
        element.setAttribute(key, element.getAttribute(key).replace(_old, _new))
      }
    }

    // loop through elements in field and run updateAttr to ensure correct index
    let nextSibling = form.nextElementSibling
    while (nextSibling && nextSibling !== this.formTemplate) {
      Array.from(nextSibling.firstElementChild.children)
        .forEach(function (element, i) {
          updateAttr(element, 'name', i)
          updateAttr(element, 'for', i)
          updateAttr(element, 'id', i)
        })
      nextSibling = nextSibling.nextElementSibling
    }
    form.remove()
  }

  // create a form as a string object, replacing prefix with correct id
  function getNewForm (formTemplate, id) {
    const gotForm = formTemplate.innerHTML.replace(PLACEHOLDER, id)
    return gotForm
  }

  formsets.forEach(function (formset, i) {
    dynamicFormSets.push(new DynamicFormSet(formset))
  })

  // only calling jquery for select dropdown (used for icon select for map modules)
  if (window.jQuery.fn.selectdropdown) {
    window.jQuery('.category-icon-select')
      .not('.js-form-template .category-icon-select')
      .selectdropdown(selectDropdownSettings)
  }
})
