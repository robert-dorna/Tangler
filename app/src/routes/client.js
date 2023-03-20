
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
  get: async (args) => req(`http://0.0.0.0:5000/data`, args),
  update: async (args) => req(`http://0.0.0.0:5000/update`, args),
  create: async (args) => req(`http://0.0.0.0:5000/create`, args),
  move: async (args) => req(`http://0.0.0.0:5000/move`, args),
  unlink: async (args) => req(`http://0.0.0.0:5000/unlink`, args),
  displayConfig: async () => req(`http://0.0.0.0:5000/display`),
}

export default client