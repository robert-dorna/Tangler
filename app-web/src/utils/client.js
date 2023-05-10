
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
  get: async (args) => req('api/data', { method: 'GET' }, args),
  update: async (args) => req('api/data', { method: 'POST' }, args),
  create: async (args) => req('api/data', { method: 'PUT' }, args),
  move: async (args) => req('api/move', { method: 'GET' }, args),
  unlink: async (args) => req('api/unlink', { method: 'GET' }, args),
  config: async () => req('api/config', { method: 'GET' }),
  patchConfig: async (data) => req('api/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}

export default client
