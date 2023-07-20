import { writable, derived } from 'svelte/store'
import client from './client'

console.log('loading stores')

let typeValue = null;
let itemsLoadedValue = false;

export const spacesRaw = writable(null)
export const spaces = writable([])
export const space = writable(null)
export const config = writable(null)
export const type = writable(null)
export const itemsLoad = writable(false)
export const items = writable([])
export const itemsLoaded = writable(false)

// config aliases
export const order = writable([])
export const types = writable({})
export const emojis = writable([])


export function fetch() {
  console.log('fetching spaces')
  client.spaces.read().then(result => {
    spacesRaw.set(result)
  })
}

spacesRaw.subscribe((newValue) => {
  console.log('updated spacesRaw: ', newValue)
  if (newValue !== null) {
    spaces.set(newValue.all)
    space.set(newValue.selected)
  }
})

spaces.subscribe(newValue => {
  console.log('updated spaces: ', newValue)
})

space.subscribe(newValue => {
  console.log('updated space: ', newValue)
  if (newValue !== null) {
    // TODO: check if value is allowed (space in spaces)
    client.spaces.set(newValue).then(() => {
      client.config.read().then(result => {
        itemsLoaded.set(false)
        config.set({
          types: result.types,
          order: result.order,
          emojis: result.order.map((typename) => result.types[typename].emoji),
        })
      });
    })
  }
})

config.subscribe(newValue => {
  console.log('updated config: ', newValue)

  if (newValue !== null) {
    order.set(newValue.order)
    types.set(newValue.types)
    emojis.set(newValue.emojis)

    if (newValue.order) {
      type.set(newValue.order[0])
    }
    else {
      console.error('got config without order section')
    }

    itemsLoad.set(true)
  }
  else {
    order.set([])
    types.set({})
    emojis.set([])
  }
})

type.subscribe(newValue => {
  console.log('updated type: ', newValue)

  typeValue = newValue

  if (newValue !== null) {
    itemsLoad.set(true)
  }
})

itemsLoad.subscribe(newValue => {
  console.log('updated itemsLoad: ', newValue, { typeValue })
  if (newValue === true && typeValue !== null) {
    itemsLoaded.set(false)
    client.data.read(typeValue).then((result) => {
      items.set(result)
    });
  }
})

items.subscribe(newValue => {
  console.log('updated items: ', newValue)
  itemsLoaded.set(true)
})

itemsLoaded.subscribe(newValue => {
  console.log('updated itemsLoaded: ', newValue)
  itemsLoadedValue = newValue;
  if (newValue === true) {
    itemsLoad.set(false)
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

movingItem.subscribe((newMovingItem) => {
  console.log({ newMovingItem })
})

class NewItemStore {
  constructor() {
    this.nothingSelected = {
      location: false,
      anchor: {
        id: null,
        what: null,
      },
      item: {}
    }

    const { subscribe, set } = writable(this.nothingSelected)

    this.subscribe = subscribe
    this.set = set
  }

  select(anchor, location) {
    this.set({
      location,
      anchor: {
        id: anchor._id,
        what: anchor._what
      },
      item: {
        _id: 'new',
        _what: anchor._what
      }
    })
  }

  discard() {
    this.set(this.nothingSelected)
  }

  isAnchoredTo(anchor, potentialAnchor) {
    return anchor.id === potentialAnchor._id && anchor.what === potentialAnchor._what
  }
}

export const newItem = new NewItemStore

newItem.subscribe((newNewItem) => {
  console.log({ newNewItem })
})

type.subscribe(newValue => {
  if (newValue !== null) {
    newItem.discard()
  }
})