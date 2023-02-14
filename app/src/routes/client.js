
const client = {
  get: async (args) => {
    let url = `http://0.0.0.0:5000/data`;

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
}

export default client