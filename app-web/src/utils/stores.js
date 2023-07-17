import { writable, derived } from 'svelte/store'
import client from './client'


class ConfigStore {
  constructor() {
    const { subscribe, set } = writable({});

    this.subscribe = subscribe
    this.set = set
  }

  fetch() {
    client.config.read().then((result) => {
      this.set({
        types: result.types,
        order: result.order,
        emojis: result.order.map((typename) => result.types[typename].emoji),
      })
    });
  }
}

export const config = new ConfigStore
export const selectedType = writable(null)

config.subscribe((newConfig) => {
  if (newConfig.order) {
    selectedType.set(newConfig.order[0])
  }
})

class ItemsStore {
  constructor() {
    const { subscribe, set } = writable([])

    this.subscribe = subscribe
    this.set = set
  }

  fetch(typeName) {
    client.data.read(typeName).then((result) => {
      this.set(result)
    });
  }
}

export const items = new ItemsStore

selectedType.subscribe((newSelectedType) => {
  if (newSelectedType !== null) {
    items.fetch(newSelectedType)
  }
})

export const displayConfig = config
export const displayConfigAvailable = derived(displayConfig, $displayConfig => Boolean(Object.keys($displayConfig).length !== 0))
export const displayConfigTypes = derived(displayConfig, $displayConfig => $displayConfig.types)

export const LOCATION = Object.freeze({
  ABOVE: 1,
  BELOW: 2,
  CHILD: 3,
});

export const movingItem = writable(null)

function createNewItem() {
  const nothingSelected = {
    location: false,
    anchorId: null,
    anchorWhat: null,
  }

  const { subscribe, set } = writable(nothingSelected)

  function select(anchor, location) {
    set({ location, anchorId: anchor._id, anchorWhat: anchor._what })
  }

  function discard() {
    set(nothingSelected)
  }

  return {
    subscribe,
    select,
    discard,
  };
}

export const newItem = createNewItem()
