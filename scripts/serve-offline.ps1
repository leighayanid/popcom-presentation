<#
    Serve the built deck offline, with nothing installed.

    A Slidev build is a single-page app: its scripts are ES modules, and
    Chromium refuses to load those over file://, so the folder cannot just be
    double-clicked -- it has to come off a web server. This is that server,
    written against .NET's HttpListener so it runs on a stock Windows box with
    no Node, no npm and no Python.

    Serves the folder it sits in (or ..\offline when run from scripts\),
    opens the browser, and runs until Ctrl+C.
#>
[CmdletBinding()]
param(
    [string] $Root,
    [int]    $Port = 3030,
    [switch] $NoBrowser
)

$ErrorActionPreference = 'Stop'

# Run from inside the bundle, or from the repo's scripts\ folder.
if (-not $Root) {
    $here = $PSScriptRoot
    if (Test-Path (Join-Path $here 'index.html')) { $Root = $here }
    else { $Root = Join-Path (Split-Path $here -Parent) 'offline' }
}
$Root = (Resolve-Path -LiteralPath $Root).Path

if (-not (Test-Path (Join-Path $Root 'index.html'))) {
    Write-Host "No index.html in $Root" -ForegroundColor Red
    Write-Host "Build the bundle first:  npm run offline" -ForegroundColor Yellow
    exit 1
}

# text/javascript matters: a module served as text/plain is refused outright.
$mime = @{
    '.html' = 'text/html; charset=utf-8'; '.js' = 'text/javascript; charset=utf-8'
    '.mjs'  = 'text/javascript; charset=utf-8'; '.css' = 'text/css; charset=utf-8'
    '.json' = 'application/json; charset=utf-8'; '.svg' = 'image/svg+xml'
    '.png'  = 'image/png'; '.jpg' = 'image/jpeg'; '.jpeg' = 'image/jpeg'
    '.gif'  = 'image/gif'; '.webp' = 'image/webp'; '.avif' = 'image/avif'
    '.ico'  = 'image/x-icon'; '.woff' = 'font/woff'; '.woff2' = 'font/woff2'
    '.ttf'  = 'font/ttf'; '.otf' = 'font/otf'; '.mp4' = 'video/mp4'
    '.webm' = 'video/webm'; '.mp3' = 'audio/mpeg'; '.txt' = 'text/plain; charset=utf-8'
    '.map'  = 'application/json; charset=utf-8'; '.pdf' = 'application/pdf'
}

# If 3030 is busy, walk up until something is free.
$listener = $null
foreach ($p in $Port..($Port + 20)) {
    $try = New-Object System.Net.HttpListener
    $try.Prefixes.Add("http://localhost:$p/")
    try { $try.Start(); $listener = $try; $Port = $p; break }
    catch { try { $try.Close() } catch {} }
}
if (-not $listener) {
    Write-Host "Could not open a port in $Port..$($Port + 20)." -ForegroundColor Red
    exit 1
}

$url = "http://localhost:$Port/"
Write-Host ""
Write-Host "  Deck   $url" -ForegroundColor Cyan
Write-Host "  From   $Root" -ForegroundColor DarkGray
Write-Host "  Stop   Ctrl+C" -ForegroundColor DarkGray
Write-Host ""
if (-not $NoBrowser) { Start-Process $url | Out-Null }

try {
    while ($listener.IsListening) {
        $ctx = $listener.GetContext()
        $res = $ctx.Response
        try {
            $rel = [System.Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart('/')
            if ($rel -eq '') { $rel = 'index.html' }
            $path = Join-Path $Root ($rel -replace '/', '\')

            # Keep the server inside its own folder.
            $full = [System.IO.Path]::GetFullPath($path)
            if (-not $full.StartsWith($Root, [StringComparison]::OrdinalIgnoreCase)) {
                $res.StatusCode = 403; $res.Close(); continue
            }

            # The deck routes client-side (/7, /presenter/3), so anything that
            # is not a real file is handed to the app, not 404'd.
            if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
                $full = Join-Path $Root 'index.html'
            }

            $ext = [System.IO.Path]::GetExtension($full).ToLowerInvariant()
            $res.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }
            $bytes = [System.IO.File]::ReadAllBytes($full)
            $res.ContentLength64 = $bytes.Length
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
        }
        catch {
            try { $res.StatusCode = 500 } catch {}
        }
        finally {
            try { $res.Close() } catch {}
        }
    }
}
finally {
    try { $listener.Stop(); $listener.Close() } catch {}
    Write-Host "Stopped." -ForegroundColor DarkGray
}
