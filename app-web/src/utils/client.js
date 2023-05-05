
const req = async (method, url, args = []) => {
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

  return fetch(url, { method }).then((res) => res.json());
}

const client = {
  get: async (args) => req('GET', `${window.location.href}api/data`, args),
  update: async (args) => req('POST', `${window.location.href}api/data`, args),
  create: async (args) => req('PUT', `${window.location.href}api/data`, args),
  move: async (args) => req('GET', `${window.location.href}api/move`, args),
  unlink: async (args) => req('GET', `${window.location.href}api/unlink`, args),
  config: async () => req('GET', `${window.location.href}api/config`),
}

export default client
