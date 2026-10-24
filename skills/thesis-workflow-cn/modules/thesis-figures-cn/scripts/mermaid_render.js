#!/usr/bin/env node
/**
 * Offline Mermaid -> PNG renderer.
 *
 * Uses the bundled vendor/mermaid/mermaid.min.js and the locally installed Chrome or Edge
 * through the DevTools protocol. No npm packages and no network access are needed (Node 22+).
 *
 *   node mermaid_render.js <input.mmd> <output.png> --browser <chrome.exe> [--scale 3] [--config mermaid.json]
 *
 * Prints "ok <output>" on success; exits 1 with an error message otherwise.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');
const { pathToFileURL } = require('url');

const MERMAID_JS = path.resolve(__dirname, '..', 'vendor', 'mermaid', 'mermaid.min.js');
const TIMEOUT_MS = 60000;
const PADDING = 16;

function parseArgs(argv) {
  const args = { scale: 3, config: null, browser: null, positional: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--scale') args.scale = Number(argv[++i]) || 3;
    else if (a === '--config') args.config = argv[++i];
    else if (a === '--browser') args.browser = argv[++i];
    else args.positional.push(a);
  }
  return args;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function waitFor(fn, what) {
  const start = Date.now();
  while (Date.now() - start < TIMEOUT_MS) {
    const v = await fn();
    if (v) return v;
    await sleep(100);
  }
  throw new Error(`timed out waiting for ${what}`);
}

// Minimal DevTools protocol client over Node's built-in WebSocket
function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    const pending = new Map();
    let nextId = 1;
    ws.onmessage = ev => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) {
        const { res, rej } = pending.get(msg.id);
        pending.delete(msg.id);
        msg.error ? rej(new Error(msg.error.message)) : res(msg.result);
      }
    };
    ws.onerror = () => reject(new Error('cannot connect to browser DevTools'));
    ws.onopen = () => resolve({
      send: (method, params = {}) => new Promise((res, rej) => {
        const id = nextId++;
        pending.set(id, { res, rej });
        ws.send(JSON.stringify({ id, method, params }));
      }),
      close: () => ws.close(),
    });
  });
}

function pageHtml(code, config) {
  // The diagram source and config are embedded as JSON, so no escaping issues with quotes or <, >
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}#out{display:inline-block;padding:${PADDING}px}</style>
<script src="${pathToFileURL(MERMAID_JS).href}"></script></head><body><div id="out"></div>
<script>
window.__render = async () => {
  try {
    mermaid.initialize(Object.assign({ startOnLoad: false }, ${JSON.stringify(config)}));
    const { svg } = await mermaid.render('thesis-diagram', ${JSON.stringify(code)});
    const out = document.getElementById('out');
    out.innerHTML = svg;
    await document.fonts.ready;
    const r = out.getBoundingClientRect();
    return { width: Math.ceil(r.width), height: Math.ceil(r.height) };
  } catch (e) {
    return { error: String(e && e.message || e) };
  }
};
</script></body></html>`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const [input, output] = args.positional;
  if (!input || !output || !args.browser) {
    console.error('usage: node mermaid_render.js <input.mmd> <output.png> --browser <path> [--scale 3] [--config file.json]');
    process.exit(2);
  }
  if (typeof WebSocket === 'undefined' || typeof fetch === 'undefined') {
    console.error(`error=offline renderer needs Node.js 22+ (found ${process.version})`);
    process.exit(3);   // render_figures.py falls back to mermaid-cli on exit code 3
  }
  if (!fs.existsSync(MERMAID_JS)) throw new Error(`bundled Mermaid not found: ${MERMAID_JS}`);

  const code = fs.readFileSync(input, 'utf8').replace(/^﻿/, '');
  const config = args.config ? JSON.parse(fs.readFileSync(args.config, 'utf8')) : {};
  // Render at natural size; the PNG scale is controlled by --scale instead
  for (const key of ['flowchart', 'sequence', 'class', 'state', 'er', 'gantt', 'journey', 'pie']) {
    config[key] = Object.assign({ useMaxWidth: false }, config[key]);
  }

  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'thesis-mmd-'));
  const htmlFile = path.join(tmp, 'diagram.html');
  fs.writeFileSync(htmlFile, pageHtml(code, config), 'utf8');

  const browser = spawn(args.browser, [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--disable-extensions', '--allow-file-access-from-files', '--remote-debugging-port=0',
    `--user-data-dir=${path.join(tmp, 'profile')}`, 'about:blank',
  ], { stdio: 'ignore' });
  // On Windows the launcher process may exit at once and hand over to a child,
  // so the browser is shut down through DevTools rather than by PID.
  let spawnError = null;
  browser.on('error', e => { spawnError = e; });

  let client, browserClient;
  try {
    const portFile = path.join(tmp, 'profile', 'DevToolsActivePort');
    const [port, browserPath] = await waitFor(() => {
      if (spawnError) throw new Error(`cannot start browser ${args.browser}: ${spawnError.message}`);
      if (!fs.existsSync(portFile)) return null;
      const lines = fs.readFileSync(portFile, 'utf8').split('\n').map(s => s.trim());
      return lines[0] && lines[1] ? lines : null;
    }, 'browser start (check --browser path)');
    browserClient = await connect(`ws://127.0.0.1:${port}${browserPath}`);
    const target = await waitFor(async () => {
      const list = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json()).catch(() => []);
      return list.find(t => t.type === 'page');
    }, 'browser page');

    client = await connect(target.webSocketDebuggerUrl);
    await client.send('Page.navigate', { url: pathToFileURL(htmlFile).href });
    await waitFor(async () => {
      const r = await client.send('Runtime.evaluate', { expression: 'typeof window.__render === "function" && typeof mermaid !== "undefined"', returnByValue: true });
      return r.result.value;
    }, 'Mermaid to load');

    const r = await client.send('Runtime.evaluate', { expression: 'window.__render()', awaitPromise: true, returnByValue: true });
    const box = r.result.value;
    if (!box || box.error) throw new Error(`Mermaid syntax error: ${box ? box.error : 'no result'}`);

    await client.send('Emulation.setDeviceMetricsOverride', {
      width: Math.max(box.width, 100), height: Math.max(box.height, 100),
      deviceScaleFactor: args.scale, mobile: false,
    });
    const shot = await client.send('Page.captureScreenshot', {
      format: 'png', captureBeyondViewport: true,
      clip: { x: 0, y: 0, width: box.width, height: box.height, scale: 1 },
    });
    fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
    fs.writeFileSync(output, Buffer.from(shot.data, 'base64'));
    console.log(`ok ${output} ${box.width * args.scale}x${box.height * args.scale}`);
  } finally {
    if (client) client.close();
    if (browserClient) {
      await Promise.race([browserClient.send('Browser.close').catch(() => {}), sleep(3000)]);
      browserClient.close();
    } else {
      browser.kill();
    }
    for (let i = 0; i < 25; i++) {   // the profile stays locked until the browser has fully exited
      try { fs.rmSync(tmp, { recursive: true, force: true }); break; } catch { await sleep(200); }
    }
  }
}

main().catch(err => { console.error(`error=${err.message}`); process.exit(1); });
