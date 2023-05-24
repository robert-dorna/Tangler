import { writable, derived } from 'svelte/store'
import client from './client'


function createDisplayConfig() {
  const { subscribe, set } = writable({});

  function fetch() {
    client.config.read().then((json) => {
      set({
        types: json.types,
        order: json.order,
        emojis: json.order.map((typename) => json.types[typename].emoji),
      })
    });
  }

  return {
    subscribe,
    fetch,
  };
}

export const displayConfig = createDisplayConfig()
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
