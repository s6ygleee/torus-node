Add-Type -AssemblyName System.Drawing
$output = Join-Path $PSScriptRoot "..\assets\images\torus-node-social.png"
$bitmap = New-Object System.Drawing.Bitmap 1200, 630
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$navy = [System.Drawing.Color]::FromArgb(5, 10, 18)
$panel = [System.Drawing.Color]::FromArgb(10, 24, 42)
$cyan = [System.Drawing.Color]::FromArgb(86, 216, 225)
$blue = [System.Drawing.Color]::FromArgb(92, 148, 255)
$white = [System.Drawing.Color]::FromArgb(239, 246, 255)
$muted = [System.Drawing.Color]::FromArgb(166, 187, 211)
$graphics.Clear($navy)
$panelBrush = New-Object System.Drawing.SolidBrush $panel
$graphics.FillRectangle($panelBrush, 48, 48, 1104, 534)
$cyanPen = New-Object System.Drawing.Pen $cyan, 4
$bluePen = New-Object System.Drawing.Pen $blue, 2
for ($i = 0; $i -lt 8; $i++) {
  $offset = $i * 12
  $graphics.DrawEllipse($bluePen, 760 + $offset, 118 + ($offset / 3), 285 - ($offset * 2), 285 - ($offset * 2))
}
$graphics.DrawEllipse($cyanPen, 715, 92, 390, 390)
$graphics.DrawEllipse($cyanPen, 790, 190, 240, 110)
$graphics.DrawLine($bluePen, 715, 287, 1105, 287)
$smallFont = New-Object System.Drawing.Font "Segoe UI", 22, ([System.Drawing.FontStyle]::Bold)
$titleFont = New-Object System.Drawing.Font "Segoe UI", 48, ([System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font "Segoe UI", 27, ([System.Drawing.FontStyle]::Regular)
$smallBrush = New-Object System.Drawing.SolidBrush $cyan
$whiteBrush = New-Object System.Drawing.SolidBrush $white
$mutedBrush = New-Object System.Drawing.SolidBrush $muted
$graphics.DrawString("TORUS-NODE RESEARCH INITIATIVE", $smallFont, $smallBrush, 96, 108)
$graphics.DrawString("Emergent Spacetime,", $titleFont, $whiteBrush, 92, 190)
$graphics.DrawString("Gravity, and Gauge Structure", $titleFont, $whiteBrush, 92, 250)
$graphics.DrawString("Open research · Formal verification · Reproducible records", $subtitleFont, $mutedBrush, 96, 384)
$graphics.DrawString("s6ygleee.github.io/torus-node", $smallFont, $smallBrush, 96, 488)
$bitmap.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)
$smallBrush.Dispose(); $whiteBrush.Dispose(); $mutedBrush.Dispose()
$smallFont.Dispose(); $titleFont.Dispose(); $subtitleFont.Dispose()
$cyanPen.Dispose(); $bluePen.Dispose(); $panelBrush.Dispose()
$graphics.Dispose(); $bitmap.Dispose()
Write-Output $output
