# Links the Numentis WhatsApp Business Account to the app's webhook
# (https://numentis.vercel.app/api/whatsapp), so incoming messages reach the bot.
# Run: powershell -ExecutionPolicy Bypass -File tools\wa_subscribe.ps1
# Paste the WhatsApp access token when asked (the same one saved as WA_TOKEN in Vercel).

$Waba = '1453085660373335'
$Url = "https://graph.facebook.com/v21.0/$Waba/subscribed_apps"

$sec = Read-Host 'Paste WhatsApp access token' -AsSecureString
$tok = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
$h = @{ Authorization = "Bearer $tok" }

Write-Host "`nBefore:"
try { (Invoke-RestMethod -Uri $Url -Headers $h) | ConvertTo-Json -Depth 6 } catch { Write-Host $_.ErrorDetails.Message }

Write-Host "`nLinking..."
try { (Invoke-RestMethod -Method Post -Uri $Url -Headers $h) | ConvertTo-Json } catch { Write-Host $_.ErrorDetails.Message }

Write-Host "`nAfter:"
try { (Invoke-RestMethod -Uri $Url -Headers $h) | ConvertTo-Json -Depth 6 } catch { Write-Host $_.ErrorDetails.Message }
