const request = async (method, path, data = null) => {
  url = `${window.location.href}${path}`
  const options = { method }
  if (data) {
    options.headers = { 'Content-Type': 'application/json' }
    options.body = JSON.stringify(data)
  }
  return fetch(url, options).then((res) => res.json());
}

const req = async (url, options, args = []) => {
  url = `${window.location.href}${url}`

  const shouldOmmit = value => value === null || value === undefined || String(value).toUpperCase() === "NULL";
  const encode = value => String(value).replace(' ', '%20')

  let urlArgs = []
  Object.keys(args).forEach(key => {
    const value = args[key]
    if (!shouldOmmit(value)) {
      urlArgs.push(`${key}=${encode(args[key])}`)
    }
  })

  urlArgs = urlArgs.join('&')
  if (urlArgs) {
    url += `?${urlArgs}`
  }

  return fetch(url, options).then((res) => res.json());
}

const client = {
  new: {
    // not used yet, use it to replace old api listed below
    config: {
      read: async (section = null) => request('GET', section ? `/config/${section}` : '/config'),
      types: {
        read: async (what = null) => request('GET', what ? `/config/types/${what}` : '/config/types'),
        create: async (what, cfg) => request('POST', `/config/types/${what}`, cfg),
        update: async (what, cfg) => request('PATCH', `/config/types/${what}`, cfg),
        delete: async (what) => request('DELETE', `/config/types/${what}`),
      },
      order: {
        read: async () => request('GET', '/config/order'),
        update: async (newOrder) => request('PUT', '/config/order', newOrder),
      }
    },
    items: {
      read: async (what) => request('GET', `/data/${what}`)
    },
    item: {
      read: async (what, id) => request('GET', `/data/${what}/${id}`),
      create: async (what, fields) => request('POST', `/data/${what}`, fields),
      update: async (what, id, fields) => request('PATCH', `/data/${what}/${id}`, fields),
      delete: async (what, id) => request('DELETE', `/data/${what}/${id}`),
    },
  },

  // todo: old api, remove
  get: async (args) => req('api/old/data', { method: 'GET' }, args),
  update: async (args) => req('api/old/data', { method: 'POST' }, args),
  create: async (args) => req('api/old/data', { method: 'PUT' }, args),
  move: async (args) => req('api/old/move', { method: 'GET' }, args),
  unlink: async (args) => req('api/old/unlink', { method: 'GET' }, args),
  config: async () => req('api/old/config', { method: 'GET' }),
  patchConfig: async (data) => req('api/old/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}

export default client
