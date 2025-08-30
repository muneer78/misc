#!/bin/bash

extensions=(
  'accdb' 'archive' 'asp' 'at' 'bak' 'bat' 'bin' 'bsd' 'cmd' 'com' 'conf' 'config' 'cpp' 'crt'
  'csh' 'css' 'csv' 'dat' 'db' 'db3' 'dic' 'dict' 'dll' 'dmg' 'doc' 'docx' 'dotm' 'eml' 'emz'
  'enc' 'eps' 'epub' 'etag' 'exe' 'feather' 'gdb' 'gif' 'git' 'gliffy' 'groovy' 'gz' 'gzip' 'h'
  'heic' 'htm' 'html' 'hxd' 'icls' 'ico' 'ics' 'idx' 'iml' 'ini' 'ips' 'ipynb' 'j2' 'jar' 'java'
  'jfif' 'jpeg' 'jpg' 'js' 'json' 'kb' 'kgdb-wal' 'log' 'lua' 'm4a' 'map' 'mat' 'mbox' 'md' 'mime'
  'mit' 'mp3' 'mp4' 'msg' 'npy' 'npz' 'opml' 'orc' 'otf' 'parquet' 'pb' 'pbd' 'pdb' 'pdf' 'pickle'
  'pid' 'plist' 'pma' 'png' 'pot' 'potx' 'ppm' 'ppt' 'pptx' 'ps1' 'pst' 'pth' 'ptx' 'pub' 'pxd'
  'pxi' 'py' 'pyc' 'pyd' 'pyf' 'pyi' 'pys' 'pyw' 'pyx' 'r' 'rb' 'rc' 'rst' 'sav' 'sct' 'sdl' 'ses'
  'sh' 'sig' 'soql' 'sql' 'sql3' 'sqlite' 'sqlite3' 'sqlitedb' 'styl' 'svg' 'swo' 'tab' 'tbz'
  'tcl' 'tdb' 'toml' 'ts' 'tsx' 'ttf' 'tvdb' 'txt' 'vbs' 'ver' 'vscdb' 'vsdx' 'vstx' 'wasm' 'wav'
  'webp' 'whl' 'woff' 'woff2' 'xbm' 'xd' 'xls' 'xlsx' 'xltx' 'xmi' 'xml' 'xmlgz' 'xrc' 'xsl' 'xz'
  'yaml' 'yml' 'zi' 'zip' 'zwc'
)

for ext in "${extensions[@]}"; do
  if ! duti -x "$ext" &>/dev/null; then
    echo "No default app found for .$ext"
  else
    echo "Default app for .$ext:"
    duti -x "$ext"
  fi
done

