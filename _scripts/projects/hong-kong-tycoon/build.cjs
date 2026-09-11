const fs = require('node:fs');
const path = require('node:path');
const base = __dirname;
let html = fs.readFileSync(path.join(base, 'shell.html'), 'utf8');
for (const [token, name] of [['/* STYLES */', 'style.css'], ['/* ENGINE */', 'engine.js'], ['/* INTERFACE */', 'app.js']]) {
  const content = fs.readFileSync(path.join(base, name), 'utf8');
  if (!html.includes(token)) throw new Error(`Missing build marker: ${token}`);
  if (name.endsWith('.js') && /<\/script/i.test(content)) throw new Error(`Unsafe script terminator in ${name}`);
  html = html.replace(token, () => content);
}
fs.writeFileSync(path.join(base, 'index.html'), html);
console.log(`Built index.html (${Buffer.byteLength(html).toLocaleString()} bytes); no external assets or dependencies.`);
