

function diffObjects(template, actual) {
  const diff = {};
  for (const [field, value] of Object.entries(actual)) {
    if (value !== template[field]) {
      diff[field] = value;
    }
  }
  return diff;
}

const utils = {
  diffObjects
}

export default utils;