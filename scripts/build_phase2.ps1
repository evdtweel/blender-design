param(
    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-RequiredTopLevelFields {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Config
    )

    $requiredFields = @(
        'schemaVersion',
        'metadata',
        'units',
        'building',
        'door',
        'windows',
        'interiorWall',
        'roof',
        'cameraViews',
        'output'
    )

    $actualFields = @($Config.PSObject.Properties | ForEach-Object { $_.Name })

    foreach ($field in $requiredFields) {
        if ($actualFields -notcontains $field) {
            return $false
        }
    }

    return $true
}

try {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $configPath = Join-Path -Path $repoRoot -ChildPath 'config\phase2_probe.json'
    $blenderExecutable = $env:BLENDER_EXECUTABLE

    if ([string]::IsNullOrWhiteSpace($blenderExecutable)) {
        [Console]::Error.WriteLine('BLENDER_EXECUTABLE is niet ingesteld.')
        exit 10
    }

    if (-not (Test-Path -LiteralPath $blenderExecutable -PathType Leaf)) {
        [Console]::Error.WriteLine("BLENDER_EXECUTABLE wijst niet naar een bestaand bestand: $blenderExecutable")
        exit 11
    }

    $versionOutput = & $blenderExecutable --version
    $versionLines = @($versionOutput)
    $firstVersionLine = if ($versionLines.Count -gt 0) { $versionLines[0] } else { '' }

    if ($firstVersionLine -ne 'Blender 5.2.1 LTS') {
        [Console]::Error.WriteLine("Onverwachte Blender-versie: $firstVersionLine")
        exit 12
    }

    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        [Console]::Error.WriteLine("Configuratie ontbreekt: $configPath")
        exit 13
    }

    try {
        $config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    }
    catch {
        [Console]::Error.WriteLine("Configuratie is geen geldige JSON: $configPath")
        exit 13
    }

    if (-not (Test-RequiredTopLevelFields -Config $config)) {
        [Console]::Error.WriteLine("Configuratie mist verplichte hoofdvelden: $configPath")
        exit 13
    }

    if ($ValidateOnly) {
        Write-Host 'Validatie geslaagd.'
        exit 0
    }

    [Console]::Error.WriteLine('Generator ontbreekt nog; bouwen is in deze eerste versie niet beschikbaar.')
    exit 20
}
catch {
    [Console]::Error.WriteLine("Onverwachte fout: $($_.Exception.Message)")
    exit 99
}
