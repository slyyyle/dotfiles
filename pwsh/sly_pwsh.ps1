Import-Module "gsudoModule"
Set-Alias sudo gsudo

$ScriptBlock = {
	Param([string]$line)

	if ($line -match "^git") {
		return $false
	} else {
		return $true
	}
}

function zsoff { 
	sudo {Get-NetAdapterBinding -AllBindings -ComponentID ZS_ZAPPRD | Disable-NetAdapterBinding}
}

function zson {
	sudo {Get-NetAdapterBinding -AllBindings -ComponentID ZS_ZAPPRD | Enable-NetAdapterBinding}
}

Set-PSReadLineOption -AddToHistoryHandler $ScriptBlock -HistorySavePath "$env:USERPROFILE\.config\pwsh\sly_history.txt" -HistorySearchCursorMovesToEnd:$True -PredictionSource HistoryAndPlugin -PredictionViewStyle ListView

function omac01 { plink -pw PressTab123 khammitt@omacsndbx01 }

function yt { mov-cli -s youtube  $args }

Invoke-Expression (&starship init powershell)
