param(
    [switch]$ValidateOnly,
    [switch]$Clean,
    [string]$Config = 'config/songkhla_exterior.json',
    [string]$OutDir = 'out/phase3'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

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
    $allowedRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $resolvedRepoRoot -ChildPath 'out\phase3')).TrimEnd('\')
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

function Test-RequiredTopLevelFields {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$ConfigObject
    )

    $requiredFields = @(
        'schemaVersion',
        'metadata',
        'units',
        'coordinateSystem',
        'site',
        'buildingGrid',
        'levels',
        'facades',
        'roof',
        'openingTypes',
        'openingPlacementRules',
        'openingDisplay',
        'exteriorOpenings',
        'presentation',
        'unresolved'
    )

    $actualFields = @($ConfigObject.PSObject.Properties | ForEach-Object { $_.Name })

    foreach ($field in $requiredFields) {
        if ($actualFields -notcontains $field) {
            return $false
        }
    }

    return $true
}

function ConvertTo-NativeCommandLineArgument {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Argument
    )

    if ($Argument -notmatch '[\s"]') {
        return $Argument
    }

    return '"' + ($Argument.Replace('"', '\"')) + '"'
}

function Invoke-LoggedNativeCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [Parameter(Mandatory = $true)]
        [string]$LogPath
    )

    $logDirectory = Split-Path -Parent $LogPath
    $stdoutPath = Join-Path -Path $logDirectory -ChildPath 'build.stdout.tmp'
    $stderrPath = Join-Path -Path $logDirectory -ChildPath 'build.stderr.tmp'
    $quotedArguments = $Arguments | ForEach-Object { ConvertTo-NativeCommandLineArgument -Argument $_ }

    try {
        $process = Start-Process `
            -FilePath $Executable `
            -ArgumentList $quotedArguments `
            -RedirectStandardOutput $stdoutPath `
            -RedirectStandardError $stderrPath `
            -NoNewWindow `
            -PassThru `
            -Wait

        $stdout = if (Test-Path -LiteralPath $stdoutPath) { Get-Content -LiteralPath $stdoutPath -Raw } else { '' }
        $stderr = if (Test-Path -LiteralPath $stderrPath) { Get-Content -LiteralPath $stderrPath -Raw } else { '' }
        $combinedOutput = $stdout + $stderr

        Set-Content -LiteralPath $LogPath -Value $combinedOutput -NoNewline -Encoding UTF8

        if (-not [string]::IsNullOrEmpty($stdout)) {
            [Console]::Out.Write($stdout)
        }
        if (-not [string]::IsNullOrEmpty($stderr)) {
            [Console]::Error.Write($stderr)
        }

        return $process.ExitCode
    }
    finally {
        Remove-Item -LiteralPath $stdoutPath, $stderrPath -Force -ErrorAction SilentlyContinue
    }
}

try {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $configPath = Resolve-ProjectPath -RepoRoot $repoRoot -Path $Config
    $outDirPath = Resolve-ProjectPath -RepoRoot $repoRoot -Path $OutDir
    $generatorPath = Join-Path -Path $repoRoot -ChildPath 'scripts\blender\build_songkhla_exterior.py'
    $buildLogPath = Join-Path -Path $outDirPath -ChildPath 'logs\build.log'
    $blendPath = Join-Path -Path $outDirPath -ChildPath 'blender\songkhla_exterior.blend'
    $validationPath = Join-Path -Path $outDirPath -ChildPath 'reports\validation.json'
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

    if ($configObject.exteriorOpenings.Count -ne 16) {
        [Console]::Error.WriteLine("Configuratie moet exact 16 buitenopeningen bevatten.")
        exit 13
    }

    if (-not (Test-SafeOutDir -RepoRoot $repoRoot -ResolvedOutDir $outDirPath)) {
        [Console]::Error.WriteLine("Outputmap is niet toegestaan: $outDirPath")
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

    New-Item -ItemType Directory -Path (Split-Path -Parent $buildLogPath) -Force | Out-Null

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

    $blenderExitCode = Invoke-LoggedNativeCommand -Executable $blenderExecutable -Arguments $blenderArgs -LogPath $buildLogPath

    if ($blenderExitCode -ne 0) {
        [Console]::Error.WriteLine("Blender eindigde met exitcode $blenderExitCode.")
        exit 20
    }

    foreach ($requiredPath in @($blendPath, $validationPath)) {
        if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
            [Console]::Error.WriteLine("Verplichte uitvoer ontbreekt: $requiredPath")
            exit 20
        }
    }

    $successMessage = "Build geslaagd: $blendPath"
    Write-Host $successMessage
    Add-Content -LiteralPath $buildLogPath -Value $successMessage
    exit 0
}
catch {
    [Console]::Error.WriteLine("Onverwachte fout: $($_.Exception.Message)")
    exit 99
}
