import { writable, derived } from 'svelte/store'
import client from './client';


function createDisplayConfig() {
  const { subscribe, set, update } = writable({});

  function fetch() {
    client.displayConfig().then((json) => {
      set({
        types: json.types,
        order: json.order,
        emojis: json.order.map((typename) => json.types[typename].emoji),
      })
    });
  }

  return {
    subscribe,
    set,
    update,
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
  const plain = {
    _children: [],
    // _what: $newItem.anchorWhat,
    _what: null,
    title: "new item",
  };

  const nothingSelected = {
    location: false, // createMode
    anchorId: null,
    anchorWhat: null,
    fields: plain,
  }

  const { subscribe, set, update } = writable(nothingSelected)

  function select(anchor, location) {
    set({ location, anchorId: anchor._id, anchorWhat: anchor._what })
  }

  function create(fields) {
    client
      .create({
        ...fields,
        _aboveId: item["_id"],
        _aboveWhat: item["_what"],
      })
      .then(() => {
        newItem.discard();
      });
  }

  function discard() {
    set(nothingSelected)
  }

  return {
    LOCATION,
    plain,
    subscribe,
    set,
    update,
    select,
    create,
    discard,
  };
}

export const newItem = createNewItem()
