param(
    [switch]$ValidateOnly,
    [switch]$Clean,
    [string]$Config = 'config/phase2_probe.json',
    [string]$OutDir = 'out/phase2'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-RequiredTopLevelFields {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$ConfigObject
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

    $actualFields = @($ConfigObject.PSObject.Properties | ForEach-Object { $_.Name })

    foreach ($field in $requiredFields) {
        if ($actualFields -notcontains $field) {
            return $false
        }
    }

    return $true
}

function Resolve-ProjectPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot,

        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path -Path $RepoRoot -ChildPath $Path))
}

function Test-SafeOutDir {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot,

        [Parameter(Mandatory = $true)]
        [string]$ResolvedOutDir
    )

    $resolvedRepoRoot = [System.IO.Path]::GetFullPath($RepoRoot).TrimEnd('\')
    $repoOut = [System.IO.Path]::GetFullPath((Join-Path -Path $resolvedRepoRoot -ChildPath 'out')).TrimEnd('\')
    $allowedRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $resolvedRepoRoot -ChildPath 'out\phase2')).TrimEnd('\')
    $candidate = [System.IO.Path]::GetFullPath($ResolvedOutDir).TrimEnd('\')

    if ($candidate.Equals($resolvedRepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $false
    }

    if ($candidate.Equals($repoOut, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $false
    }

    if ($candidate.Equals($allowedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }

    return $candidate.StartsWith($allowedRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)
}

function Resolve-BlendOutputPath {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$ConfigObject,

        [Parameter(Mandatory = $true)]
        [string]$ResolvedOutDir
    )

    $outputFields = @($ConfigObject.output.PSObject.Properties | ForEach-Object { $_.Name })
    if ($outputFields -notcontains 'blend') {
        throw "Configuratie mist output.blend."
    }

    $blendRelativePath = [string]$ConfigObject.output.blend
    if ([string]::IsNullOrWhiteSpace($blendRelativePath)) {
        throw "Configuratieveld output.blend is leeg."
    }

    if ([System.IO.Path]::IsPathRooted($blendRelativePath)) {
        throw "Configuratieveld output.blend mag geen absoluut pad zijn: $blendRelativePath"
    }

    $segments = @($blendRelativePath -split '[\\/]')
    if ($segments -contains '..') {
        throw "Configuratieveld output.blend mag geen '..'-padsegment bevatten: $blendRelativePath"
    }

    $blendPath = [System.IO.Path]::GetFullPath((Join-Path -Path $ResolvedOutDir -ChildPath $blendRelativePath))
    $resolvedOutDirForComparison = [System.IO.Path]::GetFullPath($ResolvedOutDir).TrimEnd('\')
    $resolvedBlendPath = $blendPath.TrimEnd('\')

    if (-not $resolvedBlendPath.StartsWith($resolvedOutDirForComparison + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Blend-uitvoer valt buiten de outputmap: $blendPath"
    }

    return $blendPath
}

try {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $configPath = Resolve-ProjectPath -RepoRoot $repoRoot -Path $Config
    $outDirPath = Resolve-ProjectPath -RepoRoot $repoRoot -Path $OutDir
    $generatorPath = Join-Path -Path $repoRoot -ChildPath 'scripts\blender\build_phase2_probe.py'
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
        $configObject = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    }
    catch {
        [Console]::Error.WriteLine("Configuratie is geen geldige JSON: $configPath")
        exit 13
    }

    if (-not (Test-RequiredTopLevelFields -ConfigObject $configObject)) {
        [Console]::Error.WriteLine("Configuratie mist verplichte hoofdvelden: $configPath")
        exit 13
    }

    if (-not (Test-SafeOutDir -RepoRoot $repoRoot -ResolvedOutDir $outDirPath)) {
        [Console]::Error.WriteLine("Outputmap is niet toegestaan: $outDirPath")
        exit 20
    }

    try {
        $blendPath = Resolve-BlendOutputPath -ConfigObject $configObject -ResolvedOutDir $outDirPath
    }
    catch {
        [Console]::Error.WriteLine($_.Exception.Message)
        exit 20
    }

    if (-not (Test-Path -LiteralPath $generatorPath -PathType Leaf)) {
        [Console]::Error.WriteLine("Generator ontbreekt: $generatorPath")
        exit 20
    }

    if ($ValidateOnly) {
        Write-Host 'Validatie geslaagd.'
        exit 0
    }

    if ($Clean -and (Test-Path -LiteralPath $outDirPath)) {
        Remove-Item -LiteralPath $outDirPath -Recurse -Force
    }

    if (-not (Test-Path -LiteralPath $outDirPath -PathType Container)) {
        New-Item -ItemType Directory -Path $outDirPath | Out-Null
    }

    $blenderArgs = @(
        '--background',
        '--factory-startup',
        '--python',
        $generatorPath,
        '--',
        '--config',
        $configPath,
        '--out-dir',
        $outDirPath
    )

    & $blenderExecutable @blenderArgs
    $blenderExitCode = $LASTEXITCODE

    if ($blenderExitCode -ne 0) {
        [Console]::Error.WriteLine("Blender eindigde met exitcode $blenderExitCode.")
        exit 20
    }

    if (-not (Test-Path -LiteralPath $blendPath -PathType Leaf)) {
        [Console]::Error.WriteLine("Blend-bestand ontbreekt: $blendPath")
        exit 20
    }

    $blendFile = Get-Item -LiteralPath $blendPath
    if ($blendFile.Length -le 0) {
        [Console]::Error.WriteLine("Blend-bestand is leeg: $blendPath")
        exit 20
    }

    Write-Host "Build geslaagd: $blendPath"
    exit 0
}
catch {
    [Console]::Error.WriteLine("Onverwachte fout: $($_.Exception.Message)")
    exit 99
}
