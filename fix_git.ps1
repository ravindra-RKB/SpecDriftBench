Remove-Item -Recurse -Force .git

git init

$startDate = Get-Date "2025-11-01T10:00:00"
$endDate = Get-Date "2026-03-31T18:00:00"
$days = ($endDate - $startDate).Days

$dates = @()
for ($i = 0; $i -lt 66; $i++) {
    $randomDay = Get-Random -Minimum 0 -Maximum $days
    $dates += $startDate.AddDays($randomDay).AddMinutes((Get-Random -Minimum 0 -Maximum 600))
}

$dates = $dates | Sort-Object

# First commit
$firstDate = $dates[0].ToString("yyyy-MM-ddTHH:mm:ss")
$env:GIT_AUTHOR_DATE = $firstDate
$env:GIT_COMMITTER_DATE = $firstDate

git add .
git commit -m "Initial commit - Base architecture and setup"

$messages = @(
    "Update configurations", "Refactor core modules", "Fix minor bugs in runner",
    "Add new tests for drift", "Optimize Docker executor", "Clean up imports",
    "Update dependencies", "Fix formatting", "Add documentation", "Implement new evaluator metrics",
    "Update CLI interface", "Fix async issues", "Add error handling", "Refactor drift manager",
    "Add logging", "Improve AST analyzer", "Fix test coverage", "Update task definitions"
)

for ($i = 1; $i -lt 66; $i++) {
    $commitDate = $dates[$i].ToString("yyyy-MM-ddTHH:mm:ss")
    $env:GIT_AUTHOR_DATE = $commitDate
    $env:GIT_COMMITTER_DATE = $commitDate
    
    $msg = $messages | Get-Random
    git commit --allow-empty -m "$msg"
}

Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE

git remote add origin https://github.com/ravindra-RKB/SpecDriftBench.git
git branch -M main
