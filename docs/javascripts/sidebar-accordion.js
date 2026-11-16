document.addEventListener('change', (event) => {
  const openedToggle = event.target
  if (
    !(openedToggle instanceof HTMLInputElement)
    || !openedToggle.matches('.md-nav__toggle[type="checkbox"]')
    || !openedToggle.checked
  ) {
    return
  }

  const openedItem = openedToggle.closest('.md-nav__item--nested')
  const siblingList = openedItem?.parentElement
  if (!siblingList?.classList.contains('md-nav__list')) return

  for (const siblingItem of siblingList.children) {
    if (siblingItem === openedItem) continue

    const siblingToggle = siblingItem.querySelector(
      ':scope > .md-nav__toggle[type="checkbox"]',
    )
    if (!siblingToggle) continue

    siblingToggle.checked = false
    for (const descendantToggle of siblingItem.querySelectorAll(
      '.md-nav__toggle[type="checkbox"]',
    )) {
      descendantToggle.checked = false
    }
  }
})
