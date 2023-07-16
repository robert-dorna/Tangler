const request = async (method, path, data = null) => {
  const api_server = window.location.href + 'api'
  const options = { method }
  if (data) {
    options.headers = { 'Content-Type': 'application/json' }
    options.body = JSON.stringify(data)
  }
  return fetch(api_server + path, options).then((res) => res.json()).then(json => json.result);
}

const client = {
  config: {
    read: async (section = null) => request('GET', section ? `/config/${section}` : '/config'),
    setOrder: async (newOrder) => request('PUT', '/config/order', newOrder),
    type: {
      create: async (what, data) => request('POST', `/config/types/${what}`, data),
      read: async (what) => request('GET', `/config/types/${what}`),
      set: async (what, data) => request('PUT', `/config/types/${what}`, data),
      modify: async (what, data) => request('PATCH', `/config/types/${what}`, data),
      delete: async (what) => request('DELETE', `/config/types/${what}`),
    },
    field: {
      read: async (what, field = null) => request('GET', field ? `/config/fields/${what}/${field}` : `/config/fields/${what}`),
      create: async (what, field, data) => request('POST', `/config/fields/${what}/${field}`, data),
      set: async (what, field, data) => request('PUT', `/config/fields/${what}/${field}`, data),
      modify: async (what, field, data) => request('PATCH', `/config/fields/${what}/${field}`, data),
      delete: async (what, field) => request('DELETE', `/config/types/${what}/${field}`),
    }
  },
  data: {
    read: async (what, id = null) => request('GET', id !== null ? `/data/${what}/${id}` : `/data/${what}`),
    create: async (what, data) => request('POST', `/data/${what}`, data),
    modify: async (what, id, data) => request('PATCH', `/data/${what}/${id}`, data),
    delete: async (what, id) => request('DELETE', `/data/${what}/${id}`),
  },
}

export default client