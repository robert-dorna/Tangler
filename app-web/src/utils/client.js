
const req = async (url, args = []) => {
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

  return fetch(url).then((res) => res.json());
}

const client = {
  get: async (args) => req(`${window.location.href}api/data`, args),
  update: async (args) => req(`${window.location.href}api/update`, args),
  create: async (args) => req(`${window.location.href}api/create`, args),
  move: async (args) => req(`${window.location.href}api/move`, args),
  unlink: async (args) => req(`${window.location.href}api/unlink`, args),
  displayConfig: async () => req(`${window.location.href}api/display`),
}

export default client
